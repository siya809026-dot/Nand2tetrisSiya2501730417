// Pong - NAND to Tetris (Hack Assembly)
// Basic screen-fill test program.
// This is a starter program, not the complete Pong game.

@SCREEN
D=A
@address
M=D

(LOOP)
    @address
    A=M
    M=-1

    @address
    M=M+1

    @KBD
    D=A
    @address
    D=M-D

    @LOOP
    D;JLT

(END)
    @END
    0;JMP
