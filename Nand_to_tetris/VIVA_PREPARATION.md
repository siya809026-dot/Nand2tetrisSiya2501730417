# VIVA VOCE DEFENSE & ARCHITECTURAL REFERENCE
## ETCMTC301 - Nand to Tetris Capstone
**Candidate:** Siya Singh | Roll: 2501730417 | Parameter K = 17 (Ending: 417 -> K mod 3 = 2)

---

### Q1: How does the CPU distinguish between A-instruction and C-instruction?
**Answer:** The most significant bit (`instruction[15]`) serves as the opcode flag. When bit 15 is `0`, it is an A-instruction, and the lower 15 bits represent an immediate non-negative constant loaded into the A-Register. When bit 15 is `1`, bits 14 and 13 are unused (`11`), bit 12 (`a`) selects whether the ALU operates on A or Memory (`inM`), bits 11..6 encode the 6 ALU control flags (`zx, nx, zy, ny, f, no`), bits 5..3 determine destination registers (`A, D, M`), and bits 2..0 specify jump conditions.

### Q2: Why is `writeM` suppressed during an A-instruction?
**Answer:** In an A-instruction, bit 3 (`d3` in a C-instruction) may coincidentally be 1 as part of the constant payload. Therefore, `writeM` must strictly be gated by an `And` gate combining `isCInstruction` and `instruction[3]`. Without this, loading constants could inadvertently corrupt data in memory.

### Q3: How is the Screen Memory mapped for Parameter K = 17 (Roll: 2501730417)?
**Answer:** The Hack screen has 256 rows and 512 pixels per row. Each row consists of 32 16-bit words (\(512 / 16 = 32\)). The screen base address is `RAM[16384]`.
Row 17 starts at:
\[ 16384 + (17 \times 32) = 16384 + 544 = 16928 \]
A 32-pixel width occupies 2 words: Word 0 at address `16928` and Word 1 at `16929`. For a height of 20 rows (Rows 17 to 36), the final row (36) ends at:
\[ 16384 + (36 \times 32) + 1 = 16384 + 1152 + 1 = 17537 \]

### Q4: Explain the requirement for (K mod 3) = 2 in the Assembler.
**Answer:** With \(K = 17\), \(17 \pmod 3 = 2\). When a label `(LABEL)` appears more than once in the assembly source code, the assembler must not crash; instead, it generates a diagnostic warning message, ignores the second definition, and preserves the original ROM address registered in the symbol table.
