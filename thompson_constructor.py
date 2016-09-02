from collections import Iterable
from nfa_state import State
from nfa import Automata


def eps():
    """
    Construct NFA to match a null/empty string.

    Returns:
        Automaton that can simulate an empty string
    """
    startState, endState = State(), State(isFinalState=True)
    startState.moveOnEpsilon(endState)

    return Automata(startState, endState)


def ch(character):
    """
    Using Thompson's construction we define NFA for a single character.

    Params:
        character - regular expression of only a single character

    Returns:
        Automaton that can simulate a single character
    """
    startState, endState = State(), State(isFinalState=True)
    startState.moveOnChar(character, endState)

    return Automata(startState, endState)


def kl(automata):
    """
    Using Thompson's construction we define NFA for Kleene star.

    Params:
        automata - NFA on which Kleene star is to be defined

    Returns:
        Automaton that can simulate a Kleene star operation
    """

    if not (isinstance(automata, Automata)):
        raise ValueError("Invalid parameters passed")

    dummyStart, dummyEnd = State(), State(isFinalState=True)

    if automata \
        and automata.endState:
            automata.endState.moveOnEpsilon(automata.startState)
            automata.endState.isFinalState = False
            automata.endState.moveOnEpsilon(dummyEnd)

    
    dummyStart.moveOnEpsilon(automata.startState)
    dummyStart.moveOnEpsilon(dummyEnd)

    # automata \
    # and automata.startState \
    # and automata.startState.moveOnEpsilon(automata.endState)

    # return automata
    return Automata(dummyStart, dummyEnd)


def _seq(automata1, automata2):
    """
    Concates two NFAs together.

    Params:
        automata1 - first NFA in the concatenation sequence
        automata2 - second NFA in the concatenation sequence
    Returns:
        Automaton that can simulate two concatenated NFAs
    """

    if not (isinstance(automata1, Automata)
            and isinstance(automata2, Automata)):
        raise ValueError("Invalid parameters passed")

    if automata1 \
            and automata1.endState:
        automata1.endState.isFinalState = False

    if automata2 \
            and automata2.endState:
        automata2.endState.isFinalState = True

    automata1 \
    and automata1.endState \
    and automata1.endState.moveOnEpsilon(automata2 \
                                         and automata2.startState)

    return Automata(automata1 and automata1.startState,
                    automata2 and automata2.endState)


def _alt(automata1, automata2):
    """
    Simulates either of the two NFAs.

    Params:
        automata1 - first NFA
        automata2 - second NFA
    Returns:
        Automaton that can simulate either of two NFAs
    """

    dummyStart, dummyEnd = State(), State(isFinalState=True)

    if not (isinstance(automata1, Automata)
            and isinstance(automata2, Automata)):
        raise ValueError("Invalid parameters passed")

    if automata1 \
            and automata1.endState:
        automata1.endState.isFinalState = False

    if automata2 \
            and automata2.endState:
        automata2.endState.isFinalState = False

    dummyStart.moveOnEpsilon(automata1.startState)
    dummyStart.moveOnEpsilon(automata2.startState)

    automata1 \
    and automata1.endState \
    and automata1.endState.moveOnEpsilon(dummyEnd)

    automata2 \
    and automata2.endState \
    and automata2.endState.moveOnEpsilon(dummyEnd)

    return Automata(dummyStart, dummyEnd)


def strSeqToAutomata(string):
    """
    Convert a string to NFA.

    Params:
        string - input to be converted into an NFA

    Returns:
        Automata representing the string
    """
    if not isinstance(string, str):
        raise ValueError("Invalid input parameter passed")

    if not string: return eps()
    return _seq(dispatcher(string[0]), strSeqToAutomata(string[1:]))


def dispatcher(o):
    """
    Returns a correct Automaton based on the input object

    Params:
        o - object representing a regex/NFA component
    """

    if isinstance(o, Automata):
        return o
    elif isinstance(o, str):
        if len(o) == 0:
            return eps()
        if len(o) == 1:
            return ch(o)
        return strSeqToAutomata(o)

    raise ValueError("Invalid regular expression component")


def alt(regexs):
    """
    Construct a union of NFAs from individual regex components.

    Params:
        regexs - Individual elements of the overall NFA

    Returns:
        Automaton representing the complete NFA
    """

    if not isinstance(regexs, Iterable):
        raise ValueError("Expecting an iterable of regexs")

    automata = dispatcher(regexs[0])

    if len(regexs) > 1:
        for el in regexs[1:]:
            automata = _alt(automata, dispatcher(el))

    return automata


def seq(regexs):
    """
    Construct a concatenation of NFAs from individual regex components.

    Params:
        regexs - Individual elements of the overall NFA

    Returns:
        Automaton representing the complete NFA
    """

    automata = eps()

    for el in regexs:
        automata = _seq(automata, dispatcher(el))

    return automata
