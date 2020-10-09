from sys import argv
from os.path import isfile
from os import listdir
import re

stringflag = 0
string_holder = ""
input_arg = "./Main.jack"
keywords = [
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
]
symbols = [
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    ".",
    ",",
    ";",
    "+",
    "-",
    "*",
    "/",
    "&",
    ",",
    "<",
    ">",
    "=",
    "~",
    "|"
]
symbols_markup = {"<": "&lt;", ">": "&gt;", '"': "&quot;", "&": "&amp;"}
symbolspattern = re.compile(r'[);\[\]\.,~(-]', re.UNICODE)


def JackTokenizer(input_file):   
    global stringflag
    global string_holder
    output_file = './test.xml'
    with open(input_file) as reader, open(output_file, "w") as writer:
        writer.write("<tokens>\n")
        for line in reader.readlines():
            stripped_line = re.split('\/(\/|\*)|^\s?\*', line)[0].strip()
            if stripped_line:
                for code_line in stripped_line.split():
                    stripped_code = list(re.sub(symbolspattern, " ", code_line))
                    for match in re.finditer(symbolspattern, code_line):
                        stripped_code[match.start()] = " " + match.group() + " "
                    for token in "".join(stripped_code).split():
                        if token in keywords:
                            writer.write(f"<keyword> {token} </keyword>\n")
                        elif token in symbols:
                            if token in symbols_markup:
                                writer.write(f"<symbol> {symbols_markup[token]} </symbol>\n")
                            else:
                                writer.write(f"<symbol> {token} </symbol>\n") 
                        elif token.isnumeric():
                            writer.write(f"<integerConstant> {token} </integerConstant>\n")
                        elif token.count('"') | stringflag == 1:
                            if stringflag == 0:
                                string_holder += token.strip('"')
                            else:
                                string_holder += " " + token.strip('"')
                            if token.count('"'):
                                stringflag += 1
                            if stringflag == 2:
                                writer.write(f"<stringConstant> {string_holder} </stringConstant>\n")
                                string_holder = ""
                                stringflag = 0
                        else:
                            writer.write(f"<identifier> {token} </identifier>\n")
        writer.write("</tokens>")


def CompilationEngine():
    pass


def main():
    JackTokenizer(input_arg)

main()
if __name__ == "__main__":
    main()
