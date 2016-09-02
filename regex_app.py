import re
from thompson_constructor import *


def print_msg(message, padding=20):
    """
    Helper function to print formatted heading row.

    Params:
        message - message to be printed
        padding - count of padded symbol '-' on either side
    """
    print '-' * padding + ' ' + message + ' ' + '-' * padding


def run_experiment(pattern, regex):
    """
    Run regex matching on candidate strings.

    Params:
        pattern - regex to be evaluated
    """

    candidates = [ 
                  "",               # empty string
                  "ab",             # 'a' followed by 'b' 
                  "bb",             # 'b' followed by 'b' 
                  "a",              # only character 'a' 
                  "abbb",           # 'ab' followed by 'bb'
                  "bbab",           # 'bb' followed by 'ab'
                  "baba",           # 'ba' followed by 'ba'
                  "bbbbbbababbbbb", # thrice 'bb' -> twice 'ab' -> twice 'bb'
                  "bc",             # 'b' followed by 'c'
                  "abbc"            # 'ab' followed by 'bc'
                ]           
    for candidate in candidates:
        print candidate, pattern.matches(candidate)
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
    msg = 'Regex: (ab|bb)*bc'
    pattern = seq([kl(alt(["ab", "bb"])), "bc"])
    print_msg(message=msg)
    run_experiment(pattern, regex="(ab|bb)*bc$")

    # ------------------------------------------------------- #
    msg = 'Regex: ab{3,4}'
    pattern = seq(["a", alt(["b" * 3 + 'b' * i for i in xrange(4 - 3)])])
    print_msg(message=msg)
    run_experiment(pattern, regex="ab{3,4}")

if __name__ == '__main__':
    main()
