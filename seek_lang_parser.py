from seek_lang_lexer import *
from seek_lang_combinators import *
from seek_lang_ast import *
from functools import reduce


def keyword(kw):
    return Reserved(kw, RESERVED)

id = Tag(ID)
num = Tag(INT) ^ (lambda i: int(i))

aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

def aexp_value():
    return (num ^ (lambda i: IntAexp(i))) | \
           (id  ^ (lambda v: VarAexp(v)))

def process_group(parsed):
    ((_, p), _) = parsed
    return p

def aexp():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)

def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group

def aexp_term():
    return aexp_value() | aexp_group()

def process_binop(op):
    return lambda l, r: BinopAexp(op, l, r)

def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser

def process_relop(parsed):
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)

bexp_precedence_levels = [
    ['and'],
    ['or'],
]

def bexp():
    return precedence(bexp_term(),
                      bexp_precedence_levels,
                      process_logic)

def bexp_relop():
    relops = ['<', '<=', '>', '>=', '==', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop

def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))

def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group

def bexp_term():
    return bexp_not()   | \
           bexp_relop() | \
           bexp_group()

def process_logic(op):
    if op == 'and':
        return lambda l, r: AndBexp(l, r)
    elif op == 'or':
        return lambda l, r: OrBexp(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)

def stmt():
    return assign_stmt() | \
           if_stmt()     | \
           for_stmt()    | \
           move_stmt()

def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return id + keyword('=') + aexp() ^ process

def stmt_list():
    separator = ((keyword(';') + keyword('\n')) |
                 keyword(';') |
                 keyword('\n')) ^ \
                (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)

def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)
    return keyword('if') + bexp() + \
           keyword('do') + Lazy(stmt_list) + \
           Opt(keyword('else') + Lazy(stmt_list)) + \
           keyword('end') ^ process

def for_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return ForStatement(condition, body)
    return keyword('for') + aexp() + \
           keyword('do') + Lazy(stmt_list) + \
           keyword('end') ^ process

def move_stmt():
    def process(parsed):
        direction = parsed
        return MoveStatement(direction)
    return (keyword('up') | keyword('down') | keyword('left') | keyword('right')) ^ process

def parser():
    return Phrase(stmt_list())

def seek_parse(tokens):
    ast = parser()(tokens, 0)
    return ast

