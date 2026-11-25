#!/usr/bin/env python3
"""
Hack Two-Pass Assembler
Course: ETCMTC301 - Nand to Tetris
Student Name: Siya Singh
Roll Number: 2501730417
Parameter K: 17 (Roll ending: 417 -> K = 17 -> K mod 3 = 2: Duplicate Label Detection Warning)

Converts symbolic Hack assembly (.asm) into 16-bit binary machine code (.hack).
Implements pure two-pass compilation with duplicate label diagnostics.
"""

import sys
import re

PREDEFINED_SYMBOLS = {
    'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3,
    'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
    'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
    'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
    'SCREEN': 16384, 'KBD': 24576,
    'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4
}

DEST_TABLE = {
    '': '000', 'M': '001', 'D': '010', 'MD': '011',
    'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'
}

JUMP_TABLE = {
    '': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
    'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'
}

COMP_TABLE = {
    '0': '0101010', '1': '0111111', '-1': '0111010',
    'D': '0001100', 'A': '0110000', '!D': '0001101',
    '!A': '0110001', '-D': '0001111', '-A': '0110011',
    'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
    'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
    'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
    'M': '1110000', '!M': '1110001', '-M': '1110011',
    'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010',
    'D-M': '1010011', 'M-D': '1000111', 'D&M': '1000000',
    'D|M': '1010101'
}

class HackAssembler:
    def __init__(self, k_val=17):
        self.k_val = k_val
        self.k_mod_3 = k_val % 3
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.label_definitions = {}
        self.warnings = []
        self.next_var_address = 16

    def clean_line(self, line):
        line = re.sub(r'//.*', '', line)
        return line.strip()

    def assemble(self, asm_content):
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.label_definitions = {}
        self.warnings = []
        self.next_var_address = 16

        lines = asm_content.splitlines()
        clean_lines = []
        
        # Pass 1: Build Symbol Table for Labels & Detect Duplicates
        rom_address = 0
        for line_num, raw_line in enumerate(lines, start=1):
            line = self.clean_line(raw_line)
            if not line:
                continue
            if line.startswith('(') and line.endswith(')'):
                label = line[1:-1].strip()
                if not label:
                    continue
                if label in self.label_definitions:
                    first_line = self.label_definitions[label]['line']
                    orig_addr = self.label_definitions[label]['addr']
                    warn_msg = (f"Warning: Duplicate label '{label}' detected at Line {line_num}. "
                                f"First definition is at Line {first_line}. Preserving original ROM address {orig_addr}.")
                    self.warnings.append(warn_msg)
                    if self.k_mod_3 == 1:
                        raise ValueError(f"Strict Duplicate Label Error: '{label}' redefined at Line {line_num}")
                else:
                    self.label_definitions[label] = {'line': line_num, 'addr': rom_address}
                    self.symbol_table[label] = rom_address
            else:
                clean_lines.append((line_num, line))
                rom_address += 1

        # Pass 2: Translate Instructions
        machine_code = []
        for line_num, line in clean_lines:
            if line.startswith('@'):
                val_str = line[1:].strip()
                if val_str.isdigit():
                    addr = int(val_str)
                else:
                    if val_str not in self.symbol_table:
                        self.symbol_table[val_str] = self.next_var_address
                        self.next_var_address += 1
                    addr = self.symbol_table[val_str]
                binary_code = f"0{addr:015b}"
                machine_code.append(binary_code)
            else:
                dest_part, comp_part, jump_part = '', '', ''
                if '=' in line:
                    dest_part, rest = line.split('=', 1)
                else:
                    rest = line
                if ';' in rest:
                    comp_part, jump_part = rest.split(';', 1)
                else:
                    comp_part = rest

                dest_part = dest_part.strip()
                comp_part = comp_part.strip()
                jump_part = jump_part.strip()

                if comp_part not in COMP_TABLE:
                    raise ValueError(f"Invalid computation '{comp_part}' at line {line_num}: {line}")
                if dest_part not in DEST_TABLE:
                    raise ValueError(f"Invalid destination '{dest_part}' at line {line_num}: {line}")
                if jump_part not in JUMP_TABLE:
                    raise ValueError(f"Invalid jump '{jump_part}' at line {line_num}: {line}")

                comp_bin = COMP_TABLE[comp_part]
                dest_bin = DEST_TABLE[dest_part]
                jump_bin = JUMP_TABLE[jump_part]

                binary_code = f"111{comp_bin}{dest_bin}{jump_bin}"
                machine_code.append(binary_code)

        return machine_code, self.warnings

def main():
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <input.asm> [output.hack]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.asm', '.hack')

    with open(input_file, 'r', encoding='utf-8') as f:
        asm_content = f.read()

    assembler = HackAssembler(k_val=17)
    try:
        binary_lines, warnings = assembler.assemble(asm_content)
        for w in warnings:
            print(f"[K-MOD-3 DIAGNOSTIC] {w}")

        with open(output_file, 'w', encoding='utf-8') as f:
            for line in binary_lines:
                f.write(line + '\n')
        print(f"Assembly successful: {len(binary_lines)} instructions written to {output_file}")
    except Exception as e:
        print(f"Assembly Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
