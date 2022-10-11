from stack_array import Stack


# You do not need to change this class
class PostfixFormatException(Exception):
    pass


def postfix_eval(input_str):
    """Evaluates a postfix expression

    Input argument:  a string containing a postfix expression where tokens
    are space separated.  Tokens are either operators + - * / ** >> << or numbers.
    Returns the result of the expression evaluation.
    Raises an PostfixFormatException if the input is not well-formed
    DO NOT USE PYTHON'S EVAL FUNCTION!!!"""

    stack_for_eval = Stack(30)

    if valid_input(input_str):
        token_list = input_str.split()
        for token in token_list:
            # If token is an operator, pop two operands from the stack and perform the operation on them
            # Push the new value to the stack
            if token == '+' or token == '-' or token == '*' \
                    or token == '/' or token == '^' or token == '**' or token == '<<' or token == '>>':

                if float(stack_for_eval.peek()) % 1 == 0:
                    value_1 = int(stack_for_eval.pop())
                else:
                    value_1 = float(stack_for_eval.pop())

                if float(stack_for_eval.peek()) % 1 == 0:
                    value_2 = int(stack_for_eval.pop())
                else:
                    value_2 = float(stack_for_eval.pop())

                if token == '+':
                    stack_for_eval.push(value_2 + value_1)
                elif token == '-':
                    stack_for_eval.push(value_2 - value_1)
                elif token == '*':
                    stack_for_eval.push(value_2 * value_1)
                elif token == '/':
                    if value_1 == 0:
                        raise ValueError
                    stack_for_eval.push(value_2 / value_1)
                elif token == '**' or token == '^':
                    stack_for_eval.push(value_2 ** value_1)
                elif token == '<<':
                    stack_for_eval.push(value_2 << value_1)
                elif token == '>>':
                    stack_for_eval.push(value_2 >> value_1)

            # If token is a numerical value, push it on the stack
            else:
                try:
                    stack_for_eval.push(int(token))
                except ValueError:
                    stack_for_eval.push(float(token))

    return stack_for_eval.pop()


def infix_to_postfix(input_str):
    """Converts an infix expression to an equivalent postfix expression

    Input argument:  a string containing an infix expression where tokens are
    space separated.  Tokens are either operators + - * / ** >> << parentheses ( ) or numbers
    Returns a String containing a postfix expression """
    stack_for_eval = Stack(30)
    postfix_list = []
    token_list = input_str.split()

    for token in token_list:
        temporary_counter = 0
        # if the token is a number, add it to the postfix_list
        if not (token == '+' or token == '-' or token == '*' or token == '/' or token == '^' or token == '**' or
                token == '(' or token == ')' or token == '<<' or token == '>>'):
            postfix_list.append(token)
        elif token == '(':  # if an opening parenthesis is encountered, push it onto the stack
            stack_for_eval.push(token)
        elif token == ')':  # when a closed parenthesis is encountered, evaluate the whole parenthetical expression
            encounter_closing_parentheses(stack_for_eval, postfix_list)
        else:  # if the token is an operator, evaluate it based on it's precedence
            while temporary_counter == 0:
                if not stack_for_eval.is_empty():
                    if stack_for_eval.peek() == '(':  # '(' leads to the next operator being pushed on the stack
                        temporary_counter += 1

                    elif precedence(stack_for_eval.peek()) >= precedence(token):  # if the current operator has a
                        # precedence less than or equal to the top of the stack, pop the stack to the list and
                        # replace the top of the stack with the new operator
                        if precedence(stack_for_eval.peek()) == 'd' == precedence(token):  # '^' and '**'
                            temporary_counter += 1
                        else:
                            postfix_list.append(stack_for_eval.pop())

                    else:  # if the new operator has a higher precedence push it onto the stack
                        temporary_counter += 1
                else:  # if the stack is empty, push the operator onto the stack
                    temporary_counter += 1
            stack_for_eval.push(token)

    while not stack_for_eval.is_empty():  # move leftover operators from the stack to the back of the postfix expression
        postfix_list.append(stack_for_eval.pop())
    return ' '.join(postfix_list)


def prefix_to_postfix(input_str):
    """Converts a prefix expression to an equivalent postfix expression

    Input argument:  a string containing a prefix expression where tokens are
    space separated.  Tokens are either operators + - * / ** >> << parentheses ( ) or numbers
    Returns a String containing a postfix expression(tokens are space separated)"""

    stack_for_eval = Stack(30)
    token_list = input_str.split()

    for i in range(len(token_list) - 1, -1, -1):
        # if the token is an operator, pop two strings from the stack and concatenate all three strings
        # push the new string to the stack
        if (token_list[i] == '+' or token_list[i] == '-' or token_list[i] == '*' or token_list[i] == '/' or token_list[
            i] == '^' or token_list[i] == '**' or
                token_list[i] == '(' or token_list[i] == ')' or token_list[i] == '<<' or token_list[i] == '>>'):
            op1 = stack_for_eval.pop()
            op2 = stack_for_eval.pop()
            string = op1 + ' ' + op2 + ' ' + token_list[i]
            stack_for_eval.push(string)
        # if the token is an operand, push it to the stack
        else:
            stack_for_eval.push(token_list[i])

    return stack_for_eval.peek()


def valid_input(input_string):
    """Checks if the input consists of valid tokens, and if there is the correct number of values and operators

    Input argument: A postfix expression
     Returns True if valid, raises the appropriate exception if invalid"""

    token_list = input_string.split()
    value_counter = 0
    operator_counter = 0

    for token in token_list:
        if not (token == '+' or token == '-' or token == '*'
                or token == '/' or token == '^' or token == '**' or token == '<<' or token == '>>'):  # an operand
            try:
                float(token)
            except ValueError:
                raise PostfixFormatException('Invalid token')

    for token in token_list:
        if token == '+' or token == '-' or token == '*' \
                or token == '/' or token == '^' or token == '**' or token == '<<' or token == '>>':
            operator_counter += 1
        else:
            value_counter += 1

    if value_counter - operator_counter < 1:
        raise PostfixFormatException('Insufficient operands')
    elif value_counter - operator_counter > 1:
        raise PostfixFormatException('Too many operands')

    return True


def encounter_closing_parentheses(stack, postfix_list):
    """Loop that adds all the tokens inside a set of parentheses to the postfix expression This method is necessary
    to translate from infix since parenthesis have the highest precedence and are not a valid operand in postfix

    Input argument: The operator stack and the postfix list that has been compiled so far.
    Returns the postfix list after the parenthetical expression has been added to it"""

    while stack.peek() != '(':
        postfix_list.append(stack.pop())
    stack.pop()
    return postfix_list


def precedence(token):
    """This method determines the precedence level of the input operator and returns a letter associated with that
    level. The letters are used because they are characters that can be directly compared to each other.

    Input argument: the operator whose precedence needs to be found
    Returns the precedence level of the operator, represented with a letter"""

    operator_precedence = [('**', 'd', 'high'), ('^', 'd', 'high'), ('*', 'c', 'medium'), ('/', 'c', 'medium'),
                           ('+', 'b', 'low'), ('-', 'b', 'low'), ('<<', 'a', 'lowest'), ('>>', 'a', 'lowest')]
    for operator in operator_precedence:
        if operator[0] == token:
            return operator[1]
