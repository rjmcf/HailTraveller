class Item(object):
	def __init__(self, portable, visible, can_talk, noun_names, item_description, description, printer):
		self.portable = portable
		self.visible = visible
		self.can_talk = can_talk
		self.noun_names = noun_names
		self.item_description = item_description
		self.description = description
		self.printer = printer
		
	def __repr__(self):
		return self.noun_names[0]
		
	def be_looked_at(self):
		"""Function called when the player looks at the item."""
		self.printer.pprint(self.description)