# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest
from lark.lark import Lark

def DynamicEarleyLark(grammar, **kwargs):
    return Lark(grammar, lexer='dynamic', parser='earley', **kwargs)

class TestParserComments(unittest.TestCase):
    def make_test_parser(self):
        # Create a parser for a grammar that has `#` as a "comment" character, and which expects one
        return DynamicEarleyLark(r"""
            %import common.INT
            %ignore "#"
            start : INT*
        """)

    def test_happy_path_with_child(self):
        parser = self.make_test_parser()

        # Accepts a single digit
        tree = parser.parse("2")
        self.assertEqual(tree.children, ['2'])

        # Accepts multiple digits
        tree = parser.parse("23")
        self.assertEqual(tree.children, ['2', '3'])

        # Accepts no digits
        tree = parser.parse("")
        self.assertEqual(tree.children, [])

        # Accepts digits with ignored `#` character
        tree = parser.parse("#2")
        self.assertEqual(tree.children, ['2'])

    def test_comment_without_child(self):
        parser = self.make_test_parser()

        # This parse should ignore all `#` characters and return an empty tree.
        tree = parser.parse("##")
        self.assertEqual(tree.children, [])

if __name__ == '__main__':
    unittest.main()
