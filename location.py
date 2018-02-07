class Location(object):	
	def __init__(self, location_id, path_description, description, printer, events):
		"""description stores what will be seen when the player looks around. 
		paths lists the paths the player can take from this location.
		objects lists the objects found at this location. Each may be visible or invisible.
		"""
		
		self.location_id = location_id
		self.path_description = path_description
		self.description = description
		self.paths = {}
		self.objects = []
		self.events = events
		self.printer = printer
		self.event_returned = False
		
	def __repr__(self):
		return self.description
		
	def be_looked_at(self):
		"""Function called when the player looks around a location."""
		#self.printer.pprint(self.description)
		for item in self.objects:
			if item.visible:
				self.printer.pprint(item.item_description)
		for direction in self.paths.iterkeys():
			if "forward" in direction:
				self.printer.pprint("In front of you " + self.paths[direction].path_description)
			elif "ship" in direction:
				self.printer.pprint("On the side of the spaceship " + self.paths[direction].path_description)
			elif "citadel" in direction:
				self.printer.pprint("Looking again at the citadel, you see " + self.paths[direction].path_description)
			else:
				self.printer.pprint("To your " + direction[0] + " " + self.paths[direction].path_description)
		
	def set_direction(self, directions, location):
		"""Auxiliary function called while setting paths."""
		self.paths[directions] = location
		
		
		
# Location ids are formed of two numbers, the first corresponds to the planet it is on,
# and the second to the location itself. Locations are numbered in order of discovery:
#	Citadel			= 0
# 	FirePlanet 		= 1
#	WaterPlanet 	= 2
#	AirPlanet 		= 3
#	EarthPlanet 	= 4
# 	Ship 			= 5