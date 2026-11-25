# CAPSTONE PROJECT REPORT: HACK COMPUTER SYSTEM & GRAPHICS EMULATION
**Course Code:** ETCMTC301 - Nand to Tetris  
**Academic Year:** 2026-2027  
**Student:** Siya Singh (Roll: 2501730417)  
**Supervisor / Department:** School of Engineering & Technology, K.R. Mangalam University  

---

## 1. Abstract & Executive Summary
This capstone engineering project encompasses the design, hardware synthesis, assembler software construction, and real-time machine execution of the Hack Computer architecture. Built upon the first principles of digital logic (NAND gates to arithmetic units, registers, memory decoders, and program counters), the project culminates in a complete software toolchain and interactive 16-bit Von Neumann machine emulator executing interactive graphics.

All hardware specifications, memory maps, assembler warning mechanisms, and screen coordinates are individualized to University Roll Number **2501730417**:
- **Student Roll Number:** 2501730417 (Ending digits: 417)
- **Parameter K:** 17 (last two digits of university roll number)
- **Case Selection:** \(K \pmod 3 = 17 \pmod 3 = 2\) (Duplicate label detection warning with first-occurrence preservation)
- **Display Output:** 32 pixels wide by 20 rows tall rectangular box starting at Screen Row 17 (RAM[16928..17537]).

---

## 2. Part A: Hack Computer HDL Architecture
The Hack Computer consists of three core chips:
1. **CPU.hdl:** Implements instruction decoding separating A-instructions (`0...`) from C-instructions (`111...`). Contains an A-Register, D-Register, 16-bit ALU, writeM gating, and a 15-bit Program Counter (PC) equipped with jump logic computed from ALU zero (`zr`) and negative (`ng`) output flags.
2. **Memory.hdl:** Complete 32K address space mapping 16K Data RAM (`0x0000..0x3FFF`), 8K Screen memory (`0x4000..0x5FFF`), and the single-word Keyboard register (`0x6000`, address 24576).
3. **Computer.hdl:** Top-level chip tying ROM32K instruction memory to the CPU and Memory subsystems under a synchronous global clock.

All HDL designs passed formal verification against official test scripts (`CPU.tst`, `Memory.tst`, `Computer.tst`) with zero comparison discrepancies.

---

## 3. Part B: Python Two-Pass Assembler
The custom assembler (`assembler.py`) translates Hack assembly into binary machine code across two sequential passes:
- **Pass 1 (Symbolic Resolution):** Scans the source file, records label symbols `(LABEL)` mapped to their respective ROM program memory index, and executes diagnostic duplicate label checks. For \(K \pmod 3 = 17 \pmod 3 = 2\), encountering an existing label emits an explicit diagnostic warning and preserves the original declaration address.
- **Pass 2 (Code Generation):** Replaces variable symbols with sequential RAM addresses starting at `RAM[16]`, and encodes A-instructions and C-instructions into strict 16-bit binary words according to standard Hack truth tables.

---

## 4. Part C: Interactive Box Program & Real-Time Emulator
`Box.asm` implements an event-driven polling loop that continuously queries `RAM[24576]` (Keyboard).
- When a keystroke is detected, the program iterates through 20 screen rows (Rows 17 to 36), writing `-1` (`0xFFFF`, all 16 pixels black) into Word 0 and Word 1 of each row (32 pixels across).
- When the key is released (`RAM[24576] == 0`), the routine clears the identical address block to `0` (white).

Real-time software emulation verifies CPU register updates (PC, A, D, KBD) cycle-by-cycle while painting memory-mapped pixels onto a 512x256 display canvas.
