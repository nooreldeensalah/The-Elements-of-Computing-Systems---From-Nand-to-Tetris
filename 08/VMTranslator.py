from sys import argv
from os.path import isfile
from os import listdir

input_arg = argv[1]
output_file = input_arg.strip(".vm") + ".asm"
stripped_name = input_arg.split("/")[-1].strip(".vm")
arithmetic_operands = ["add", "sub", "and", "or", "neg", "not", "lt", "gt", "eq"]
segment_map = {"this": "THIS", "that": "THAT", "argument": "ARG", "local": "LCL"}
label = 0


def append_newline(Lines):
    return list(map(lambda x: x + "\n", Lines))


def CommandType(command):
    if command.startswith("push"):
        return "push"
    elif command.startswith("pop"):
        return "pop"
    elif command in arithmetic_operands:
        return "arithmetic"
    elif command.startswith("label"):
        return "label"
    elif command.startswith("goto"):
        return "goto"
    elif command.startswith("if"):
        return "if"
    elif command.startswith("call"):
        return "call"
    elif command.startswith("function"):
        return "function"
    elif command.startswith("return"):
        return "return"


def write_label(label):
    pass


def write_goto(label):
    pass


def write_if(label):
    pass


def write_return():
    pass


def write_call(function_name, num_args):
    pass


def write_function(function_name, num_locals):
    pass


