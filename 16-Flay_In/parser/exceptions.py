class ParsingError(Exception):
	pass

class CustomError(ParsingError):
	def __init__(self, titel, line, message):
		self.message = f"Line {line}: {titel}.\n{message}"
		super().__init__(self.message)

class InvalidPosition(ParsingError):
	def __init__(self, line, message):
		self.message = f"Line {line}: Invalid position of nb_drones.\n{message}"
		super().__init__(self.message)

class InvalidNumber(ParsingError):
	def __init__(self, line, message):
		self.message = f"Line {line}: Invalid positive number.\n{message}"
		super().__init__(self.message)

class NotFound(ParsingError):
	def __init__(self, message):
		self.message = f"Map must contain exactly {message}. None found."
		super().__init__(self.message)

class Duplicate(ParsingError):
	def __init__(self, line, message):
		self.message = f"Line {line}: Duplicate.\n{message}"
		super().__init__(self.message)

class InvalidName(ParsingError):
	def __init__(self, line, message):
		self.message = f"Line {line}: Invalid name.\n{message}"
		super().__init__(self.message)

class InvalidSyntax(ParsingError):
	def __init__(self, line, message):
		self.message = f"Line {line}: Syntax error.\n{message}"
		super().__init__(self.message)

class MapError(ParsingError):
	def __init__(self, message):
		self.message = f"Map error.\n{message}"
		super().__init__(self.message)

class SolverError(Exception):
	pass

class SimulationError(SolverError):
	def __init__(self, message):
		self.message = f"Simulation error.\n{message}"
		super().__init__(self.message)

class PathNotFound(SolverError):
	def __init__(self, message):
		self.message = f"Pathfinding error.\n{message}"
		super().__init__(self.message)
