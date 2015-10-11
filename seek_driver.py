import sys
from seek_lang_parser import *
from seek_lang_lexer import seek_lex

def evaluate_seek_lang():
    filename = "instructions.sk"
    text = open(filename).read()
    tokens = seek_lex(text)
    parse_result = seek_parse(tokens)
    if not parse_result:
        sys.stderr.write('Parse error!\n')
        sys.exit(1)
    ast = parse_result.value
    env = {}
    ast.eval(env)

    sys.stdout.write('Final variable values:\n')
    for name in env:
        sys.stdout.write('%s: %s\n' % (name, env[name]))

if __name__ == '__main__':
    evaluate_seek_lang()
