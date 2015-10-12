import sys

from seek_lang.parser import *
from seek_lang.lexer import seek_lex


def evaluate_seek_lang(robot_pos = (0, 0), loot_pos = (0, 0)):
    filename = "instructions.sk"
    text = open(filename).read()
    tokens = seek_lex(text)
    if not tokens:
        return None
    parse_result = seek_parse(tokens)
    if not parse_result:
        sys.stderr.write('Parse error!\n')
        return None
    ast = parse_result.value
    env = {'robot_x': robot_pos[0],
           'robot_y': robot_pos[1],
           'loot_x': loot_pos[0],
           'loot_y': loot_pos[1],
           'movement_list': []}
    ast.eval(env)

    # sys.stdout.write('Final variable values:\n')
    # for name in env:
    #     sys.stdout.write('%s: %s\n' % (name, env[name]))
    return env['movement_list']

if __name__ == '__main__':
    evaluate_seek_lang()
