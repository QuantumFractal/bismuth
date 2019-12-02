from lark import Lark, Transformer, Token, Visitor, v_args
import logging
logging.basicConfig(level=logging.DEBUG)

import sys
from pathlib import Path

top_dir = Path(sys.path[0]).parents[0]
grammar_dir = top_dir / "grammar"
svg_dir = top_dir / "svg"


def parse_number(value):
    attr_val = None
    try:
        attr_val = float(value)
    except ValueError:
        try:
            attr_val = int(value)
        except ValueError:
            pass
    return attr_val

class T(Transformer):
    def start(self, *args):
        return args[0]

    def command(self, *args):
        tree = args[0][0]
        command = tree.data
        points = [t for t in tree.children if type(t) != Token]
        data = {'command': command, 'points': points}
        return data

    def pair(self, *args):
        first = parse_number(args[0][0].value)
        second = parse_number(args[0][1].value)
        return (first, second)

class GCodeTransformer(Transformer):

    def __init__(self):
        point_grammar = """start: (NUMBER WS NUMBER WS?)+
                            %import common.WS
                            %import common.NUMBER
                        """
        self.line_parser = Lark(point_grammar, parser='lalr')

        with open(grammar_dir / "path.lark") as f:
            self.path_parser = Lark(f.read(), parser='lalr')
        self.path_transformer = T()


    def element(self, *args):
        tag = args[0][0].value

        if tag == "svg":
            attrs = {t[0]: t[1] for t in args[0] if type(t) == tuple}
            content = [d for d in args[0] if type(d) == dict]
            return {'tag': tag, 'attrs': attrs, 'content': content}

        else:
            attrs = args[0][2:-1]
            attrs.insert(0, ('tag', tag))
            data = {t[0]: t[1] for t in attrs}

            if tag.startswith("poly"):
                tree = self.line_parser.parse(data['points'])
                points = [parse_number(n) for n in tree.children if n.type == "NUMBER"]
                data['points'] = points

            if tag.startswith("path"):
                tree = self.path_parser.parse(data['d'])
                tree = self.path_transformer.transform(tree)
                data['path'] = tree
            return data

    def start(self, *args):
        return args[0][1]

    def attr(self, *args):
        attr = args[0]
        attr_name = str(attr[0])
        attr_val = None

        try:
            attr_val = float(attr[1].value)
        except ValueError:
            try:
                attr_val = int(attr[1].value)
            except ValueError:
                attr_val = attr[1].value if attr[1] else None

        return (attr_name, attr_val)

    prolog = lambda self, _: None


class Filter(Visitor):
    def thing(self, tree):
        print(tree.data)


svg_parser = None
with open(grammar_dir / "svg.lark", 'r') as f:
    svg_parser = Lark(f.read(), parser='lalr', debug=True)

with open(svg_dir / "example1.svg", 'r') as f:
    tree = svg_parser.parse(f.read())
    print(tree.pretty())
    print("-----")
    t = GCodeTransformer().transform(tree)
    print(">>>>>")

    import json
    print(json.dumps(t, indent=2))
    #Filter().visit(tree)
    #import code; code.interact(local=locals()) 
