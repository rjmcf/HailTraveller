from item import Item

class Sign(Item):
	def __init__(self, text, description, printer):
		super(Sign, self).__init__(False, True, False, ["sign"], description, "You can just about read the worn letters on the sign.", printer)
		self.text = text
		
	def read(self):
		"""Function called when the player reads the sign."""
		self.printer.pprint(self.text)