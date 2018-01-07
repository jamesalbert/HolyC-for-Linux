from json import load


def populate_ast(phase, ast_type, **kwargs):
    with open(f'config/{ast_type}_ast.json') as ast_file:
        ast_json = load(ast_file)
    for keypath, value in kwargs.items():
        keys = keypath.split('.')
        last_key = keys.pop()
        if not keys:
            ast_json[last_key] = value
        else:
            sub_ast = ast_json[keys.pop(0)]
            '''
            fix this ugliness
            '''
            for key in keys:
                if isinstance(sub_ast, list):
                    sub_ast = sub_ast[0][key]
                else:
                    sub_ast = sub_ast[key]
            if isinstance(sub_ast, list):
                sub_ast[0][last_key] = value
            else:
                sub_ast[last_key] = value
    phase.tokens.append(ast_json)
    return phase.tokens[-1]
