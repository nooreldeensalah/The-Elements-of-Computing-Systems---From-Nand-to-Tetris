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
M=M+1
@Skip.0
0;JEQ
(False.0)
@SP
A=M
M=0
@SP
M=M+1
(Skip.0)
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
@True.1
D;JEQ
@False.1
D;JNE
(True.1)
@SP
A=M
M=-1
@SP
M=M+1
@Skip.1
0;JEQ
(False.1)
@SP
A=M
M=0
@SP
M=M+1
(Skip.1)
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
@True.2
D;JEQ
@False.2
D;JNE
(True.2)
@SP
A=M
M=-1
@SP
M=M+1
@Skip.2
0;JEQ
(False.2)
@SP
A=M
M=0
@SP
M=M+1
(Skip.2)
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
@True.3
D;JLT
@False.3
D;JGT
(True.3)
@SP
A=M
M=-1
@SP
M=M+1
@Skip.3
0;JEQ
(False.3)
@SP
A=M
M=0
@SP
M=M+1
(Skip.3)
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
@True.4
D;JLT
@False.4
D;JGT
(True.4)
@SP
A=M
M=-1
@SP
M=M+1
@Skip.4
0;JEQ
(False.4)
@SP
A=M
M=0
@SP
M=M+1
(Skip.4)
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
@True.5
D;JLT
@False.5
D;JGT
(True.5)
@SP
A=M
M=-1
@SP
M=M+1
@Skip.5
0;JEQ
(False.5)
@SP
A=M
M=0
@SP
M=M+1
(Skip.5)
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
@True.6
D;JGT
@False.6
D;JLT
(True.6)
@SP
A=M
M=-1
@SP
M=M+1
@Skip.6
0;JEQ
(False.6)
@SP
A=M
M=0
@SP
M=M+1
(Skip.6)
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
@True.7
D;JGT
@False.7
D;JLT
(True.7)
@SP
A=M
M=-1
@SP
M=M+1
@Skip.7
0;JEQ
(False.7)
@SP
A=M
M=0
@SP
M=M+1
(Skip.7)
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
@True.8
D;JGT
@False.8
D;JLT
(True.8)
@SP
A=M
M=-1
@SP
M=M+1
@Skip.8
0;JEQ
(False.8)
@SP
A=M
M=0
@SP
M=M+1
(Skip.8)
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
