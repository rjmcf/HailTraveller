from item import Item

class Window(Item):
	def __init__(self, printer):
		super(Window, self).__init__(False, True, False, ["window", "out", "outside", "port"], "The light from the landscape outside the window serves as the ship's primary source of illumination while it is landed.", None, printer)
				
	def initialise(self, game):
		self.game = game
		self.description = self.game.current_planet.description		
		
	def be_moved(self):
		self.description = self.game.current_planet.description
		