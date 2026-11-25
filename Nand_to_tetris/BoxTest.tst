// BoxTest.tst - Test script for Box.hack execution on Hack CPU
// Course: ETCMTC301 - Nand to Tetris
// Student: Siya Singh (2501730417, K=17)

load Box.hack,
output-file BoxTest.out,
compare-to BoxTest.cmp,
output-list RAM[24576]%D1.6.1 RAM[16928]%D1.6.1 RAM[16929]%D1.6.1 RAM[17536]%D1.6.1 RAM[17537]%D1.6.1;

// Test 1: Key released (KBD=0) -> Screen words must be 0
set RAM[24576] 0,
repeat 300 {
    ticktock;
}
output;

// Test 2: Key pressed (KBD=65 'A') -> Screen words must be -1
set RAM[24576] 65,
repeat 1500 {
    ticktock;
}
output;

// Test 3: Key released again -> Screen words must clear to 0
set RAM[24576] 0,
repeat 1500 {
    ticktock;
}
output;
