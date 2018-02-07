from errors import InvalidStateError

class Planet(object):
	def __init__(self, name, description, ship, game):
		"""is_visited is false until the landing location has 3 directions off of it.
		locations is a list of the locations that can be visited on the planet.
		current_location is a marker that keeps track of where the player is on the planet.
		"""
		self.name = name
		self.is_visited = False
		self.locations = []
		self.description = description
		self.ship = ship
		self.objects = []
		self.current_location = None
		self.game = game

	def set_path(self, loc1, direction, loc2):
		"""direction is either forwards or left. When the path is set, the player will be
		given that direction as an option to travel in.
		"""
		loc1.set_direction(direction, loc2)
		if "ship" in direction:
			loc2.set_direction(("out", "outside", "forward", "forwards"), loc1)
		elif "left" in direction:
			loc2.set_direction(("right",), loc1)
		elif "right" in direction:
			loc2.set_direction(("left",), loc1)
		elif "forwards" in direction:
			loc2.set_direction(direction, loc1)

		if loc1 not in self.locations:
			self.locations.append(loc1)
		if loc2 not in self.locations:
			self.locations.append(loc2)

	def add_location(self, loc):
		"""Adds a location to the planet without setting any paths from it."""
		self.locations.append(loc)
		if self.current_location == None:
			self.current_location = loc

	def get_sign_list(self):
		sign_file = open("textFiles/signs.txt")
		exec(sign_file.read())
		return all_signs

	def get_npc_speeches(self, planet, number):
		npc_file = open("textFiles/npcspeeches.txt")
		exec(npc_file.read())
		try:
			if planet == 0:
				return citadel_npcs[number]
			elif planet == 1:
				return fire_npcs[number]

			else:
				raise InvalidStateError("Incorrect planet given")
		except:
			raise InvalidStateError("Incorrect speech number given")

	def land(self):
		if self.name == "Citadel":
			self.set_path(self.landing_location, ("forward", "forwards", "ship", "spaceship", "in", "inside", "door"), self.ship)
		else:
			self.set_path(self.landing_location, ("back", "backwards", "ship", "spaceship", "in", "inside", "door"), self.ship)
		self.ship.window.be_moved()
