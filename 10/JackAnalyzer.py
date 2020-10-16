from sys import argv
from os.path import isfile
from os import listdir
import re

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
    "&",
    "|",
    "<",
    ">",
    "=",
    "~",
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
                    if token in keywords:
                        tokens_list.append((token, "keyword"))
                    elif token in symbols:
                        if token in symbols_markup:
                            tokens_list.append((symbols_markup[token], "symbol"))
                        else:
                            tokens_list.append((token, "symbol"))
                    elif token.isnumeric():
                        tokens_list.append((token, "integerConstant"))
                    elif token.count('"') | stringflag == 1:
                        if stringflag == 0:
                            string_holder += token.strip('"')
                        else:
                            string_holder += " " + token.strip('"')
                        if token.count('"'):
                            stringflag += 1
                        if stringflag == 2:
                            tokens_list.append((string_holder, "stringConstant"))
                            string_holder = ""
                            stringflag = 0
                    else:
                        tokens_list.append((token, "identifier"))
    reader.close()
    return tokens_list


class CompilationEngine:
    TERMINAL_TOKEN_TYPES = ["stringConstant", "integerConstant", "identifier", "symbol"]
    TERMINAL_KEYWORDS = ["boolean", "class", "void", "int"]
    CLASS_VAR_DEC_TOKENS = ["static", "field"]
    SUBROUTINE_TOKENS = ["function", "method", "constructor"]
    STATEMENT_TOKENS = ["do", "let", "while", "return", "if"]
    STARTING_TOKENS = {
        "var_dec": "var",
        "parameter_list": "(",
        "subroutine_body": "{",
        "expression_list": "(",
        "expression": ["=", "[", "("],
    }
    TERMINATING_TOKENS = {
        "class": "}",
        "class_var_dec": ";",
        "subroutine": "}",
        "parameter_list": ")",
        "expression_list": ")",
        "statements": "}",
        "do": ";",
        "let": ";",
        "while": "}",
        "if": "}",
        "var_dec": ";",
        "return": ";",
        "expression": [";", ")", "]", ","],
    }
    OPERATORS = ["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="]
    UNARY_OPERATORS = ["-", "~"]

    def __init__(self, tokens, output_file):
        self.tokens = tokens
        self.token_index = -1
        self.output_file = output_file

    def compile_class(self):
        self.xml_tag_writer('class')
        while self.has_more_tokens():
            self.advance()
            if self.current_token_type() in self.TERMINAL_TOKEN_TYPES or self.current_token() in self.TERMINAL_KEYWORDS:
                self.xml_token_writer()
            elif self.current_token() in self.CLASS_VAR_DEC_TOKENS:
                self.compile_class_var_decs()
            elif self.current_token() in self.SUBROUTINE_TOKENS:
                self.compile_subroutine_dec()
        self.xml_tag_writer('/class')

    def compile_class_var_decs(self):
        self.xml_tag_writer('classVarDec')
        self.xml_token_writer()
        while self.current_token() != self.TERMINATING_TOKENS['class_var_dec']:
            self.advance()
            self.xml_token_writer()
        self.xml_tag_writer('/classVarDec')

    def compile_subroutine_dec(self):
        self.xml_tag_writer('subroutineDec')
        self.xml_token_writer()
        while self.current_token() != self.TERMINATING_TOKENS['subroutine']:
            self.advance()

            if self.current_token() == self.STARTING_TOKENS['parameter_list']:
                self.compile_paramater_list()
            elif self.current_token() == self.STARTING_TOKENS['subroutine_body']:
                self.compile_subroutine_body()
            else:
                self.xml_token_writer()

        self.xml_tag_writer('/subroutineDec')

    def compile_paramater_list(self):
        self.xml_token_writer()
        self.xml_tag_writer('parameterList')
        while not self.tokens[self.token_index + 1][0] == self.TERMINATING_TOKENS['parameter_list']:
            self.advance()
            self.xml_token_writer()
        self.xml_tag_writer('/parameterList')

        self.advance()
        self.xml_token_writer()

    def compile_subroutine_body(self):
        self.xml_tag_writer('subroutineBody')
        self.xml_token_writer()
        while not self.current_token() == self.TERMINATING_TOKENS['subroutine']:
            self.advance()
            if self.current_token() == self.STARTING_TOKENS['var_dec']:
                self.compile_var_dec()
            elif self.current_token() in self.STATEMENT_TOKENS:
                self.compile_statements()
            else:
                self.xml_token_writer()
        self.xml_token_writer()
        self.xml_tag_writer('/subroutineBody')
        
    def compile_var_dec(self):
        self.xml_tag_writer('varDec')
        self.xml_token_writer()
        while not self.current_token() == self.TERMINATING_TOKENS['var_dec']:
            self.advance()
            self.xml_token_writer()
        self.xml_tag_writer('/varDec')

    def compile_statements(self):
        self.xml_tag_writer('statements')
        while not self.current_token() == self.TERMINATING_TOKENS['subroutine']:
            if self.current_token() == 'if':
                self.compile_if()
            elif self.current_token() == 'do':
                self.compile_do()
            elif self.current_token() == 'let':
                self.compile_let()
            elif self.current_token() == 'while':
                self.compile_while()
            elif self.current_token() == 'return':
                self.compile_return()
            self.advance()
        self.xml_tag_writer('/statements')

    def compile_let(self):
        self.xml_tag_writer('letStatement')
        self.xml_token_writer()
        while not self.current_token() == self.TERMINATING_TOKENS['let']:
            self.advance()
            if self.current_token() in self.STARTING_TOKENS['expression']:
                self.xml_token_writer()
                self.compile_expression()
            else:
                self.xml_token_writer()
        self.xml_tag_writer('/letStatement')

    def compile_if(self):
        self.xml_tag_writer('ifStatement')
        self.xml_token_writer()
        self.advance()
        self.xml_token_writer()
        self.compile_expression()
        while not self.current_token() == self.TERMINATING_TOKENS['if']:
            self.advance()
            if self.current_token() in self.STATEMENT_TOKENS:
                self.compile_statements()
            else:
                self.xml_token_writer()
        if self.tokens[self.token_index + 1][0] == 'else':
            self.xml_token_writer()
            self.advance()
            self.xml_token_writer()
            while not self.current_token() == self.TERMINATING_TOKENS['if']:
                self.advance()
                if self.current_token() in self.STATEMENT_TOKENS:
                    self.compile_statements()
                else:
                    self.xml_token_writer()
        self.xml_token_writer()
        self.xml_tag_writer('/ifStatement')

    def compile_while(self):
        self.xml_tag_writer('whileStatement')
        self.xml_token_writer()
        self.advance()
        self.xml_token_writer()
        self.compile_expression()
        while not self.current_token() == self.TERMINATING_TOKENS['while']:
            self.advance()
            if self.current_token() in self.STATEMENT_TOKENS:
                self.compile_statements()
            else:
                self.xml_token_writer()  
        self.xml_token_writer()
        self.xml_tag_writer('/whileStatement')

    def compile_do(self):
        self.xml_tag_writer('doStatement')
        self.xml_token_writer()
        while not self.current_token() == self.TERMINATING_TOKENS['do']:
            self.advance()
            if self.current_token() == self.STARTING_TOKENS['expression_list']:
                self.compile_expression_list()
            else:
                self.xml_token_writer()
        self.xml_tag_writer('/doStatement')

    def compile_return(self):
        self.xml_tag_writer('returnStatement')
        self.xml_token_writer()
        if not self.tokens[self.token_index + 1][0] == self.TERMINATING_TOKENS['return']:
            self.compile_expression()
        else:
            self.advance()
            self.xml_token_writer()
        self.xml_tag_writer('/returnStatement')

    def compile_expression(self):
        self.xml_tag_writer('expression')
        if self.current_token() == '(' and self.tokens[self.token_index + 1][0] == '-':
            unary_negative = True
        else:
            unary_negative = False
        self.advance()
        while self.current_token() not in self.TERMINATING_TOKENS['expression']:
            if self.current_token() in self.OPERATORS and not unary_negative:
                self.xml_token_writer()
                self.advance()
            else:
                self.compile_term()
        self.xml_tag_writer('/expression')
        self.xml_token_writer()

    def compile_expression_in_expression_list(self):
        self.xml_tag_writer('expression')
        while self.current_token() not in self.TERMINATING_TOKENS['expression']:
            if self.current_token() == ',':
                self.advance()
            if self.current_token() in self.OPERATORS:
                self.xml_token_writer()
                self.advance()
            else:
                self.compile_term()
        self.xml_tag_writer('/expression')
        if self.current_token() == ',':
            self.xml_token_writer()
            self.advance()

    def compile_term(self):
        self.xml_tag_writer('term')
        while self.current_token() not in self.TERMINATING_TOKENS['expression']:
            if self.current_token() == self.STARTING_TOKENS['expression_list']:
                if self.tokens[self.token_index - 2][0] == '.':
                    self.compile_expression_list()
                else:
                    self.xml_token_writer()
                    self.compile_expression()
            elif self.current_token() in self.STARTING_TOKENS['expression']:
                self.xml_token_writer()
                self.compile_expression()
            elif self.current_token() in self.UNARY_OPERATORS:
                self.xml_token_writer()
                if self.tokens[self.token_index + 1][0] in self.STARTING_TOKENS['expression']:
                    self.advance()
                    self.compile_term()
                    break
                else:
                    self.advance()
                    self.xml_tag_writer('term')
                    self.xml_token_writer()
                    self.xml_tag_writer('/term')
            else:
                self.xml_token_writer()
            
            if self.tokens[self.token_index + 1][0] in self.OPERATORS and self.current_token() != '(':
                self.advance()
                break
            self.advance()
        self.xml_tag_writer('/term')

    def compile_expression_list(self):
        self.xml_token_writer()
        self.xml_tag_writer('expressionList')
        self.advance()
        if not self.current_token() == self.TERMINATING_TOKENS['expression_list']:
            while not self.current_token() == self.TERMINATING_TOKENS['expression_list']:
                self.compile_expression_in_expression_list()
        self.xml_tag_writer('/expressionList')
        self.xml_token_writer()

    def current_token(self):
        return self.tokens[self.token_index][0]

    def advance(self):
        if self.has_more_tokens():
            self.token_index += 1

    def current_token_type(self):
        return self.tokens[self.token_index][1]

    def xml_tag_writer(self, tag):
        self.output_file.write(f"<{tag}>\n")

    def xml_token_writer(self):
        tag_name = self.current_token_type()
        token_name = self.current_token()
        self.output_file.write(f"<{tag_name}> {token_name} </{tag_name}>\n")

    def has_more_tokens(self):
        return self.token_index < len(self.tokens) - 1


def JackAnalyzer():
    if isfile(input_arg):
        tokens = JackTokenizer(input_arg)
        output_file = input_arg.replace("jack", "xml")
        output_file = open(output_file, "w")
        CompilationEngine(tokens, output_file).compile_class()
        output_file.close()
    else:
        jack_files = list(filter(lambda x: x.endswith("jack"), listdir(input_arg)))
        jack_files = map(lambda x: f'./{input_arg}/' + x, jack_files)
        for file in jack_files:
            tokens = JackTokenizer(file)
            output_file = file.replace("jack", "xml")
            output_file = open(output_file, "w")
            CompilationEngine(tokens, output_file).compile_class()
            output_file.close()


if __name__ == "__main__":
    JackAnalyzer()
