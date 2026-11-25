const fs = require("fs");
const path = require("path");

const asmPath = path.join(__dirname, "Nand_to_tetris", "Box.asm");
const hackPath = path.join(__dirname, "Nand_to_tetris", "Box.hack");

const asm = fs.readFileSync(asmPath, "utf8");

const PREDEFINED = {
  R0: 0, R1: 1, R2: 2, R3: 3, R4: 4, R5: 5, R6: 6, R7: 7,
  R8: 8, R9: 9, R10: 10, R11: 11, R12: 12, R13: 13, R14: 14, R15: 15,
  SCREEN: 16384, KBD: 24576, SP: 0, LCL: 1, ARG: 2, THIS: 3, THAT: 4
};
const DEST = {
  "": "000", "M": "001", "D": "010", "MD": "011",
  "A": "100", "AM": "101", "AD": "110", "AMD": "111"
};
const JUMP = {
  "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
  "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
};
const COMP = {
  "0": "0101010", "1": "0111111", "-1": "0111010",
  "D": "0001100", "A": "0110000", "!D": "0001101",
  "!A": "0110001", "-D": "0001111", "-A": "0110011",
  "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
  "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
  "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
  "M": "1110000", "!M": "1110001", "-M": "1110011",
  "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
  "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
  "D|M": "1010101"
};

const lines = asm.split(/\r?\n/);
let rom = 0;
const symbols = { ...PREDEFINED };
const instructions = [];

for (const raw of lines) {
  const line = raw.replace(/\/\/.*/, "").trim();
  if (!line) continue;
  if (line.startsWith("(") && line.endsWith(")")) {
    const label = line.slice(1, -1).trim();
    if (!(label in symbols)) {
      symbols[label] = rom;
    }
  } else {
    instructions.push(line);
    rom++;
  }
}

let nextVar = 16;
const output = [];

for (const line of instructions) {
  if (line.startsWith("@")) {
    const sym = line.slice(1).trim();
    let addr;
    if (/^\d+$/.test(sym)) {
      addr = parseInt(sym, 10);
    } else {
      if (!(sym in symbols)) {
        symbols[sym] = nextVar++;
      }
      addr = symbols[sym];
    }
    output.push("0" + addr.toString(2).padStart(15, "0"));
  } else {
    let dest = "", comp = "", jump = "";
    let rest = line;
    if (rest.includes("=")) {
      const parts = rest.split("=");
      dest = parts[0].trim();
      rest = parts[1].trim();
    }
    if (rest.includes(";")) {
      const parts = rest.split(";");
      comp = parts[0].trim();
      jump = parts[1].trim();
    } else {
      comp = rest.trim();
    }
    const bin = "111" + COMP[comp] + DEST[dest] + JUMP[jump];
    output.push(bin);
  }
}

fs.writeFileSync(hackPath, output.join("\n") + "\n");
console.log("Successfully assembled Box.asm -> Box.hack:", output.length, "instructions");
