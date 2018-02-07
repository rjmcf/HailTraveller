from location import Location
from console import Console

class Ship(Location):
	"""ship should not be a planet!"""
	def __init__(self, window, printer):
		super(Ship, self).__init__("50", "you can see a door through which you can enter.", "The ship has a small cockpit, and you try not to become claustrophobic.", printer, [])
		
		self.console = Console(self.printer)
		self.window = window
		self.objects = [self.window, self.console]
		
	def be_looked_at(self):
		for item in self.objects:
			self.printer.pprint(item.item_description)
		self.printer.pprint("In front of you is the exit from the ship, through which you catch glipses of " + self.window.game.current_planet.name +".")
		