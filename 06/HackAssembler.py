import sys
from re import split as re_split

SymbolsDict = {
    "SCREEN": "16384",
    "KBD": "24576",
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4",
}
for number in range(16):
    SymbolsDict[f"R{number}"] = number
CompAndJumpDict = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}
DestDict = {
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}


def CInstructionHandler(Instruction):
    global DestDict
    global CompAndJumpDict
    splitted_instruction = re_split("[=;]", Instruction)
    if len(splitted_instruction) == 3:
        dest = DestDict[splitted_instruction[0]]
        comp = CompAndJumpDict[splitted_instruction[1]]
        jump = CompAndJumpDict[splitted_instruction[2]]
        return "111" + comp + dest + jump
    else:
        equal_location = Instruction.find("=")
        semicolon_location = Instruction.find(";")
        if equal_location == -1:  # Missing destination
            comp = CompAndJumpDict[splitted_instruction[0]]
            jump = CompAndJumpDict[splitted_instruction[1]]
            dest = "000"
            return "111" + comp + dest + jump
        if semicolon_location == -1:  # Missing Jump
            dest = DestDict[splitted_instruction[0]]
            comp = CompAndJumpDict[splitted_instruction[1]]
            jump = "000"
            return "111" + comp + dest + jump


def AInstructionHandler(Instruction):
    if Instruction[1:] not in SymbolsDict:  # If not a symbol.
        return format(int(Instruction[1:]), "016b")
    else:
        return format(int(SymbolsDict[Instruction[1:]]), '016b')


def Parser(file_name):
    global SymbolsDict
    register_location = 16
    with open(file_name) as Labelpass:
        line_number = 0
        for line in Labelpass.readlines():
            line_instruction = line.split('//')[0].strip()
            if line_instruction:                   # Valid Instruction
                if line_instruction.startswith('('):  # Label
                    Label = line_instruction.strip('()')
                    SymbolsDict[Label] = str(line_number)
                if not line_instruction.count('('):
                    line_number += 1

    with open(file_name) as Symbolpass:
        for line in Symbolpass.readlines():
            line_instruction = line.split('//')[0].strip()
            if line_instruction:
                if line_instruction.startswith('@') and not line_instruction[1:].isdigit():  # Possible Symbol
                    if line_instruction[1:] not in SymbolsDict:
                        SymbolsDict[line_instruction[1:]] = str(register_location)
                        register_location += 1

    with open(file_name) as f, open(file_name.replace('asm', 'hack'), 'w') as writer:
        for line in f.readlines():
            line_instruction = line.split("//")[0].strip()
            if line_instruction:
                if line_instruction.startswith("@"):  # A-Instruction
                    writer.write(AInstructionHandler(line_instruction) + "\n")
                elif not line_instruction.count('('):  # Neither A-Instruction nor Label
                    writer.write(CInstructionHandler(line_instruction) + "\n")


def main():
    Parser(sys.argv[1])


if __name__ == "__main__":
    main()
