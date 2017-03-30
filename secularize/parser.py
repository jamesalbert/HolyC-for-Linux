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
            'Print': 'printf',
            'U0': 'void',
            'U8': 'unsigned char',
            'U16': 'unsigned short',
            'U32': 'unsigned int',
            'U64': 'unsigned long',
            'I8': 'char',
            'I16': 'short',
            'I32': 'int',
            'I64': 'long',
            'F64': 'double'
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
        # self.skip_punc(start)
        while not self.input.eof():
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
        coord = f'{self.input.input.filename}:{self.input.input.line}'
        name = func['name']['name']
        func['name']['name'] = name
        func['args']['exprs'] = [
            {
                '_nodetype': 'Constant',  # change
                'type': arg['type'],
                'value': f'"{arg["value"]}"'\
                if hasattr(arg['value'], 'isalpha') else f'{arg["value"]}',
                'coord': coord
            }
            for arg in self.delimited('(', ')', ',', self.parse_expression)
        ]
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
        vars_ = self.delimited('(', ')', ',', self.parse_varname)
        expr = self.parse_expression()
        expr['decl']['type']['args'] = {
            "_nodetype": "ParamList",
            "coord": "./examples/test.c:1",
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
        if self.input.peek().get('type') in ['str', 'num']:
            return self.parse_call(expr)
        else:
            return expr

    def parse_atom(self):
        def anon():
            if self.input.peek().get('_nodetype') == 'FuncCall':
                return self.input.next()
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
            if tok['type'] == 'datatype':
                var = self.input.next()
                print(self.input.tokens)
                # exit()
                print(tok, var)
                print(var)
                if var['_nodetype'] == 'FuncDef':
                    self.input.next()
                    return self.parse_lambda()
                var['type']['type']['names'].append(
                    self.direct_trans.get(tok['value'], tok['value']))
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
            if tok['type'] == 'var' or tok['type'] == 'num' or\
               tok['type'] == 'str':
                return tok
            if tok.get('_nodetype') == 'Decl':
                return {
                    'type': 'string',
                    'value': tok['name']
                }
                return {
                    "_nodetype": "ID",
                    "name": tok['name'],
                    "coord": tok['coord']
                }
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
                type_ = self.direct_trans.get(type_, type_)
                break
        self.input.next()
        prog = self.delimited('{', '}', ';', self.parse_expression)
        return self.input.read_function(name, prog, type_=[type_])

    def parse_expression(self):
        return self.maybe_call(lambda: self.maybe_binary(self.parse_atom(), 0))
