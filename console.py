from item import Item

class Console(Item):
	def __init__(self, printer):
		super(Console, self).__init__(False, True, False, ["console", "board", "navigator", "map"], "The sounds of the console prevent the silence from becoming lonely.","The lights on the ship's console pulsate gently. The map on the display only works while in flight.", printer)
		