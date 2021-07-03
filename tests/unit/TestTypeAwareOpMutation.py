# MIT License
#
# Copyright (c) [2020 - 2021] The yinyang authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import unittest

from src.parsing.Parse import parse_str, parse_file
from src.mutators.TypeAwareOpMutation import TypeAwareOpMutation

sys.path.append("../../")


class Mockargs:
    config = ""
    scratchfolder = "."
    name = ""


class TypeAwareOpMutationTestCase(unittest.TestCase):
    def test_ta(self):
        configfile = "tests/res/operators.txt"
        formulafile = "tests/res/formula_file.smt2"
        script = parse_file(formulafile)

        args = Mockargs()
        args.config = configfile
        args.name = formulafile.strip(".smt2")
        args.config = configfile
        args.modulo = 2

        script = parse_file(formulafile, silent=True)
        mutator = TypeAwareOpMutation(script, args)
        mutator.mutate()


if __name__ == "__main__":
    unittest.main()