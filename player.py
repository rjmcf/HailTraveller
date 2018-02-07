class Player(object):
	def __init__(self, printer):
		self.karma = 0
		self.gun_pieces = 0
		self.inventory = {}
		self.has_gun = False
		self.printer = printer
	
	def get(self, inv_item, place):
		self.inventory[inv_item] = place
	
	def check_inventory(self):
		if self.inventory:
			self.printer.pprint("In your inventory you find:\n")
			for item, place in self.inventory.items():
				self.printer.pprint("    " + item + " from " + place + ".\n")
		else:
			self.printer.pprint("You have nothing in your inventory!")