from sys import argv
from os.path import isfile
from os import listdir

input_arg = argv[1]
output_file = input_arg.strip(".vm") + ".asm"
stripped_name = input_arg.split("/")[-1].strip(".vm")
arithmetic_operands = ["add", "sub", "and", "or", "neg", "not", "lt", "gt", "eq"]
segment_map = {"this": "THIS", "that": "THAT", "argument": "ARG", "local": "LCL"}
label = 0
function_name = "null"


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
    label_tag = label[6:]
    Lines = [f"// {label}", f"({function_name}${label_tag})"]
    return append_newline(Lines)


def write_goto(label):
    label_tag = label[5:]
    Lines = [f"// {label}", f"@{function_name}${label_tag}", "0;JMP"]
    return append_newline(Lines)


def write_if(label):
    label_tag = label[8:]
    Lines = [
        f"// {label}",
        "@SP",
        "M=M-1",
        "@SP",
        "A=M",
        "D=M",
        f"@{function_name}${label_tag}",
        "D;JNE",
    ]
    return append_newline(Lines)


def write_return():
    Lines = [
        f"// {label}",
        "@LCL",
        "D=M",
        "@R13",  # EndFrame
        "M=D",
        "@5",
        "D=D-A",
        "A=D",
        "D=M",
        "@R14",  # RET
        "M=D",
        "@SP",
        "M=M-1",
        "@SP",
        "A=M",
        "D=M",
        "@ARG",
        "A=M",
        "M=D",
        "@ARG",
        "D=M",
        "@SP",
        "M=D+1",
        "@R13",
        "D=M",
        "@1",
        "D=D-A",
        "A=D",
        "D=M",
        "@THAT",
        "M=D",
        "@R13",
        "D=M",
        "@2",
        "D=D-A",
        "A=D",
        "D=M",
        "@THIS",
        "M=D",
        "@R13",
        "D=M",
        "@3",
        "D=D-A",
        "A=D",
        "D=M",
        "@ARG",
        "M=D",
        "@R13",
        "D=M",
        "@4",
        "D=D-A",
        "A=D",
        "D=M",
        "@LCL",
        "M=D",
        "@R14",
        "0;JMP",
    ]
    return append_newline(Lines)


def write_call(command):
    global function_name
    num_args = int(command[-1])
    function_name = command.split()[1]
    Lines = [
        f"// {label}",
        "" "@LCL",  # TODO: push return-address  # Push LCL
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@ARG",  # Push ARG
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@THIS",  # Push THIS
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@THAT",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "D=M",
        "@5" "D=D-A",
        f"@{num_args}",
        "D=D-A",
        "@ARG",
        "M=D",
        "@SP",
        "D=M",
        "@LCL",
        "M=D",
        "@{function_name}",
        "0;JMP",
        # TODO: (return-address)
    ]


def write_function(command):
    global function_name
    local_vars_num = int(command[-1])
    function_name = command.split()[1]
    Lines = [
        f"// {command}",
        f"({function_name})",
        f"@{local_vars_num}",
        "D=A",
        "@R13",
        "M=D",
        f"({function_name}$push_zeroes)",
        "@SP",
        "A=M",
        "M=0",
        "@SP",
        "M=M+1",
        "@R13",
        "M=M-1",
        "D=M",
        f"@{function_name}$push_zeroes",
        "D;JGT",
    ]
    return append_newline(Lines)


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
                        writer.writelines(write_return())


def main():
    if isfile(input_arg):
        Parser(input_arg)
    else:
        vm_files = list(filter(lambda x: x.endswith("vm"), listdir(input_arg)))
        Parser(vm_files)


if __name__ == "__main__":
    main()
