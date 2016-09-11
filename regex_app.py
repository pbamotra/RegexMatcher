import re
from thompson_constructor import *


def print_msg(message, padding=20, symbol='-'):
    """
    Helper function to print formatted heading row.

    Params:
        message - message to be printed
        padding - count of padded symbol '-' on either side
    """
    print symbol * padding + ' ' + message + ' ' + symbol * padding


def run_experiment(pattern, regex):
    """
    Run regex matching on candidate strings.

    Params:
        pattern - regex to be evaluated
    """

    candidates = [ 
                  "",                                   # empty string
                  "ab",                                 # 'a' followed by 'b'
                  "bb",                                 # 'b' followed by 'b'
                  "a",                                  # only character 'a'
                  "abbb",                               # 'ab' followed by 'bb'
                  "bbab",                               # 'bb' followed by 'ab'
                  "baba",                               # 'ba' followed by 'ba'
                  "bbbbbbababbbbb",                     # thrice 'bb' -> twice 'ab' -> twice 'bb'
                  "bc",                                 # 'b' followed by 'c'
                  "abbc",                               # 'ab' followed by 'bc'
                  "aaa" * 5,                            # lot of 'a'
                  "abbbbbbc",                           # 'ab' -> 'bb' * 2 -> 'bc'
                  "aaaaaaaaaaaaaa",                     # 14 'a'
                  "aaaaaaaaaaaaaa" * 70                 # 14 * 70 'a'
                ]           
    for candidate in candidates:
        # print candidate, pattern.matches(candidate)
        truth = re.compile(regex).match(candidate) is not None
        assert pattern.matches(candidate) == truth
    print


def main():
    """Entry point to the code for running experiments."""

    # ------------------------------------------------------- #
    msg = 'Regex: (ab|bb)*'

    ab_or_bb = alt(["ab", "bb"])
    zero_or_more = kl(ab_or_bb)

    pattern = zero_or_more
    print_msg(message=msg)
    run_experiment(pattern, regex="(ab|bb)*$")

    # ------------------------------------------------------- #
    msg = 'Regex: (ab|bb)+'

    pattern = seq([alt(["ab", "bb"]), kl(alt(["ab", "bb"]))])
    print_msg(message=msg)
    run_experiment(pattern, regex="(ab|bb)+$")

    # ------------------------------------------------------- #
    msg = 'Regex: ((ab|bb)*(bc))'
    pattern = seq([kl(alt(["ab", "bb"])), "bc"])
    print_msg(message=msg)
    run_experiment(pattern, regex="((ab|bb)*(bc)$)")

    # ------------------------------------------------------- #
    msg = 'Regex: (ab{3,4})'
    pattern = seq(["a", alt(["b" * 3 + 'b' * i for i in xrange(4 - 3)])])
    print_msg(message=msg)
    run_experiment(pattern, regex="(ab{3,4}$)")

    # ------------------- Version 2.0 ----------------------- #
    print_msg(message='Added in version 2.0', symbol='=')
    print

    # - custom test -
    msg = 'Regex: ((a|aa)+)'
    a_or_aa = alt(["a", "aa"])
    zero_or_more_times = kl(a_or_aa)
    pattern = seq([a_or_aa, zero_or_more_times])

    print_msg(message=msg)
    run_experiment(pattern, regex="((a|aa)+)$")

    # - parser extension -
    msg = '>Regex: ((ab|bb)+)'
    pattern = constructPattern('((ab|bb)+)')
    print_msg(message=msg)
    run_experiment(pattern, regex="((ab|bb)+)$")

    msg = '>Regex: ((ab|bb)*)'
    pattern = constructPattern('((ab|bb)*)')
    print_msg(message=msg)
    run_experiment(pattern, regex="((ab|bb)*)$")

    msg = '>Regex: ((a|aa)+)'
    pattern = constructPattern('((a|aa)+)')
    print_msg(message=msg)
    run_experiment(pattern, regex="((a|aa)+)$")

    msg = '>Regex: ((ab|bb)*(bc))'
    pattern = constructPattern('((ab|bb)*(bc))')
    print_msg(message=msg)
    run_experiment(pattern, regex="((ab|bb)*bc)$")

    msg = '>Regex: ((ab|bb)(bc))'
    pattern = constructPattern('((ab|bb)(bc))')
    print_msg(message=msg)
    run_experiment(pattern, regex="((ab|bb)bc)$")

    msg = '>Regex: ((ab|bb)+(bc))'
    pattern = constructPattern('((ab|bb)+(bc))')
    print_msg(message=msg)
    run_experiment(pattern, regex="((ab|bb)+bc)$")

    msg = '>Regex: ((ab|bb)+bc*)'
    pattern = constructPattern('((ab|bb)+bc*)')
    print_msg(message=msg)
    run_experiment(pattern, regex="((ab|bb)+bc*)$")

    msg = '>Regex: ((ab|aaaaaaaaaaaaaa...x70)+(bc)*)'
    pattern = constructPattern('(((ab)|{})+(bc)*)'.format('aaaaaaaaaaaaaa' * 70))
    print_msg(message=msg)
    run_experiment(pattern, regex="((ab|{})+(bc)*)$".format('aaaaaaaaaaaaaa' * 70))

    msg = '>Regex: (a*b+)'
    pattern = constructPattern('(a*b+)')
    print_msg(message=msg)
    run_experiment(pattern, regex="(a*b+$)")


