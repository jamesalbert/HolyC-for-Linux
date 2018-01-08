from json import dumps


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
        self.toplevel_prog = list()
        self.out = self.parse_toplevel()

    def _is(self, _in, _type):
        tok = self.input.peek()
        return tok.get('type', False) and tok and tok['type'] == _type and\
            (not _in or tok['value'] == _in) and tok

    def _skip(self, _in, _type):
        if getattr(self, f'is_{_type}')(_in):
            self.input.next()
        else:
            self.input.croak(f'Expecting punctuation: "{_in}"')

    def get_coord(self):
        return f'{self.input.input.filename}:{self.input.input.line}'

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
        while not self.input.eof():
            # print(f'delimited list: {a}')
            if self.is_punc(stop):
                break
            if first:
                first = False
            else:
                self.skip_punc(sep)
            if self.is_punc(stop):
                break
            a.append(parser())
        self.skip_punc(stop)
        return a

    def parse_call(self, func):
        coord = self.get_coord()
        # print(f'parsing call: {func}')
        name = func['name']['name']
        func['name']['name'] = name
        func['args']['exprs'] = [
            arg for arg in self.delimited('(', ')', ',', self.parse_expression)
        ]
        # print(f'func: {func}')
        return func

    def parse_varname(self):
        type_ = self.input.next()['value']
        name = self.input.next()
        if name['_nodetype'] != 'Decl':
            self.input.croak('Expecting variable name')
        name['type']['type']['names'].append(type_)
        name['init'] = None
        return name

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
        coord = self.get_coord()
        vars_ = self.delimited('(', ')', ',', self.parse_varname)
        expr = self.parse_expression()
        expr['decl']['type']['args'] = {
            "_nodetype": "ParamList",
            "coord": coord,
            "params": vars_,
        }
        return expr

    def parse_bool(self):
        return {
            'type': 'bool',
            'value': self.input.next()['value'] == 'true'
        }

    def maybe_call(self, expr):
        expr = expr()
        # print(f'sub expr: {expr}')
        if self.input.peek().get('type') in ['string', 'num'] or \
           self.input.peek().get('_nodetype') in ['ID']:
            return self.parse_call(expr)
        else:
            return expr

    def parse_atom(self):
        def anon():
            if self.input.peek().get('_nodetype') == 'FuncCall':
                print("found FuncCall")
                return self.input.next()
            if self.is_punc('('):
                print("found (")
                self.input.next()
                print("parsing expression after (")
                expr = self.parse_expression()
                print("skipping )")
                self.skip_punc(')')
                return expr
            if self.is_punc('{'):
                return self.parse_prog()
            if self.is_kw('if'):
                return self.parse_if()
            if self.is_kw('true') or self.is_kw('false'):
                return self.parse_bool()
            tok = self.input.next()
            print(f"got next token: {tok}")
            # print(f'tok: {dumps(tok, indent=2)}')
            # DATATYPE
            if tok.get('type') == 'datatype':
                print("found datatype")
                var = self.input.next()
                if var['_nodetype'] == 'FuncDef':
                    self.input.next()
                    return self.parse_lambda()
                var['type']['type']['names'].append(tok['value'])
                tok = self.input.next()
                if tok['value'] == ';':
                    var['init'] = None
                    return var
                if tok['value'] != '=':
                    self.input.croak('Expected = for variable declaration')
                tok = self.input.next()
                var['init']['type'] = type(tok['value']).__name__
                var['init']['value'] = str(tok['value'])
                return var
            # CONSTANT
            if tok.get('type') in ['string', 'int'] or \
               tok.get('_nodetype') in ['ID']:
                print("found string or int")
                return tok
            self.unexpected()
        return self.maybe_call(anon)

    def build_ast(self, prog):
        return {
            '_nodetype': 'FileAST',
            'coord': None,
            'ext': [self.input.read_function('main', prog)]
        }

    def parse_toplevel(self):
        # prog = list()
        functions = list()
        while not self.input.eof():
            expr = self.parse_expression()
            # print(f'toplevel expr: {expr}')
            if expr['_nodetype'] == 'FuncDef':
                functions.append(expr)
            else:
                self.toplevel_prog.append(expr)
                if not self.input.eof():
                    self.skip_punc(';')
        ast = self.build_ast(self.toplevel_prog)
        for func in functions[::-1]:
            ast['ext'].insert(0, func)
        return ast

    def parse_prog(self):
        coord = f'{self.input.input.filename}:{self.input.input.line}'
        name = str()
        type_ = str()
        for i, tok in enumerate(self.input.tokens[::-1]):
            if tok.get('_nodetype') == 'FuncDef':
                name = tok['decl']['name']
                type_ = self.input.tokens[len(self.input.tokens) - i - 3]['value']
                break
        self.input.next()
        prog = self.delimited('{', '}', ';', self.parse_expression)
        return self.input.read_function(name, prog, type_=[type_])

    def parse_expression(self):
        return self.maybe_call(lambda: self.maybe_binary(self.parse_atom(), 0))
