FALSE = {
    'type': 'bool',
    'value': False
}


class Parser(object):
    def __init__(self, input_):
        self.input = input_
        self.precedence = {
            '=': 1,
            '||': 2,
            '&&': 3,
            '<': 7,
            '>': 7,
            '<=': 7,
            '>=': 7,
            '==': 7,
            '!=': 7,
            '+': 10,
            '-': 10,
            '*': 20,
            '/': 20,
            '%': 20
        }
        self.direct_trans = {
            'Print': 'printf'
        }
        self.out = self.parse_toplevel()

    def _is(self, _in, _type):
        tok = self.input.peek()
        return tok and tok['type'] == _type and\
            (not _in or tok['value'] == _in) and tok

    def _skip(self, _in, _type):
        if getattr(self, f'is_{_type}')(_in):
            self.input.next()
        else:
            self.input.croak(f'Expecting punctuation: "{_in}"')

    def is_punc(self, ch):
        return self._is(ch, 'punc')

    def is_kw(self, kw):
        return self._is(kw, 'kw')

    def is_op(self, op=None):
        return self._is(op, 'op')

    def skip_punc(self, ch):
        return self._skip(ch, 'punc')

    def skip_kw(self, kw):
        return self._skip(kw, 'kw')

    def skip_op(self, op):
        return self._skip(op, 'op')

    def unexpected(self):
        self.input.croak(f'Unexpected token: {str(self.input.peek())}')

    def maybe_binary(self, left, my_prec):
        tok = self.is_op()
        if tok:
            his_prec = self.precedence[tok['value']]
            if his_prec > my_prec:
                self.input.next()
                return self.maybe_binary({
                    'type': 'assign' if tok['value'] == "=" else 'binary',
                    'operator': tok['value'],
                    'left': left,
                    'right': self.maybe_binary(self.parse_atom(), his_prec)
                }, my_prec)
        return left

    def delimited(self, start, stop, sep, parser):
        a = list()
        first = True
        self.skip_punc(start)
        while not self.input.eof():
            if self.is_punc(stop):
                break
            if first:
                first = False
            else:
                self.skip_punc(separator)
            if self.is_punc(stop):
                break
            a.insert(len(a), parser())
        self.skip_punc(stop)
        return a

    def parse_call(self, func):
        coord = f'{self.input.input.filename}:{self.input.input.line}'
        return {
            '_nodetype': 'FuncCall',
            'coord': coord,
            'name': {
                '_nodetype': 'ID',
                'name': self.direct_trans.get(func['value'], func['value']),
                'coord': coord
            },
            'args': {
                '_nodetype': 'ExprList',
                'coord': coord,
                'exprs': [
                    {
                        '_nodetype': 'Constant',  # change
                        'type': arg['type'],
                        'value': f'"{arg["value"]}"',
                        'coord': coord
                    } for arg in self.delimited('(', ')', ',', self.parse_expression)
                ]
            }
        }

    def parse_varname(self):
        name = self.input.next()
        if name['type'] != 'var':
            self.input.croak('Expecting variable name')
        return name['value']

    def parse_if(self):
        self.skip_kw('if')
        cond = self.parse_expression()
        if not self.is_punc('{'):
            self.skip_kw('then')
        then = self.parse_expression()
        ret = {
            'type': 'if',
            'cond': cond,
            'then': then,
        }
        if self.is_kw("else"):
            self.input.next()
            ret['else'] = self.parse_expression()
        return ret

    def parse_lambda(self):
        return {
            'type': 'lambda',
            'vars': self.delimited('(', ')', ',', self.parse_varname),
            'body': self.parse_expression()
        }

    def parse_bool(self):
        return {
            'type': 'bool',
            'value': self.input.next()['value'] == 'true'
        }

    def maybe_call(self, expr):
        expr = expr()
        return self.parse_call(expr) if self.is_punc('(') else expr

    def parse_atom(self):
        def anon():
            if self.is_punc('('):
                self.input.next()
                expr = self.parse_expression()
                self.skip_punc(')')
                return expr
            if self.is_punc('{'):
                return self.parse_prog()
            if self.is_kw('if'):
                return self.parse_if()
            if self.is_kw('true') or self.is_kw('false'):
                return self.parse_bool()
            tok = self.input.next()
            if tok['type'] == 'var' or tok['type'] == 'num' or\
               tok['type'] == 'str':
                return tok
            self.unexpected()
        return self.maybe_call(anon)

    def parse_toplevel(self):
        coord = f'{self.input.input.filename}:{self.input.input.line}'
        prog = list()
        while not self.input.eof():
            prog.insert(len(prog), self.parse_expression())
            if not self.input.eof():
                self.skip_punc(';')
        return {
            '_nodetype': 'FileAST',
            'coord': None,
            'ext': [
                {
                    "_nodetype": "FuncDef",
                    "coord": coord,
                    "decl": {
                        "_nodetype": "Decl",
                        "name": "main",
                        "quals": [],
                        "storage": [],
                        "funcspec": [],
                        "coord": coord,
                        "type": {
                            "_nodetype": "FuncDecl",
                            "coord": coord,
                            "type": {
                                "_nodetype": "TypeDecl",
                                "declname": "main",
                                "quals": [],
                                "coord": coord,
                                "type": {
                                    "_nodetype": "IdentifierType",
                                    "names": [
                                        "int"
                                    ],
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
                }
            ]
        }

    def parse_prog(self):
        coord = f'{self.input.input.filename}:{self.input.input.line}'
        prog = self.delimited('{', '}', ';', self.parse_expression)
        if prog.length == 0:
            return FALSE
        if prog.length == 1:
            return prog[0]
        return {
            '_nodetype': 'FileAST',
            'coord': None,
            'ext': [
                {
                    "_nodetype": "FuncDef",
                    "coord": coord,
                    "decl": {
                        "_nodetype": "Decl",
                        "name": "main",
                        "quals": [],
                        "storage": [],
                        "funcspec": [],
                        "coord": coord,
                        "type": {
                            "_nodetype": "FuncDecl",
                            "coord": coord,
                            "type": {
                                "_nodetype": "TypeDecl",
                                "declname": "main",
                                "quals": [],
                                "coord": coord,
                                "type": {
                                    "_nodetype": "IdentifierType",
                                    "names": [
                                        "int"
                                    ],
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
                }
            ]
        }

    def parse_expression(self):
        return self.maybe_call(lambda: self.maybe_binary(self.parse_atom(), 0))
