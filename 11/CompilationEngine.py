class LabelCounter:
    def __init__(self, labels):
        self.labels = labels
        self.counts = {}
        self._initialize_counts()

    def increment(self, label):
        self.counts[label] += 1

    def decrement(self, label):
        self.counts[label] -= 1

    def get(self, label):
        return self.counts[label]

    def reset_counts(self):
        self._initialize_counts()

    def _initialize_counts(self):
        for label in self.labels:
            self.counts[label] = 0


class JackToken:
    KEYWORD_TOKENS = [
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
    CLASS_VAR_DEC_TOKENS = ["static", "field"]
    SUBROUTINE_TOKENS = ["function", "method", "constructor"]
    STATEMENT_TOKENS = ["do", "let", "while", "return", "if"]
    OPERATORS = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
    UNARY_OPERATORS = ["-", "~"]
    TOKENS_THAT_NEED_LABELS = ["if", "while"]

    def __init__(self, text):
        self.text = text

    def token_type(self):
        if not self.text:
            return None
        elif self.text[0] == '"':
            return "STRING_CONST"
        elif self.text in self.KEYWORD_TOKENS:
            return "KEYWORD"
        elif self.text.isnumeric():
            return "INT_CONST"
        elif self.text.isalnum():
            return "IDENTIFIER"
        else:
            return "SYMBOL"

    def is_expression_list_delimiter(self):
        return self.text == ","

    def is_expression_list_starter(self):
        return self.text == "("

    def is_subroutine_call_delimiter(self):
        return self.text == "."

    def is_unary_operator(self):
        return self.text in self.UNARY_OPERATORS

    def is_operator(self):
        return self.text in self.OPERATORS

    def is_if(self):
        return self.text == "if"

    def is_statement_token(self):
        return self.text in self.STATEMENT_TOKENS

    def starts_class_var_dec(self):
        return self.text in self.CLASS_VAR_DEC_TOKENS

    def starts_subroutine(self):
        return self.text in self.SUBROUTINE_TOKENS

    def is_class(self):
        return self.text == "class"

    def is_string_const(self):
        return self.token_type() == "STRING_CONST"

    def is_identifier(self):
        return self.token_type() == "IDENTIFIER"

    def is_keyword(self):
        return self.token_type() == "KEYWORD"

    def is_boolean(self):
        return self.text in ["true", "false"]

    def is_null(self):
        return self.text == "null"

    def is_empty(self):
        return len(self.text) == 0


class JackTokenizer:
    COMMENT_OPERATORS = ["/", "*"]
    STRING_CONST_DELIMITER = '"'

    def __init__(self, input_file):
        self.input_file = input_file
        self.tokens_found = []
        self.current_token = None
        self.next_token = None
        self.has_more_tokens = True

    def advance(self):
        # initialize char
        char = self.input_file.read(1)
        # skip whitespace and comments
        char = self._skip_whitespace_and_comments(starting_char=char)

        # get token
        if self._is_string_const_delimeter(char):
            token = JackToken(self._get_string_const(starting_char=char))
        elif char.isalnum():
            token = JackToken(self._get_alnum_underscore(starting_char=char))
        else:  # symbol
            token = JackToken(char)

        # set tokens
        if self.current_token:
            self.current_token = self.next_token
            self.next_token = token
            self.tokens_found.append(token)
        else:  # initial setup
            self.current_token = token
            self.next_token = token
            self.tokens_found.append(token)
            # get next token
            self.advance()

        if self.current_token.is_empty():
            self.has_more_tokens = False

    def class_token_reached(self):
        if not self.current_token:
            return False
        else:
            return self.current_token.is_class()

    def null(self):
        if self.current_token.is_null():
            return self.current_token.text

    def boolean(self):
        if self.current_token.is_boolean():
            return self.current_token.text

    def keyword(self):
        if self.current_token.is_keyword():
            return self.current_token.text

    def identifier(self):
        if self.current_token.is_identifier():
            return self.current_token.text

    def string_const(self):
        if self.current_token.is_string_const():
            # remove " that denote string const
            return self.current_token.text.replace('"', "")

    def part_of_expression_list(self):
        if len(self.tokens_found) < 3:
            return False

        past_token = self.tokens_found[-3]
        return (
            past_token.is_expression_list_delimiter()
            or past_token.is_expression_list_starter()
        )

    def _get_alnum_underscore(self, starting_char):
        token = ""
        char = starting_char
        # get rest of token
        while self._is_alnum_or_underscore(char):
            # keep track of what was last read
            last_pos = self.input_file.tell()
            token += char
            char = self.input_file.read(1)
        self.input_file.seek(last_pos)
        return token

    def _get_string_const(self, starting_char):
        char = starting_char
        token = ""

        # add initial "
        token += char
        char = self.input_file.read(1)

        # get rest of token up to ending "
        while not self._is_string_const_delimeter(char):
            token += char
            char = self.input_file.read(1)

        # get last "
        token += char
        return token

    def _skip_whitespace_and_comments(self, starting_char):
        char = starting_char

        while char.isspace() or char in self.COMMENT_OPERATORS:
            if char.isspace():
                # read 1 char bc we don't know what's next
                char = self.input_file.read(1)
            elif char in self.COMMENT_OPERATORS:
                # make sure comment and not operator
                last_pos = self.input_file.tell()
                # read rest of line
                rest_of_line = self.input_file.readline()
                if not self._is_start_of_comment(char, rest_of_line):
                    # go back
                    self.input_file.seek(last_pos)
                    # no whitespace / comments left to parse
                    break
                else:
                    # read next char
                    char = self.input_file.read(1)
            continue
        return char

    def _is_alnum_or_underscore(self, char):
        return char.isalnum() or char == "_"

    def _is_string_const_delimeter(self, char):
        return char == '"'

    def _is_start_of_comment(self, char, rest_of_line):
        # comment of form: // or */
        single_line_comment = rest_of_line[0] == self.COMMENT_OPERATORS[0]
        # comment of form: /**
        multi_line_comment = (
            char == self.COMMENT_OPERATORS[0] and rest_of_line[0:2] == "**"
        )
        # comment of form:  * comment
        part_of_multi_line_comment = self._part_of_multiline_comment()
        return single_line_comment or multi_line_comment or part_of_multi_line_comment

    def _part_of_multiline_comment(self):
        if not self.tokens_found:
            return True
        elif self.tokens_found[-1] == ";":
            return True
        else:
            return False


class VMWriter:
    ARITHMETIC_LOGICAL_OPERATORS = {
        "+": "add",
        "-": "sub",
        "=": "eq",
        ">": "gt",
        "<": "lt",
        "&": "and",
        "|": "or",
    }
    UNARY_OPERATORS = {"-": "neg", "~": "not"}

    def __init__(self, output_file):
        """
        creates a new .vm file and prepares it for writing
        """
        self.output_file = output_file

    def write_push(self, segment, index):
        """
        writes a vm push command
        segment options: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
        index: int
        """
        self.output_file.write("push {} {}\n".format(segment, index))

    def write_pop(self, segment, index):
        """
        writes a vm pop command
        segments: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
        index: int
        """
        self.output_file.write("pop {} {}\n".format(segment, index))

    def write_arithmetic(self, command):
        """
        writes a vm arithmetic-logical command
        commands: ADD, SUB, EQ, GT, LT, AND, OR
        """
        self.output_file.write(
            "{}\n".format(self.ARITHMETIC_LOGICAL_OPERATORS[command])
        )

    def write_unary(self, command):
        """
        writes a vm unary command
        commands: NEG, NOT
        """
        self.output_file.write("{}\n".format(self.UNARY_OPERATORS[command]))

    def write_label(self, label):
        """
        writes a VM label comand
        label: string
        """
        self.output_file.write("label {}\n".format(label))

    def write_goto(self, label):
        self.output_file.write("goto {}\n".format(label))

    def write_ifgoto(self, label):
        self.output_file.write("if-goto {}\n".format(label))

    def write_call(self, name, num_args):
        self.output_file.write("call {} {}\n".format(name, num_args))

    def write_function(self, name, num_locals):
        """
        writes a VM call command
        name: string, name of subroutine
        num_locals: int, number of locals for function
        """
        self.output_file.write("function {} {}\n".format(name, num_locals))

    def write_return(self):
        self.output_file.write("return\n")


class SymbolTable:
    def __init__(self):
        self.symbols = []

    def reset(self):
        self.symbols = []

    def define(self, name, symbol_type, kind):
        new_symbol = {
            "name": name,
            "type": symbol_type,
            "kind": kind,
            "index": self.var_count(kind),
        }
        self.symbols.append(new_symbol)

    def var_count(self, kind):
        return sum(symbol["kind"] == kind for symbol in self.symbols)

    def kind_of(self, name):
        return self.find_symbol_by_name(name).get("kind")

    def type_of(self, name):
        return self.find_symbol_by_name(name).get("type")

    def index_of(self, name):
        return self.find_symbol_by_name(name).get("index")

    def find_symbol_by_name(self, value):
        for symbol in self.symbols:
            if symbol["name"] == value:
                return symbol


class Operator:
    def __init__(self, token, category):
        self.token = token
        self.category = category

    def unary(self):
        return self.category == "unary"

    def multiplication(self):
        return self.token == "*"

    def division(self):
        return self.token == "/"


class CompilationEngine:
    SYMBOL_KINDS = {"parameter_list": "argument", "var_dec": "local"}
    STARTING_TOKENS = {
        "var_dec": ["var"],
        "parameter_list": ["("],
        "subroutine_body": ["{"],
        "expression_list": ["("],
        "expression": ["=", "[", "("],
        "array": ["["],
        "conditional": ["if", "else"],
    }
    TERMINATING_TOKENS = {
        "class": ["}"],
        "class_var_dec": [";"],
        "subroutine": ["}"],
        "parameter_list": [")"],
        "expression_list": [")"],
        "statements": ["}"],
        "do": [";"],
        "let": [";"],
        "while": ["}"],
        "if": ["}"],
        "var_dec": [";"],
        "return": [";"],
        "expression": [";", ")", "]", ","],
        "array": ["]"],
    }
    TOKENS_THAT_NEED_LABELS = ["if", "while"]

    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = output_file
        self.class_symbol_table = SymbolTable()
        self.subroutine_symbol_table = SymbolTable()
        self.vm_writer = VMWriter(output_file)
        self.label_counter = LabelCounter(labels=self.TOKENS_THAT_NEED_LABELS)
        self.class_name = None

    def compile_class(self):
        # skip everything up to class start
        while not self.tokenizer.class_token_reached():
            self.tokenizer.advance()
        # since compilation unit is a class makes sense to store this as instance variable
        self.class_name = self.tokenizer.next_token.text

        while self.tokenizer.has_more_tokens:
            self.tokenizer.advance()

            if self.tokenizer.current_token.starts_class_var_dec():
                self.compile_class_var_dec()
            elif self.tokenizer.current_token.starts_subroutine():
                self.compile_subroutine()

    def compile_class_var_dec(self):
        symbol_kind = self.tokenizer.keyword()

        # get symbol type
        self.tokenizer.advance()
        symbol_type = self.tokenizer.keyword()

        # get all identifiers
        while self._not_terminal_token_for("class_var_dec"):
            self.tokenizer.advance()

            if self.tokenizer.identifier():
                # add symbol to class
                symbol_name = self.tokenizer.identifier()
                self.class_symbol_table.define(
                    name=symbol_name, kind=symbol_kind, symbol_type=symbol_type
                )

    def compile_subroutine(self):
        # new subroutine means new subroutine scope
        self.subroutine_symbol_table.reset()

        # get subroutine name
        self.tokenizer.advance()
        self.tokenizer.advance()
        subroutine_name = self.tokenizer.current_token.text

        # compile parameter list
        self.tokenizer.advance()
        self.compile_parameter_list()

        # compile body
        self.tokenizer.advance()
        self.compile_subroutine_body(subroutine_name=subroutine_name)

        # rest counts from subroutine
        self.label_counter.reset_counts()

    def compile_subroutine_body(self, subroutine_name):
        # skip start
        self.tokenizer.advance()
        # get all locals
        num_locals = 0
        while self._starting_token_for("var_dec"):
            num_locals += self.compile_var_dec()
            self.tokenizer.advance()

        # write function command
        self.vm_writer.write_function(
            name="{}.{}".format(self.class_name, subroutine_name), num_locals=num_locals
        )

        # compile all statements
        while self._not_terminal_token_for("subroutine"):
            self.compile_statements()

    def compile_parameter_list(self):
        ### symbol table
        while self._not_terminal_token_for("parameter_list"):
            self.tokenizer.advance()

            # symbol table
            if self.tokenizer.next_token.is_identifier():
                symbol_kind = self.SYMBOL_KINDS["parameter_list"]
                symbol_type = self.tokenizer.current_token.text
                symbol_name = self.tokenizer.next_token.text
                self.subroutine_symbol_table.define(
                    name=symbol_name, kind=symbol_kind, symbol_type=symbol_type
                )

    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        self.tokenizer.advance()
        symbol_type = self.tokenizer.current_token.text
        num_vars = 0
        while self._not_terminal_token_for("var_dec"):
            self.tokenizer.advance()

            if self.tokenizer.identifier():
                num_vars += 1
                symbol_kind = self.SYMBOL_KINDS["var_dec"]
                symbol_name = self.tokenizer.identifier()
                self.subroutine_symbol_table.define(
                    name=symbol_name, kind=symbol_kind, symbol_type=symbol_type
                )
        return num_vars

    def compile_statements(self):
        statement_compile_methods = {
            "if": self.compile_if,
            "do": self.compile_do,
            "let": self.compile_let,
            "while": self.compile_while,
            "return": self.compile_return,
        }

        while self._not_terminal_token_for("subroutine"):
            if self.tokenizer.current_token.is_statement_token():
                statement_type = self.tokenizer.current_token.text
                statement_compile_methods[statement_type]()

            self.tokenizer.advance()

    def compile_do(self):
        self.tokenizer.advance()
        caller_name = self.tokenizer.current_token.text
        symbol = self._find_symbol_in_symbol_tables(symbol_name=caller_name)
        self.tokenizer.advance()
        self.tokenizer.advance()
        subroutine_name = self.tokenizer.current_token.text

        if symbol:  # user defined Method
            # push value onto local segment
            segment = "local"
            index = symbol["index"]
            symbol_type = symbol["type"]
            self.vm_writer.write_push(segment=segment, index=index)
        else:
            symbol_type = caller_name

        subroutine_call_name = symbol_type + "." + subroutine_name
        self.tokenizer.advance()
        num_args = self.compile_expression_list()
        if symbol:
            # calling object passed as implicit argument
            num_args += 1
        # write call
        self.vm_writer.write_call(name=subroutine_call_name, num_args=num_args)
        # pop off return of previous call we don't care about
        self.vm_writer.write_pop(segment="temp", index="0")

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        """
        example: let direction = 0;
        """
        # get symbol to store expression evaluation
        self.tokenizer.advance()
        symbol_name = self.tokenizer.current_token.text
        symbol = self._find_symbol_in_symbol_tables(symbol_name=symbol_name)

        # array assignment?
        array_assignment = self._starting_token_for(
            keyword_token="array", position="next"
        )
        if array_assignment:
            # get to index expression
            self.tokenizer.advance()
            self.tokenizer.advance()
            # compile it
            self.compile_expression()
            self.vm_writer.write_push(segment=symbol["kind"], index=symbol["index"])
            # add two addresses
            self.vm_writer.write_arithmetic(command="+")

        # go past =
        while not self.tokenizer.current_token.text == "=":
            self.tokenizer.advance()
        # compile all expressions
        while self._not_terminal_token_for("let"):
            self.tokenizer.advance()
            self.compile_expression()

        if not array_assignment:
            # store expression evaluation in symbol location
            self.vm_writer.write_pop(segment=symbol["kind"], index=symbol["index"])
        else:  # array unloading
            # pop return value onto temp
            self.vm_writer.write_pop(segment="temp", index="0")
            # pop address of array slot onto THAT
            self.vm_writer.write_pop(segment="pointer", index="1")  # pointer 1 => array
            # push value on temp back onto stack
            self.vm_writer.write_push(segment="temp", index="0")
            # set that
            self.vm_writer.write_pop(segment="that", index="0")

    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        """
        example: while (x > 0) { ... }
        """
        # write while label
        self.vm_writer.write_label(
            label="WHILE_EXP{}".format(self.label_counter.get("while"))
        )

        # advance to expression start (
        self.tokenizer.advance()
        self.tokenizer.advance()

        # compile expression in ()
        self.compile_expression()

        # NOT expression so for easily handling of termination and if-goto
        self.vm_writer.write_unary(command="~")
        self.vm_writer.write_ifgoto(
            label="WHILE_END{}".format(self.label_counter.get("while"))
        )

        while self._not_terminal_token_for("while"):
            self.tokenizer.advance()

            if self._statement_token():
                self.compile_statements()

        # write goto
        self.vm_writer.write_goto(
            label="WHILE_EXP{}".format(self.label_counter.get("while"))
        )
        # write end label
        self.vm_writer.write_label(
            label="WHILE_END{}".format(self.label_counter.get("while"))
        )
        # add while to labels count
        self.label_counter.increment("while")

    def compile_if(self):
        """
        example: if (True) { ... } else { ... }
        """
        # advance to expression start
        self.tokenizer.advance()
        self.tokenizer.advance()
        # compile expression in ()
        self.compile_expression()
        # write ifgoto to if statement
        self.vm_writer.write_ifgoto(
            label="IF_TRUE{}".format(self.label_counter.get("if"))
        )
        # write goto if false (else)
        self.vm_writer.write_goto(
            label="IF_FALSE{}".format(self.label_counter.get("if"))
        )
        # write if label
        self.vm_writer.write_label(
            label="IF_TRUE{}".format(self.label_counter.get("if"))
        )
        # body of if
        self.compile_conditional_body()
        # else?
        if self._starting_token_for(keyword_token="conditional", position="next"):
            # past closing {
            self.tokenizer.advance()
            # goto if end if this path wasn't hit
            self.vm_writer.write_goto(
                label="IF_END{}".format(self.label_counter.get("if"))
            )
            # if false
            self.vm_writer.write_label(
                label="IF_FALSE{}".format(self.label_counter.get("if"))
            )
            # compile else
            self.compile_conditional_body()
            # define IF_END
            self.vm_writer.write_label(
                label="IF_END{}".format(self.label_counter.get("if"))
            )
        else:  # no else present
            # go to end of if
            self.vm_writer.write_label(
                label="IF_FALSE{}".format(self.label_counter.get("if"))
            )

    def compile_conditional_body(self):
        while self._not_terminal_token_for("if"):
            self.tokenizer.advance()

            if self._statement_token():
                if self.tokenizer.current_token.is_if():
                    # add ifto labels count
                    self.label_counter.increment("if")
                    # compile nested if
                    self.compile_statements()
                    # subtract for exiting nesting
                    self.label_counter.decrement("if")
                else:
                    self.compile_statements()

    # term (op term)*
    def compile_expression(self):
        # ops get compiled at end in reverse order in which they were added
        ops = []

        while self._not_terminal_token_for("expression"):
            if self._subroutine_call():
                self.compile_subroutine_call()
            elif self._array_expression():
                self.compile_array_expression()
            elif self.tokenizer.current_token.text.isdigit():
                self.vm_writer.write_push(
                    segment="constant", index=self.tokenizer.current_token.text
                )
            elif self.tokenizer.identifier():
                self.compile_symbol_push()
            elif (
                self.tokenizer.current_token.is_operator()
                and not self._part_of_expression_list()
            ):
                ops.insert(
                    0, Operator(token=self.tokenizer.current_token.text, category="bi")
                )
            elif self.tokenizer.current_token.is_unary_operator():
                ops.insert(
                    0,
                    Operator(token=self.tokenizer.current_token.text, category="unary"),
                )
            elif self.tokenizer.string_const():
                self.compile_string_const()
            elif self.tokenizer.boolean():  # boolean case
                self.compile_boolean()
            elif self._starting_token_for("expression"):  # nested expression
                # skip starting (
                self.tokenizer.advance()
                self.compile_expression()
            elif self.tokenizer.null():
                self.vm_writer.write_push(segment="constant", index=0)

            self.tokenizer.advance()

        # compile_ops
        for op in ops:
            self.compile_op(op)

    def compile_op(self, op):
        if op.unary():
            self.vm_writer.write_unary(command=op.token)
        elif op.multiplication():
            self.vm_writer.write_call(name="Math.multiply", num_args=2)
        elif op.division():
            self.vm_writer.write_call(name="Math.divide", num_args=2)
        else:
            self.vm_writer.write_arithmetic(command=op.token)

    def compile_boolean(self):
        self.vm_writer.write_push(segment="constant", index=0)

        if self.tokenizer.boolean() == "true":
            # negate true
            self.vm_writer.write_unary(command="~")

    def compile_string_const(self):
        # handle string const
        string_length = len(self.tokenizer.string_const())
        self.vm_writer.write_push(segment="constant", index=string_length)
        self.vm_writer.write_call(name="String.new", num_args=1)
        # build string from chars
        for char in self.tokenizer.string_const():
            if not char == self.tokenizer.STRING_CONST_DELIMITER:
                ascii_value_of_char = ord(char)
                self.vm_writer.write_push(segment="constant", index=ascii_value_of_char)
                self.vm_writer.write_call(name="String.appendChar", num_args=2)

    def compile_symbol_push(self):
        symbol = self._find_symbol_in_symbol_tables(
            symbol_name=self.tokenizer.identifier()
        )
        segment = symbol["kind"]
        index = symbol["index"]
        self.vm_writer.write_push(segment=segment, index=index)

    def compile_array_expression(self):
        symbol_name = self.tokenizer.current_token.text
        symbol = self._find_symbol_in_symbol_tables(symbol_name=symbol_name)
        # get to index expression
        self.tokenizer.advance()
        self.tokenizer.advance()
        # compile
        self.compile_expression()
        # push onto local array symbol
        self.vm_writer.write_push(segment="local", index=symbol["index"])
        # add two addresses: identifer and expression result
        self.vm_writer.write_arithmetic(command="+")
        # pop address onto pointer 1 / THAT
        self.vm_writer.write_pop(segment="pointer", index=1)
        # push value onto stack
        self.vm_writer.write_push(segment="that", index=0)

    def compile_subroutine_call(self):
        subroutine_name = ""

        while not self._starting_token_for("expression_list"):
            subroutine_name += self.tokenizer.current_token.text
            self.tokenizer.advance()
        # get num of args
        num_args = self.compile_expression_list()
        # write_call after pushing arguments onto stack
        self.vm_writer.write_call(name=subroutine_name, num_args=num_args)

    # (expression (',' expression)* )?
    def compile_expression_list(self):
        num_args = 0

        if self._empty_expression_list():
            return num_args

        # start expressions
        self.tokenizer.advance()

        while self._not_terminal_token_for("expression_list"):
            num_args += 1
            self.compile_expression()
            if self._another_expression_coming():  # would be , after compile expression
                self.tokenizer.advance()
        return num_args

    def compile_return(self):
        if self._not_terminal_token_for(keyword_token="return", position="next"):
            self.compile_expression()
        else:  # push constant for void
            self.vm_writer.write_push(segment="constant", index="0")
            self.tokenizer.advance()

        self.vm_writer.write_return()

    def _not_terminal_token_for(self, keyword_token, position="current"):
        if position == "current":
            return (
                not self.tokenizer.current_token.text
                in self.TERMINATING_TOKENS[keyword_token]
            )
        elif position == "next":
            return (
                not self.tokenizer.next_token.text
                in self.TERMINATING_TOKENS[keyword_token]
            )

    def _starting_token_for(self, keyword_token, position="current"):
        if position == "current":
            return (
                self.tokenizer.current_token.text in self.STARTING_TOKENS[keyword_token]
            )
        elif position == "next":
            return self.tokenizer.next_token.text in self.STARTING_TOKENS[keyword_token]

    def _statement_token(self):
        return self.tokenizer.current_token.is_statement_token()

    def _another_expression_coming(self):
        return self.tokenizer.current_token.is_expression_list_delimiter()

    def _find_symbol_in_symbol_tables(self, symbol_name):
        if self.subroutine_symbol_table.find_symbol_by_name(symbol_name):
            return self.subroutine_symbol_table.find_symbol_by_name(symbol_name)
        elif self.class_symbol_table.find_symbol_by_name(symbol_name):
            return self.class_symbol_table.find_symbol_by_name(symbol_name)

    def _empty_expression_list(self):
        return self._start_of_expression_list() and self._next_ends_expression_list()

    def _start_of_expression_list(self):
        return (
            self.tokenizer.current_token.text in self.STARTING_TOKENS["expression_list"]
        )

    def _next_ends_expression_list(self):
        return (
            self.tokenizer.next_token.text in self.TERMINATING_TOKENS["expression_list"]
        )

    def _subroutine_call(self):
        return (
            self.tokenizer.identifier()
            and self.tokenizer.next_token.is_subroutine_call_delimiter()
        )

    def _array_expression(self):
        return self.tokenizer.identifier() and self._starting_token_for(
            keyword_token="array", position="next"
        )

    def _part_of_expression_list(self):
        return self.tokenizer.part_of_expression_list()
