# Start of unittest - add to completely test functions in exp_eval

import unittest
from exp_eval import *


class test_expressions(unittest.TestCase):
    def test_postfix_eval_01(self):
        # Test a variety of postfix expressions
        self.assertAlmostEqual(postfix_eval("3 5 +"), 8)
        self.assertAlmostEqual(postfix_eval("6"), 6)
        self.assertAlmostEqual(postfix_eval("5 1 2 + 4 ^ + 3 - "), 83)
        self.assertAlmostEqual(postfix_eval("3 -5 +"), -2)
        self.assertAlmostEqual(postfix_eval("3.5 1 +"), 4.5)
        self.assertAlmostEqual(postfix_eval("2 4 **"), 16)
        self.assertAlmostEqual(postfix_eval("2 4 ^"), 16)
        self.assertAlmostEqual(postfix_eval("3 4 *  2 5 * +"), 22)
        self.assertAlmostEqual(postfix_eval("7 4 -3 * 1 5 + / *"), -14)
        self.assertAlmostEqual(postfix_eval("3 4 + 5 6 ^ 7 / *"), 15625)
        self.assertAlmostEqual(postfix_eval("5 5 * 4 2 / +"), 27)
        self.assertAlmostEqual(postfix_eval("100 87 - 3 * 39 / 1 1 - * 3 +"), 3)
        self.assertAlmostEqual(postfix_eval("2 1 3 ** **"), 2)
        # test bitshift operators
        self.assertAlmostEqual(postfix_eval('2 3 3 2 ** / 9 * <<'), 16)
        self.assertAlmostEqual(postfix_eval('2 3 3 2 ** / 9 * >>'), 0)
        self.assertRaises(TypeError, postfix_eval, '2 3 2 / >>')

    def test_postfix_eval_02(self):
        # Test for Invalid Token
        try:
            postfix_eval("blah")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Invalid token")

        try:
            postfix_eval("1 2 - 6 23 a 4")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Invalid token")

    def test_postfix_eval_03(self):
        # Test for Insufficient Operands
        try:
            postfix_eval("4 +")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Insufficient operands")

    def test_postfix_eval_04(self):
        # Test for Too Many Operands
        try:
            postfix_eval("1 2 3 +")
            self.fail()
        except PostfixFormatException as e:
            self.assertEqual(str(e), "Too many operands")

    def test_postfix_eval_05(self):
        # Test for divide by zero
        self.assertRaises(ValueError, postfix_eval, '1 0 /')
        self.assertRaises(ValueError, postfix_eval, '2 1 1 - /')

    def test_closing_parentheses(self):
        # test the helper function encounter_closing_parentheses that helps the postfix expression account for
        # parentheses
        stack = Stack(10)
        stack.push('(')
        stack.push('-')
        stack.push('+')
        lst = ['1', '+', '-5']
        self.assertEqual(encounter_closing_parentheses(stack, lst), ['1', '+', '-5', '+', '-'])

    def test_precedence(self):
        # test the helper function precedence that returns the precedence level of the input operator
        operator = '**'
        self.assertEqual(precedence(operator), 'd')
        operator = '^'
        self.assertEqual(precedence(operator), 'd')
        operator = '*'
        self.assertEqual(precedence(operator), 'c')
        operator = '/'
        self.assertEqual(precedence(operator), 'c')
        operator = '+'
        self.assertEqual(precedence(operator), 'b')
        operator = '-'
        self.assertEqual(precedence(operator), 'b')
        operator = '>>'
        self.assertEqual(precedence(operator), 'a')
        operator = '<<'
        self.assertEqual(precedence(operator), 'a')

    def test_infix_to_postfix_01(self):
        # test some general infix to postfix cases
        self.assertEqual(infix_to_postfix("6 - 3"), "6 3 -")
        self.assertEqual(infix_to_postfix("6"), "6")
        self.assertEqual(infix_to_postfix('3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3'), '3 4 2 * 1 5 - 2 3 ^ ^ / +')
        self.assertEqual(infix_to_postfix('4 * 2 / ( 1 - 5 ) ^ 2 ^ 3'), '4 2 * 1 5 - 2 3 ^ ^ /')

    def test_infix_to_postfix_02(self):
        # test a big infix expression including multiple exponents
        self.assertEqual(infix_to_postfix('2 * 3 ^ ( 4 ^ 2 ^ .5 ) / 8 * 3 + 1 * 4 + 5 - 6 ^ 2 / 422'),
                         '2 3 4 2 .5 ^ ^ ^ * 8 / 3 * 1 4 * + 5 + 6 2 ^ 422 / -')
        # test expressions that include bitshift operators
        self.assertEqual(infix_to_postfix('2 << 3'), '2 3 <<')
        self.assertEqual(infix_to_postfix('2 << 3 / 3 ** 2 * 9'), '2 3 3 2 ** / 9 * <<')
        self.assertEqual(infix_to_postfix('2 >> 3 / 3 ** 2 * 9'), '2 3 3 2 ** / 9 * >>')
        self.assertEqual(infix_to_postfix('2 + 3 >> 2'), '2 3 + 2 >>')

    def test_prefix_to_postfix(self):
        # test various long prefix expressions
        self.assertEqual(prefix_to_postfix("* - 3 / 2 1 - / 4 5 6"), "3 2 1 / - 4 5 / 6 - *")
        self.assertEqual(prefix_to_postfix('- / * 20 * 50 + 3 6 300 2'), '20 50 3 6 + * * 300 / 2 -')
        self.assertEqual(prefix_to_postfix('+ 500 40'), '500 40 +')
        self.assertEqual(prefix_to_postfix('+ - + / * 2 20 2 * + 3 4 ^ 3 2 6 15'),
                         '2 20 * 2 / 3 4 + 3 2 ^ * + 6 - 15 +')
        self.assertEqual(prefix_to_postfix('* - + ^ 2.1 2 5.2 7.2 7.1'), '2.1 2 ^ 5.2 + 7.2 - 7.1 *')
        # test including bitshift operator
        self.assertEqual(prefix_to_postfix('>> 5 ** -13 2'), '5 -13 2 ** >>')
        # test for a single number
        self.assertEqual(prefix_to_postfix('5'), '5')

    """ following are the test cases my code failed the first time around"""

    def test_01postfix_eval_add(self):
        self.assertAlmostEqual(12.0, postfix_eval("12"))
        self.assertAlmostEqual(12.0, postfix_eval("12.0"))


if __name__ == "__main__":
    unittest.main()
