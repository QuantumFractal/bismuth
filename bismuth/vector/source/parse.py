from lark import Lark, Transformer, Token, Visitor, v_args
import logging
logging.basicConfig(level=logging.DEBUG)

import sys
from pathlib import Path

top_dir = Path(sys.path[0]).parents[0]
grammar_dir = top_dir / "grammar"
svg_dir = top_dir / "svg"


class GCodeTransformer(Transformer):
    def element(self, *args):
        tag = args[0][0].value
        attrs = args[0][2:-1]

        if tag == "rect":
            attrs.insert(0, ('tag', tag))
            return {t[0]: t[1] for t in attrs}
        elif tag == "svg":
            return args[0][-2]
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

with open(svg_dir / "rect1.svg", 'r') as f:
    tree = svg_parser.parse(f.read())
    print(tree.pretty())
    print("-----")
    t = GCodeTransformer().transform(tree)
    print(">>>>>")
    print(t.pretty())
    #Filter().visit(tree)
    #import code; code.interact(local=locals()) 
