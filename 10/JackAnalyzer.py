from sys import argv
from os.path import isfile
from os import listdir
import re

token_index = 0
input_arg = argv[1]
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
    "&amp;",
    ",",
    "&lt;",
    "&gt;",
    "=",
    "~",
    "|",
]
symbols_markup = {"<": "&lt;", ">": "&gt;", '"': "&quot;", "&": "&amp;"}
symbolspattern = re.compile(r"[);\[\]\.,~(-]")


def JackTokenizer(input_file):
    stringflag = 0
    string_holder = ""
    tokens_list = list()
    reader = open(input_file)
    for line in reader.readlines():
        stripped_line = re.split("\/(\/|\*)|^\s?\*", line)[0].strip()
        if stripped_line:
            for code_line in stripped_line.split():
                stripped_code = list(re.sub(symbolspattern, " ", code_line))
                for match in re.finditer(symbolspattern, code_line):
                    stripped_code[match.start()] = " " + match.group() + " "
                for token in "".join(stripped_code).split():
                    if token in symbols_markup:
                        tokens_list.append(symbols_markup[token])
                    elif token.count('"') | stringflag == 1:
                        if stringflag == 0:
                            string_holder += token.strip('"')
                        else:
                            string_holder += " " + token.strip('"')
                        if token.count('"'):
                            stringflag += 1
                        if stringflag == 2:
                            tokens_list.append(string_holder)
                            string_holder = ""
                            stringflag = 0
                    else:
                        tokens_list.append(token)
    reader.close()
    return tokens_list


class CompilationEngine:
    def __init__(self, tokens, output_file):
        self.tokens = tokens
        self.token_index = 0
        self.output_file = output_file

    def compile_class(self):
        pass

    def compile_class_var_decs(self):
        pass

    def compile_subroutine_dec(self):
        pass

    def compile_paramaters(self):
        pass

    def compile_var_dec(self):
        pass

    def compile_statements(self):
        pass

    def compile_let(self):
        pass

    def compile_if(self):
        pass

    def compile_while(self):
        pass

    def compile_do(self):
        pass

    def compile_return(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self):
        pass


def JackAnalyzer():
    if isfile(input_arg):
        tokens = JackTokenizer(input_arg)
        output_file = input_arg.replace("jack", "xml")
        output_file = open(output_file, "w")
        CompilationEngine(tokens, output_file)
        output_file.close()
    else:
        jack_files = list(filter(lambda x: x.endswith("jack"), listdir(input_arg)))
        for file in jack_files:
            tokens = JackTokenizer(file)
            output_file = file.replace("jack", "xml")
            output_file = open(output_file, "w")
            CompilationEngine(tokens, output_file)
            output_file.close()


if __name__ == "__main__":
    JackAnalyzer()
