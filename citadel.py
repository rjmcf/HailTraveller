from planet import Planet
from location import Location
from sign import Sign
from item import Item
from npc import NPC, NPCState
from errors import InvalidDirection
from event import Event, EventName

class Citadel(Planet):
	def __init__(self, name, ship, printer, game):
		"""Stores the information regarding the citadel."""
		super(Citadel, self).__init__(name, "You look out and see the broken village, the empty plain, and the spire of the citadel looming over it all.", ship, game)

		self.game_begin = Location("00", "you can see the ruined village in which you woke up.", "You are surrounded by tumble-down houses. You have no idea how you first arrived here.", printer, [])
		houses = Item(False, True, False, ["houses", "house", "buildings"], "Rows of houses spilling their guts on to the road surround you.", "The houses look like they have been destroyed by a large explosion. You wonder who lived there, and how they must have died.", printer)
		sign1 = Sign(self.get_sign_list()[0]["first_sign"], "A wooden sign is sticking upright in the dusty ground.", printer)
		self.npc1 = NPC(["man"], "There is a man standing before you.", "He is the first person you can remember seeing", True, False, self.get_npc_speeches(0,0), printer, [Event(EventName.on_talking, 'self.game.citadel.npc1.state = NPCState.during_task; self.reveal_people()', "00", NPCState.before_task), Event(EventName.gun_collecting, 'self.game.citadel.npc1.state = NPCState.task_complete', "00"), Event(EventName.on_talking, 'self.game.citadel.second_sign.set_direction(("forward", "forwards","citadel"), self.game.citadel.citadel_loc); self.game.citadel.game_begin.objects.remove(self.game.citadel.npc1); self.game.citadel.second_sign.objects.append(self.game.citadel.npc1); self.game.printer.pprint("The man scurries away to the citadel. You suppose you better follow him."); self.game.citadel.second_sign.description = "In front of you is a giant building, towers and flying buttresses everywhere. The doors that once were barred are now blocked only by the man."', "00", NPCState.after_task)], game)
		self.game_begin.objects = [houses, sign1, self.npc1]

		self.second_sign = Location("01", "there lies a dirt path leading through the houses to a large building.", "In front of you is a giant building, towers and flying buttresses everywhere. The door is barred.", printer, [Event(EventName.on_arrival, 'self.game.printer.pprint("What\'s that to your right?"); self.game.citadel.set_path(self.game.citadel.game_begin, ("right",), self.game.citadel.ship_hidden)', "00")])
		cit = Item(False, True, False, ["citadel", "building"], "There is a large building that looks like it might be a citadel of some sort.", "The imposing building looks like it would be difficult to attack and easy to defend. You wouldn't mind living inside it during a seige.", printer)
		sign2 = Sign(self.get_sign_list()[0]["citadel_sign"], "A sign is hanging from the door of the citadel.", printer)
		self.second_sign.objects = [cit, sign2]

		self.ship_hidden = Location("02", "you spot the path you didn't see at first leading out of the village to an open space.", "You are standing in front of a spaceship.", printer, [Event(EventName.on_arrival, 'self.game.printer.pprint("Once inside you\'ll be able to fly it, but only as far as the other four planets.")', "02")])
		ship_item = Item(False, True, False, ["ship", "spaceship", "craft"], "A spaceship rests lopsidedly in the dirt.", "The spaceship looks in a much worse state than it actually is. You hope.", printer)
		self.ship_hidden.objects = [ship_item]

		self.citadel_loc = Location("03", "the doors now stand slightly open, and a great light shines through.", "", printer, [Event(EventName.on_arrival, 'self.end_game()', "03")])		

		self.landing_location = self.ship_hidden
		self.current_location = self.game_begin
		for loc in [self.game_begin, self.second_sign, self.ship_hidden, self.citadel_loc, ship]:
			self.add_location(loc)

		self.set_path(self.game_begin, ("left",), self.second_sign)

	def move(self, direction):
		"""Changes the player's current location and sets the appropriate paths."""
		moved = False
		for directions in self.current_location.paths.iterkeys():
			if direction in directions:
				self.current_location = self.current_location.paths[directions]
				moved = True
		if not moved:
			raise InvalidDirection
		else:
			events = None
			for event in self.current_location.events:
				if event.cue == EventName.on_arrival and not event.called:
					event.called = True
					if not events:
						events = []
					events.append(event)
			return events
