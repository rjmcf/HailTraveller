from planet import Planet
from location import Location
from item import Item
from sign import Sign
from errors import InvalidDirection
from event import Event, EventName
from npc import NPC, NPCState

class Fireplanet(Planet):
	def __init__(self, name, ship, printer, game):
		"""Stores the information regarding the fire planet."""
		super(Fireplanet, self).__init__(name, "Bracing yourself against the heat, you squint out at the blackened landscape, dotted with pools of lava.", ship, game)
		
		self.crater = Location("10", "there is a path that leads back to where you left your spaceship. You hope it's still there and the crater hasn't eaten it.", "Your spaceship sits behind you, hanging on the edge of a large crater, which glows mysteriously due to the magma inside.", printer, [Event(EventName.on_arrival, 'self.game.printer.pprint("You had to be careful as you landed on Paxak, as the surface is mostly covered in seething lava. Even the ground you can walk on is inhospitible and dangerous. You are glad that you weren\'t born here.")', "10"), Event(EventName.on_sign_read, 'self.game.printer.pprint("The words on the sign are written in a language that speaks of crackling embers and barely controlled aggression. Though the language is not your own, you can read it, albeit with some difficutly. You wish you understood why.")', "1-")])
		ship_item = Item(False, True, False, ["ship", "spaceship", "craft"], "Your spaceship is still there, thank goodness.", "The plating on the bottom looks a little blackened after the descent through the hot atmosphere.", printer)
		crater = Item(False, True, False, ["crater"], "The crater behind the spaceship glows ominously.", "It looks pretty deep. The bottom, far below you, has what looks like a lava spring filling it. You wish you'd spotted a better patch of ground to land on, but this was the closest place to the signs of life you spotted from the air. It'll do for now.", printer)
		sign1 = Sign(self.get_sign_list()[1]["first_sign"], "A metal board attached to a section of small girder protrudes from the ground. You guess that this is the Paxak version of signs.", printer)
		npc1 = NPC(["man1"], "Man1 stands before you.", "As you look at man1, you see man1.", False, False, self.get_npc_speeches(1,0), printer, [], game)
		self.crater.objects = [ship_item, crater, sign1, npc1]
		
		self.base_of_volcano = Location("11", "you see a constant stream of smoke and a hazy glow from the top of a large mountain.", "You look up at the peak of the smoking volcano. You decide not to risk your life venturing up.", printer, []) 
		volcano = Item(False, True, False, ["mountain", "volcano"], "The volcano stands in front of you like a lightly sleeping giant.", "You reason that going to the top would be a pretty quick way to end your life.", printer)
		sign2 = Sign(self.get_sign_list()[1]["second_sign"], "Facing away from the volcano is a second sign, almost red hot from the heated ground.", printer)
		self.npc2 = NPC(["man2"], "Man2 stands before you.", "Perhaps she could get into the volcano?", True, False, self.get_npc_speeches(1,1), printer, [Event(EventName.on_talking, 'self.game.fireplanet.npc2.state = NPCState.task_complete', "11", NPCState.during_task), Event(EventName.on_talking, 'self.game.fireplanet.npc5.state = NPCState.task_complete; self.game.player.get("The deepest heat", "the volcano"); self.game.printer.pprint("You got the deepest heat from the volcano!")', "11", NPCState.after_task)], game)
		self.base_of_volcano.objects = [volcano, sign2, self.npc2]
		
		self.village = Location("12", "you can just see what could be the remains of a settlement.", "You are surrounded by tumbledown houses, broken and split. Debris is strewn from the doorways, as if they were hurriedly deserted.", printer, [Event(EventName.on_arrival, 'self.game.fireplanet.set_path(self.game.fireplanet.village, ("forwards", "forward"), self.game.fireplanet.crater)', "12")])		
		buildings = Item(False, True, False, ["buildings", "houses"], "You realise the houses are glittering slightly in the light of the everpresent lava.", "The houses appear to have been made from a glass like substance, now shattered. It's terrible, but it's also beautiful.", printer)
		sign3 = Sign(self.get_sign_list()[1]["third_sign"], "Just outside the village is another sign, telling more of the story.", printer)
		npc3 = NPC(["man3"], "Man3 stands before you.", "Man3 is a house husband.", False, False, self.get_npc_speeches(1,2), printer, [], game)
		self.village.objects = [buildings, sign3, npc3]
		
		self.lava_pool_edge = Location("13", "you can see a large expanse of lava.", "You go as close to the lava pool as you dare. It is hot.", printer, [])
		pool = Item(False, True, False, ["pool", "lava"], "The pool of lava is constantly in motion, as if being stirred from within.", "The heat of the molten rock is making bubbles in the liquid, and whenever they burst you have to be careful not to get burned.", printer)
		sign4 = Sign(self.get_sign_list()[1]["fourth_sign"], "In danger of being consumed by the spitting lava is a sign.", printer)
		npc4 = NPC(["man4"], "Man4 stands before you.", "Man4 will in fact be a child.", False, False, self.get_npc_speeches(1,3), printer, [], game)
		self.lava_pool_edge.objects = [pool, sign4, npc4]
		
		self.workshop = Location("14", "you spot a small building all on its own.", "The building is the least damaged of all the ones you have seen here, but then it's not made of the same material as the others.", printer, [Event(EventName.on_arrival, 'self.game.fireplanet.set_path(self.game.fireplanet.workshop, ("left",), self.game.fireplanet.crater)', "14"), Event(EventName.on_arrival, 'EventName.planets_visited_before_npcs += "A"', "14")])
		building = Item(False, True, False, ["building", "workshop"], "The small building looks solid and heavily fireproofed, and as if it has had to be rebuilt multiple times.", "The substance the building is made of reminds you of the hardened black rocks you have seen floating within the lava. Inside the building you see a furnace, an anvil, and an iron bucket filled with tools of a blacksmith. This must be the workshop of Paxak.", printer)
		sign5 = Sign(self.get_sign_list()[1]["fifth_sign"], "Stuck on the door is the sign that completes the story.", printer)
		self.npc5 = NPC(["man5"], "Man5 stands before you.", "Man5 owns the forge.", True, True, self.get_npc_speeches(1,4), printer, [Event(EventName.on_talking, 'self.game.fireplanet.npc2.state = NPCState.during_task; self.game.player.karma += 1', "14", NPCState.during_task), Event(EventName.on_talking, 'self.game.player.get("Explosive power", "Paxak"); self.game.player.gun_pieces += 1; self.game.printer.pprint("You got the Explosive Power part of the Ultimate Weapon!"); del(self.game.player.inventory["The deepest heat"]); self.game.printer.pprint("The deepest heat of the volcano was taken away.")', "14", NPCState.after_task)], game)
		self.workshop.objects = [building, sign5, self.npc5]
		
		self.landing_location = self.crater
		self.current_location = self.ship
		for loc in [self.crater, self.base_of_volcano, self.village, self.lava_pool_edge, self.workshop, self.ship]:
			self.add_location(loc)
			
		self.set_path(self.crater, ("left",), self.base_of_volcano)
		self.set_path(self.base_of_volcano, ("left",), self.village)
		self.set_path(self.village, ("left",), self.lava_pool_edge)
		self.set_path(self.lava_pool_edge, ("left",), self.workshop)
		
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
				if not events:
					events = []
				if event.cue == EventName.on_arrival and not event.called:
					event.called = True
					events.append(event)
				elif event.cue == EventName.on_sign_read and not event.called:
					event.called = True
					events.append(event)
			return events  