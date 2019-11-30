from lark import Lark, Transformer, Token, Visitor, v_args
import logging
logging.basicConfig(level=logging.DEBUG)

import sys
from pathlib import Path

top_dir = Path(sys.path[0]).parents[0]
grammar_dir = top_dir / "grammar"
svg_dir = top_dir / "svg"

svg_parser = None
with open(grammar_dir / "polyline.lark", 'r') as f:
    svg_parser = Lark(f.read(), parser='lalr', debug=True)


poly_line_string = "60.0 110 65 120 70 115 75 130 80 125 85 140 90 135 95 150 100 145"


tree = svg_parser.parse(poly_line_string)
print(tree.pretty())
import code; code.interact(local=locals()) 