def annotate(regexString):
    """
    Used to explicitly concatenate string using binary operation

    Params:
        regexString - regex string
    Returns:
        regexString annotated with explicit concat operation .(dot)
    """
    operators = {'|', '*', '+'}
    result = ''

    for idx, ch in enumerate(regexString):
        if (idx + 1) < len(regexString):
            ch2 = regexString[idx + 1]
            result += ch
            if ch != '(' and ch2 != ')' and ch2 not in operators and ch != '|':
                result += '.'
    result += regexString[-1]
    return result


def postfixConvertor(regexString):
    """
    Converts regex string after annotation to postfix format for easy processing

    Params:
        regexString - regex string
    Returns:
        String - postfix version of the regex
    """
    precedence = {'(': 1, '|': 2, '.': 3, '*': 4, '+':4}

    parse = ''
    stack = []
    regexString = annotate(regexString)

    for ch in regexString:
        if ch == '(':
            stack.append(ch)
        elif ch == ')':
            while stack[-1] != '(':
                parse += stack.pop()
            stack.pop()
        else:
            while stack:
                if precedence.get(stack[-1], 5) >= precedence.get(ch, 5):
                    parse += stack.pop()
                else: break
            stack.append(ch)
    return parse


def constructPattern(regexString):
    """
    Processes postfix version of regex string to an NFA

    Params:
        regexString - postfix regex string
    Returns:
        NFA representing regex
    """
    method_map = {'|': 'alt', '.': 'seq'}
    stack = []
    operators = {'.', '|', '*', '+'}
    binary = {'.', '|'}
    unary = operators - binary
    res = ''
    postfixRegex = postfixConvertor(regexString)

    for ch in postfixRegex:
        res = ''
        if ch not in operators:
            stack.append((ch, True))
        else:
            if ch in binary:
                op2, isChar2 = stack.pop()
                op1, isChar = stack.pop()

                if isChar2 and isChar and ch == '.':
                    res = op1 + op2
                    push = (res, True)
                else:
                    res = method_map[ch] + '([' + ('\"'  if isChar  else '') + op1 \
                                                + ('\",' if isChar  else ',') \
                                                + ('\"'  if isChar2 else '') + op2 \
                                                + ('\"'  if isChar2 else '') \
                                                + '])'
                    push = (res, False)
                stack.append(push)
            else:
                op1, isChar = stack.pop()
                res = 'kl' + '(' + ('\"' if isChar else '') + op1 \
                                 + ('\"' if isChar else '') + ')'
                if ch == '+':
                    res = 'seq([' + ('\"' if isChar else '') + op1 \
                                  + ('\"' if isChar else '') + ', ' + res + '])'
                stack.append((res, False))

    return eval(stack.pop()[0])

if __name__ == '__main__':
    main()

