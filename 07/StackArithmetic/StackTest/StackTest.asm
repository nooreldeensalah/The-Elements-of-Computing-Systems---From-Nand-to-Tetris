// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M-D
@True.0
D;JEQ
@False.0
D;JNE
(True.0)
@SP
A=M
M=-1
@SP
M=M+1@Skip.0
0;JEQ
(False.0)
@SP
A=M
M=0
@SP
M=M+1(Skip.0)
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M-D
@True.0
D;JEQ
@False.0
D;JNE
(True.0)
@SP
A=M
M=-1
@SP
M=M+1@Skip.0
0;JEQ
(False.0)
@SP
A=M
M=0
@SP
M=M+1(Skip.0)
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M-D
@True.0
D;JEQ
@False.0
D;JNE
(True.0)
@SP
A=M
M=-1
@SP
M=M+1@Skip.0
0;JEQ
(False.0)
@SP
A=M
M=0
@SP
M=M+1(Skip.0)
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M-D
@True.0
D;JLE
@False.0
D;JGT
(True.0)
@SP
A=M
M=-1
@SP
M=M+1@Skip.0
0;JEQ
(False.0)
@SP
A=M
M=0
@SP
M=M+1(Skip.0)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M-D
@True.0
D;JLE
@False.0
D;JGT
(True.0)
@SP
A=M
M=-1
@SP
M=M+1@Skip.0
0;JEQ
(False.0)
@SP
A=M
M=0
@SP
M=M+1(Skip.0)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M-D
@True.0
D;JLE
@False.0
D;JGT
(True.0)
@SP
A=M
M=-1
@SP
M=M+1@Skip.0
0;JEQ
(False.0)
@SP
A=M
M=0
@SP
M=M+1(Skip.0)
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M-D
@True.0
D;JGT
@False.0
D;JLE
(True.0)
@SP
A=M
M=-1
@SP
M=M+1@Skip.0
0;JEQ
(False.0)
@SP
A=M
M=0
@SP
M=M+1(Skip.0)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M-D
@True.0
D;JGT
@False.0
D;JLE
(True.0)
@SP
A=M
M=-1
@SP
M=M+1@Skip.0
0;JEQ
(False.0)
@SP
A=M
M=0
@SP
M=M+1(Skip.0)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M-D
@True.0
D;JGT
@False.0
D;JLE
(True.0)
@SP
A=M
M=-1
@SP
M=M+1@Skip.0
0;JEQ
(False.0)
@SP
A=M
M=0
@SP
M=M+1(Skip.0)
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M+D
@SP
A=M
M=D
@SP
M=M+1
// push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M-D
@SP
A=M
M=D
@SP
M=M+1
// neg
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@R13
D=-M
@SP
A=M
M=D
@SP
M=M+1
// and
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M&D
@SP
A=M
M=D
@SP
M=M+1
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R13
D=M
@R14
D=M|D
@SP
A=M
M=D
@SP
M=M+1
// not
@SP
M=M-1
@SP
A=M
D=M
@R13
M=D
@R13
D=!M
@SP
A=M
M=D
@SP
M=M+1
