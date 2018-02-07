from stateholder import StateHolder
from errors import InvalidCommandError

class Parser(object):

	def __init__(self):
		self.verb_map = {
				("go", "move", "run", "walk", "enter"): StateHolder.move,
				("talk", "ask", "speak"): StateHolder.talk,
				("pick", "take", "grab"): StateHolder.take,
				("look", "see", "observe"): StateHolder.look,
				("read",): StateHolder.read,
				("shoot", "fire"): StateHolder.shoot,
				("fly",): StateHolder.fly1,
				("save",): StateHolder.save,
				("help",): StateHolder.help,
				("quit",): StateHolder.quit,
				("inventory",): StateHolder.inventory
				}
		self.nouns = []


	def parse(self, input):
		self.words = input.strip(".").split(" ");
		self.words = [e.lower() for e in self.words if e != '']
		self.verb = None
		self.noun = None

		for word in self.words:
			for key in self.verb_map.keys():
				if word in key:
					self.verb = self.verb_map[key]
					self.words.remove(word)
			if self.verb != None:
				break

		for word in self.words:
			if word in self.nouns and not self.noun:
				self.noun = word
				self.words.remove(word)

		# Check there is at least a verb
		if self.verb == None:
			raise InvalidCommandError("You need a verb!\n")
		# Check no other words are verbs or nouns
		for word in self.words:
			if word in self.nouns:
				raise InvalidCommandError("Too many nouns!\n")
			for key in self.verb_map.keys():
				if word in key:
					raise InvalidCommandError("Too many verbs!\n")

		return (self.verb, self.noun)
