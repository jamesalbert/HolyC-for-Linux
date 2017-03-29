class TokenStream(object):
    def __init__(self, input_):
        self.input = input_
        self.current = None
        self.keywords = 'if then else true false'.split(' ')
        self.datatypes = ['U0', 'U8', 'U16', 'U32', 'U64',
                          'I8', 'I16', 'I32', 'I64', 'F64']
        self.tokens = list()

    def croak(self, message):
        return self.input.croak(message)

    def is_keyword(self, word):
        return word in self.keywords

    def is_datatype(self, word):
        return word in self.datatypes

    def is_digit(self, ch):
        try:
            int(ch)
            return True
        except (ValueError, TypeError):
            return False

    def is_id_start(self, ch):
        try:
            return ch.isalpha()
        except AttributeError:
            return False

    def is_id(self, ch):
        return self.is_id_start(ch) or ch in '?!-<>=0123456789'

    def is_op_char(self, ch):
        return ch in '+-*/%=&|<>!'

    def is_punc(self, ch):
        return ch in ',;(){}[]'

    def is_whitespace(self, ch):
        return ch in ' _\t_\n'.split('_')

    def read_while(self, predicate):
        string = str()
        while not self.input.eof() and predicate(self.input.peek()):
            string += self.input.next()
        return string

    def read_while_prev(self, predicate):
        string = str()
        line = self.input.line
        col = self.input.col
        while not self.input.bof() and predicate(self.input.peek_prev()):
            string += self.input.prev()
        self.input.line = line
        self.input.col = col
        return string[::-1]

    def read_number(self):
        has_dot = False
        def anon(ch, has_dot):
            if ch == '.':
                if (has_dot):
                    return False
                has_dot = True
                return True
            return self.is_digit(ch)
        number = self.read_while(lambda ch: anon(ch, has_dot))
        try:
            number = int(number)
        except ValueError:
            number = float(number)
        self.tokens.append({
            'type': 'num',
            'value': number
        })
        return self.tokens[-1]

    def read_function(self, name, prog):
        coord = f'{self.input.filename}:{self.input.line}'
        self.tokens.append({
            "_nodetype": "FuncDef",
            "coord": coord,
            "decl": {
                "_nodetype": "Decl",
                "name": name,
                "quals": [],
                "storage": [],
                "funcspec": [],
                "coord": coord,
                "type": {
                    "_nodetype": "FuncDecl",
                    "coord": coord,
                    "type": {
                        "_nodetype": "TypeDecl",
                        "declname": name,
                        "quals": [],
                        "coord": coord,
                        "type": {
                            "_nodetype": "IdentifierType",
                            "names": ["int"] if name == 'main' else ["int"],
                            "coord": coord
                        }
                    },
                    "args": None
                },
                "bitsize": None,
                "init": None
            },
            "body": {
                "_nodetype": "Compound",
                "coord": coord,
                "block_items": prog
            },
            "param_decls": None
        })
        return self.tokens[-1]

    def read_ident(self):
        coord = f'{self.input.filename}:{self.input.line}'
        id_ = self.read_while(self.is_id)
        type_ = str()
        if self.is_keyword(id_):
            type_ = 'kw'
        elif self.is_datatype(id_):
            type_ = 'datatype'
        else:
            if self.tokens and self.tokens[-1].get('type') == 'datatype' and\
               self.peek()['value'] == '(':
                return self.read_function(id_, list())
            if self.peek()['value'] == '(':
                return {
                    "_nodetype": "FuncCall",
                    "coord": coord,
                    "name": {
                        "_nodetype": "ID",
                        "name": id_,
                        "coord": coord
                    },
                    "args": {
                        "_nodetype": "ExprList",
                        "coord": coord,
                        "exprs": [
                            {
                                "_nodetype": "Constant",
                                "type": "string",
                                "value": "\"\"",
                                "coord": coord
                            }
                        ]
                    }
                }
            return {
                "_nodetype": "Decl",
                "name": id_,
                "quals": [],
                "storage": [],
                "funcspec": [],
                "coord": coord,
                "type": {
                    "_nodetype": "TypeDecl",
                    "declname": id_,
                    "quals": [],
                    "coord": coord,
                    "type": {
                        "_nodetype": "IdentifierType",
                        "names": list(),  # type will be inserted later
                        "coord": coord
                    }
                },
                "init": {
                    "_nodetype": "Constant",
                    "type": "int",
                    "value": None,
                    "coord": coord
                },
                "bitsize": None
            }
        self.tokens.append({
            'type': type_,
            'value': id_
        })
        return self.tokens[-1]

    def read_escaped(self, end):
        escaped = False
        string = str()
        self.input.next()
        while not self.input.eof():
            ch = self.input.next()
            if escaped:
                string += ch
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == end:
                break
            else:
                string += ch
        return string

    def read_string(self):
        self.tokens.append({
            'type': 'str',
            'value': self.read_escaped('"')
        })
        return self.tokens[-1]

    def skip_comment(self):
        self.read_while(lambda ch: ch != "\n")
        self.input.next()

    def read_next(self):
        self.read_while(self.is_whitespace)
        if self.input.eof():
            return None
        ch = self.input.peek()
        if ch == "//":
            self.skip_comment()
            return self.read_next()
        if ch == '"':
            return self.read_string()
        if self.is_digit(ch):
            return self.read_number()
        if self.is_id_start(ch):
            return self.read_ident()
        if self.is_punc(ch):
            self.tokens.append({
                'type': 'punc',
                'value': self.input.next()
            })
            return self.tokens[-1]
        if self.is_op_char(ch):
            self.tokens.append({
                'type': 'op',
                'value': self.read_while(self.is_op_char)
            })
            return self.tokens[-1]
        self.input.croak(f'Can\'t handle character: {ch}')

    def read_prev(self):
        self.read_while_prev(self.is_whitespace)
        if self.input.bof():
            return None
        ch = self.input.peek()
        if ch == "//":
            self.skip_comment()
            return self.read_next()
        if ch == '"':
            return self.read_string()
        if self.is_digit(ch):
            return self.read_number()
        if self.is_id_start(ch):
            return self.read_ident()
        if self.is_punc(ch):
            self.tokens.append({
                'type': 'punc',
                'value': self.input.next()
            })
            return self.tokens
        if self.is_op_char(ch):
            self.tokens.append({
                'type': 'op',
                'value': self.read_while(self.is_op_char)
            })
            return self.tokens[-1]
        self.input.croak(f'Can\'t handle character: {ch}')

    def peek(self):
        if self.current:
            return self.current
        self.current = self.read_next()
        return self.current

    def next(self):
        tok = self.current
        self.current = None
        return tok or self.read_next()

    def prev(self):
        return self.read_prev()

    def eof(self):
        return self.peek() is None