def WriteSegments(command, segment, index):
    if CommandType(command) == "push":
        if segment == "constant":
            Lines = [
                f"// {command}",
                f"@{index}",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]
            return append_newline(Lines)
        elif segment == "static":
            Lines = [
                f"// {command}",
                f"@{stripped_name}.{index}",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]
            return append_newline(Lines)
        elif segment == "temp":
            Lines = [
                f"// {command}",
                "@5",
                "D=A",
                f"@{index}",
                "D=D+A",
                "A=D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]
            return append_newline(Lines)
        elif segment == "pointer":
            if index == "0":
                Lines = [
                    f"// {command}",
                    "@THIS",
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1",
                ]
                return append_newline(Lines)
            elif index == "1":
                Lines = [
                    f"// {command}",
                    "@THAT",
                    "D=M",
                    "@SP",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1",
                ]
                return append_newline(Lines)
        elif segment in segment_map:
            Lines = [
                f"// {command}",
                f"@{segment_map[segment]}",
                "D=M",
                f"@{index}",
                "D=D+A",
                "A=D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]
            return append_newline(Lines)
    elif CommandType(command) == "pop":
        if segment == "static":
            Lines = [
                f"// {command}",
                "@SP",
                "M=M-1",
                "@SP",
                "A=M",
                "D=M",
                f"@{stripped_name}.{index}",
                "M=D",
            ]
            return append_newline(Lines)
        elif segment == "temp":
            Lines = [
                f"// {command}",
                "@SP",
                "M=M-1",
                f"@{index}",
                "D=A",
                "@5",
                "D=D+A",
                "@R13",
                "M=D",
                "@SP",
                "A=M",
                "D=M",
                "@R13",
                "A=M",
                "M=D",
            ]
            return append_newline(Lines)
        elif segment == "pointer":
            if index == "0":
                Lines = [
                    f"// {command}",
                    "@SP",
                    "M=M-1",
                    "@SP",
                    "A=M",
                    "D=M",
                    "@THIS",
                    "M=D",
                ]
                return append_newline(Lines)
            if index == "1":
                Lines = [
                    f"// {command}",
                    "@SP",
                    "M=M-1",
                    "@SP",
                    "A=M",
                    "D=M",
                    "@THAT",
                    "M=D",
                ]
                return append_newline(Lines)

        elif segment in segment_map:
            Lines = [
                f"// {command}",
                "@SP",
                "M=M-1",
                f"@{segment_map[segment]}",
                "D=M",
                f"@{index}",
                "D=D+A",
                "@R13",
                "M=D",
                "@SP",
                "A=M",
                "D=M",
                "@R13",
                "A=M",
                "M=D",
            ]
            return append_newline(Lines)


def WriteArithmetic(command):
    global label
    pop_two = [
        f"// {command}",
        "@SP",
        "M=M-1",
        "@SP",
        "A=M",
        "D=M",
        "@R13",
        "M=D",
        "@SP",
        "M=M-1",
        "@SP",
        "A=M",
        "D=M",
        "@R14",
        "M=D",
    ]
    pop_one = pop_two[:8]
    if command == "add":
        Lines = pop_two + [
            "@R13",
            "D=M",
            "@R14",
            "D=M+D",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]
        return append_newline(Lines)
    elif command == "sub":
        Lines = pop_two + [
            "@R13",
            "D=M",
            "@R14",
            "D=M-D",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]
        return append_newline(Lines)
    elif command == "or":
        Lines = pop_two + [
            "@R13",
            "D=M",
            "@R14",
            "D=M|D",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]
        return append_newline(Lines)
    elif command == "and":
        Lines = pop_two + [
            "@R13",
            "D=M",
            "@R14",
            "D=M&D",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]
        return append_newline(Lines)
    elif command == "neg":
        Lines = pop_one + ["@R13", "D=-M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        return append_newline(Lines)
    elif command == "not":
        Lines = pop_one + ["@R13", "D=!M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        return append_newline(Lines)
    elif command == "eq":
        Lines = pop_two + [
            "@R13",
            "D=M",
            "@R14",
            "D=M-D",
            f"@True.{label}",
            "D;JEQ",
            f"@False.{label}",
            "D;JNE",
            f"(True.{label})",
            "@SP",
            "A=M",
            "M=-1",
            "@SP",
            "M=M+1",
            f"@Skip.{label}",
            "0;JMP",
            f"(False.{label})",
            "@SP",
            "A=M",
            "M=0",
            "@SP",
            "M=M+1",
            f"(Skip.{label})",
        ]
        label += 1
        return append_newline(Lines)
    elif command == "lt":
        Lines = pop_two + [
            "@R13",
            "D=M",
            "@R14",
            "D=M-D",
            f"@True.{label}",
            "D;JLT",
            f"@False.{label}",
            "D;JGE",
            f"(True.{label})",
            "@SP",
            "A=M",
            "M=-1",
            "@SP",
            "M=M+1",
            f"@Skip.{label}",
            "0;JMP",
            f"(False.{label})",
            "@SP",
            "A=M",
            "M=0",
            "@SP",
            "M=M+1",
            f"(Skip.{label})",
        ]
        label += 1
        return append_newline(Lines)
    elif command == "gt":
        Lines = pop_two + [
            "@R13",
            "D=M",
            "@R14",
            "D=M-D",
            f"@True.{label}",
            "D;JGT",
            f"@False.{label}",
            "D;JLE",
            f"(True.{label})",
            "@SP",
            "A=M",
            "M=-1",
            "@SP",
            "M=M+1",
            f"@Skip.{label}",
            "0;JMP",
            f"(False.{label})",
            "@SP",
            "A=M",
            "M=0",
            "@SP",
            "M=M+1",
            f"(Skip.{label})",
        ]
        label += 1
        return append_newline(Lines)


def Parser(*files):
    for file in files:
        with open(file, "r") as reader, open(output_file, "a") as writer:
            for line in reader.readlines():
                command = line.split("//")[0].strip()
                if command:
                    if CommandType(command) == "push" or CommandType(command) == "pop":
                        segment = command.split()[1]
                        index = command.split()[2]
                        writer.writelines(WriteSegments(command, segment, index))
                    elif CommandType(command) == "arithmetic":
                        writer.writelines(WriteArithmetic(command))
                    elif CommandType(command) == "label":
                        writer.writelines(write_label(command))
                    elif CommandType(command) == "goto":
                        writer.writelines(write_goto(command))
                    elif CommandType(command) == "if":
                        writer.writelines(write_if(command))
                    elif CommandType(command) == "function":
                        writer.writelines(write_function(command))
                    elif CommandType(command) == "call":
                        writer.writelines(write_call(command))
                    elif CommandType(command) == "return":
                        writer.writelines(write_return(command))


def main():
    if isfile(input_arg):
        Parser(input_arg)
    else:
        vm_files = list(filter(lambda x: x.endswith("vm"), listdir(input_arg)))
        Parser(vm_files)


if __name__ == "__main__":
    main()
