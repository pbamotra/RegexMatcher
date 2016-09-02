class State(object):
	"""Represents the state/node in a Non-deterministic Finite Automata."""

	def __init__(self, isFinalState=False):
		"""
		Initialise the state type and transition arrays.

		Params:
			isFinalState: True if this is final state state, False otherwise
		"""

		self._charRangeMin = 0
		self._charRangeMax = 255

		self.isFinalState = isFinalState
		self.charTransitions = [[] for _ in xrange(self._charRangeMax)]
		self.epsilonTransitions = list()

	def isSupportedChar(self, character):
		"""
		Check if input character is in valid ASCII range.

		Params:
			character - input symbol

		Returns:
			True if input is an ascii symbol is in supported range, else False
		"""

		if len(character) > 1:
			raise ValueError("Expected a empty or one character string")

		if len(character) == 0: return True
		return self._charRangeMin <= ord(character) <= self._charRangeMax

	def moveOnChar(self, character, destinationState):
		"""
		Add a character transition to destinationState.

		Params:
			character - symbol for which this transition is defined
			destinationState - state to which transition leads to
		"""

		if not (isinstance(character, str)
				and isinstance(destinationState, State)):

			raise ValueError("Invalid parameters passed")

		if not self.isSupportedChar(character):
			raise ValueError("Character symbol is invalid")

		charAsciiValue = ord(character)
		self.charTransitions[charAsciiValue].append(destinationState)

	def moveOnEpsilon(self, destinationState):
		"""
		Add an empty move from this state to next.

		Params:
			destinationState - state to which transition leads to
		"""

		if not isinstance(destinationState, State):
			raise ValueError("Invalid parameters passed")

		self.epsilonTransitions.append(destinationState)

	def matches(self, string):
		"""
		Matches string against pattern represented by the NFA.

		Params:
			string - input for which pattern matching is performed

		Returns:
			True if string matches pattern (NFA), False otherwise
		"""

		return self.simulateNfa(string, set())

	def simulateNfa(self, string, processedStates):
		"""
		Simulate NFA one character at a time from the string.

		Params:
			string - input for which pattern matching is performed
			processedStates - set of states that were matched partial pattern

		Returns:
			True if the NFA reaches the final state, False otherwise
		"""

		# If loop exists in NFA, return False
		if self in processedStates: return False

		processedStates.add(self)

		if string:
			# If string is non-empty, check if the substring from second
			# character (if any) can be processed by the NFA starting with
			# the character transitions of the first character
			firstChar = string[0]

			if self.isSupportedChar(firstChar):
				for nextState in self.charTransitions[ord(firstChar)]:
					if nextState.matches(string[1:]): return True

			# or, if still there is no match found, try repeating the process
			# from next node by making an epsilon move

			for epsilonState in self.epsilonTransitions:
				if epsilonState.simulateNfa(string, processedStates): return True

		else:
			# If string has been completely processed, check if we're in
			# final state. If yes, the string matched correctly
			if self.isFinalState: return True

			# otherwise go to neighbors using epsilon moves, and try to
			# reach the final state
			for epsilonState in self.epsilonTransitions:
				if epsilonState.simulateNfa('', processedStates): return True

		return False