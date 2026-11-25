// Box.asm - Capstone Project: Make the Computer Draw a Box
// Course: ETCMTC301 - Nand to Tetris - Project 4 / Capstone
// Student Name: Siya Singh
// Roll Number: 2501730417 (Ending in 417 -> Parameter K = 17)
// School of Engineering & Technology, K.R. Mangalam University
//
// Hardware Parameters Calculated from Roll Number:
// Parameter K = 17 (Last digits of 2501730417)
// K mod 3 = 17 mod 3 = 2
// Box Start Row: 17
// Box Height: 20 rows (Row 17 to Row 36 inclusive)
// Box Width: 32 pixels (2 16-bit words: Word 0 and Word 1 of each row)
// Screen Memory Range: RAM[16928] to RAM[17537]
//
// Logic:
// Continuously monitors keyboard register RAM[24576].
// When any key is pressed (RAM[24576] != 0), fills the 32x20 box with black (-1).
// When key is released (RAM[24576] == 0), clears the box with white (0).

(MAIN_LOOP)
    // 1. Poll the keyboard register
    @24576
    D=M
    @KEY_PRESSED
    D;JNE

    // Key is released -> set color to white (0)
    @color
    M=0
    @DRAW_BOX
    0;JMP

(KEY_PRESSED)
    // Key is pressed -> set color to black (-1 / 0xFFFF)
    @color
    M=-1

(DRAW_BOX)
    // Initialize row counter: row = 0
    @row
    M=0

(ROW_LOOP)
    // Check if row == 20 (height limit)
    @row
    D=M
    @20
    D=D-A
    @MAIN_LOOP
    D;JEQ

    // Calculate row memory offset: offset = row * 32
    @row
    D=M
    @offset
    M=D
    M=M+D    // offset = row * 2
    D=M
    M=M+D    // offset = row * 4
    D=M
    M=M+D    // offset = row * 8
    D=M
    M=M+D    // offset = row * 16
    D=M
    M=M+D    // offset = row * 32

    // Target address = 16928 + offset
    @16928
    D=A
    @offset
    D=D+M
    @addr
    M=D

    // Write Word 0 (pixels 0..15 of row)
    @color
    D=M
    @addr
    A=M
    M=D

    // Write Word 1 (pixels 16..31 of row, addr + 1)
    @addr
    M=M+1
    A=M
    M=D

    // Increment row counter: row = row + 1
    @row
    M=M+1

    @ROW_LOOP
    0;JMP
