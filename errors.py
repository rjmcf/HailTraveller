class InvalidCommandError(Exception):
	def __init__(self, message = "Invalid Command", *args):
		self.message = message
		self.args = args
		
class InvalidStateError(Exception):
	def __init__(self, message = "Invalid State", *args):
		self.message = message
		self.args = args
		
class InvalidDirection(Exception):
	def __init__(self, message = "Invalid Direction", *args):
		self.message = message
		self.args = args