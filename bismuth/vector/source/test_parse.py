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
        # For now we assume that points are 2D and paired off
        tokens = args[0]
        points = [parse_number(token.value) for token in tokens if token.type == "NUMBER"]
        return list(map(lambda x,y: (x,y), points, points[1:] + [0]))


svg_parser = None
with open(grammar_dir / "poly.lark", 'r') as f:
    svg_parser = Lark(f.read(), parser='lalr', debug=True)


path_string = "M20,230 Q40,205 50,230 T90,230"
#path_string = "M 10 10 C 20 20, 40 20, 50 10"
points = "60 110, 65 120 70 115 75 130 80 125 85 140 90 135 95 150 100 145"

tree = svg_parser.parse(points)
print(tree.pretty())

print("-"*30)
t = T().transform(tree)
print("-"*30)
print(t)
import code; code.interact(local=locals()) 