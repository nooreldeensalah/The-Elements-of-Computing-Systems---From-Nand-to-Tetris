
// ---- Setup-------
@8192
D = A
@n          //17
M = D
// ----------Reading Keyboard----------------
(CHECKING)
@KBD
D = M
@WHITEN
D ; JEQ
@BLACKEN
D ; JNE
// ----- Settings Registers to zero -----
(WHITEN)
@i
M = 0
@SCREEN
D = A
@Screen_Address // 16
M = D //16384
(LOOP_WHITE)
@i
D = M
@n
D = D - M
@CHECKING
D ; JGE

@Screen_Address
A = M
M = 0
@i
M = M + 1
@Screen_Address
M = M + 1
@LOOP_WHITE
0; JMP

(BLACKEN)
@i
M = 0
@SCREEN
D = A
@Screen_Address // 16
M = D //16384
(LOOP_BLACK)
@i
D = M
@n
D = D - M
@CHECKING
D ; JGE

@Screen_Address
A = M
M = -1
@i
M = M + 1
@Screen_Address
M = M + 1
@LOOP_BLACK
0; JMP