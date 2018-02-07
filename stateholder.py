from sign import Sign
from npc import NPC, NPCState

from event import Event, EventName
from errors import InvalidCommandError, InvalidDirection

import time

class StateHolder(object):

	def __init__(self, game):
		self.game = game
		# Python is pass by value, so must put final value of event in, not EventName.planets_visited
		self.events = [Event("A" * (len(self.game.planets) - 1), """self.game.printer.pprint("You remember the sign outside the citadel. Now you understand more about what happened, perhaps it might be worth going back?"); self.game.citadel.npc1.visible = True; self.events.extend([Event(EventName.on_arrival, "self.game.printer.pprint('A man, the first person you have ever seen as far as you can remember, stands before you.')", "00"), Event(EventName.on_arrival, "self.game.printer.pprint('You spot movement rushing down the path to your left. You try to ignore your breathing quickening and your muscles tightening. What could it have been?')", "02")])""", "50")]
		self.help_text = None

	def move(self, noun):
		if noun == None:
			raise InvalidCommandError("You must specify a direction to move in!\n")
		if noun in self.game.directions:
			# Can try to move
			try:
				events = self.game.current_planet.move(noun)
			except InvalidDirection:
				raise InvalidCommandError("You cannot go that way!\n")
			else:
				if events:
					self.events.extend(events)
				self.game.current_location = self.game.current_planet.current_location

				noun_list_list = [object.noun_names for object in self.game.current_location.objects]
				noun_list = [noun for sublist in noun_list_list for noun in sublist]
				self.game.parser.nouns = noun_list + self.game.directions
				self.game.printer.pprint(repr(self.game.current_location))

				self.check_events(EventName.on_arrival, self.move)
				self.check_events(EventName.planets_visited_before_npcs, self.move)
				self.check_events(EventName.gun_collecting, self.move)
		else:
			# Cannot move
			raise InvalidCommandError("You must specify a direction to move in!\n")
		return True

	def planets_visited(self):
		for event in self.events:
			if event.cue == 0:
				return True
		return False

	def reveal_people(self):
		for planet in self.game.planets:
			for location in planet.locations:
				for item in location.objects:
					if isinstance(item, NPC):
						item.visible = True

	def talk(self, noun):
		for object in self.game.current_location.objects:
			if noun in object.noun_names:
				if object.can_talk and object.visible:
					events, bind_to_execute = object.be_talked_to()
					if events:
						for event in events:
							if not event.called:
								event.called = True
								self.events.append(event)
					self.check_events(EventName.on_talking, self.talk, object)
					return bind_to_execute

		raise InvalidCommandError("You cannot do that!\n")
		return True

	def take(self, noun):
		for object in self.game.current_location.objects:
			if noun in object.noun_names:
				if object.visible and object.portable:
					# can take object
					pass

		raise InvalidCommandError("You cannot do that!\n")
		return True

	def look(self, noun = None):
		if not self.game.parser.words and not noun:
			self.game.current_location.be_looked_at()
			return True
		for object in self.game.current_location.objects:
			if noun in object.noun_names:
				if object.visible:
					# can look at object
					object.be_looked_at()
					return True
		for directions in self.game.current_location.paths.iterkeys():
			if noun in directions:
				self.game.printer.pprint(self.game.current_location.paths[directions].path_description.capitalize())
				return True

		#if noun in self.game.current_location.paths.iterkeys():
		#	self.game.printer.pprint(self.game.current_location.paths[noun].path_description.capitalize())
		#	return

		raise InvalidCommandError("You cannot do that!\n")
		return True

	def read(self, noun):
		for object in self.game.current_location.objects:
			if isinstance(object, Sign):
				# sign can be read
				self.check_events(EventName.on_sign_read, self.read)
				self.game.printer.pprint("You read the sign.\n")
				object.read()
				return True

		raise InvalidCommandError("You cannot do that!\n")
		return True

	def shoot(self, noun):
		raise InvalidCommandError("You cannot do that!\n")
		return True

	def fly1(self, planet):
		if not self.game.current_location == self.game.ship:
			raise InvalidCommandError("You cannot do that!\n")
			return True

		self.game.printer.pprint("Once you've taken off, the map shows you where you can fly to:")
		self.numbers = []
		for number, planet in enumerate(self.game.planets):
			string = "\t" + str(number) + ".\t" + planet.name
			if self.game.current_planet == planet:
				string += "\t(current)"
			self.numbers.append(number)
			self.game.printer.pprint(string)

		self.game.printer.pprint("Type the number of the planet you want to fly to.\n")
		self.game.app.command_text.bind("<Return>", self.fly2)
		return False


	def fly2(self, event):
		number = self.game.app.command_text.get()
		self.game.app.command_text["state"] = "disabled"
		self.game.app.command_text.bind("<Return>", self.game.printer.skipText)
		self.game.app.insert(number, True)

		try:
			number = int(number)
		except:
			self.game.printer.pprint("You must type a number to fly somewhere! You land back on the planet.")
			self.game.app.command_text["state"] = "normal"
			self.game.app.command_text.delete(0, "end")
			return True
		else:
			self.number = number

		if self.number not in self.numbers:
			self.game.printer.pprint("Type the number of the planet you want to fly to.\n\n")
			self.game.app.command_text.bind("<Return>", self.fly2)
			return False

		self.game.current_planet = self.game.planets[number]
		self.game.current_planet.land()
		self.game.printer.pprint("You gently touch down on " + self.game.current_planet.name +".\n\n")
		self.game.app.command_text["state"] = "normal"
		self.game.app.command_text.delete(0, "end")
		self.game.app.command_text.bind("<Return>", self.game.app.execute_command)

	def help(self, noun):
		# help function
		if not self.help_text:
			help_file = open("textFiles/help.txt")
			exec(help_file.read())
			self.help_text = help_text

		self.game.printer.pprint(self.help_text)
		return True

	def inventory(self, noun):
		if noun:
			self.game.printer.pprint("Just type 'inventory' to see what you have with you.")
		else:
			self.game.player.check_inventory()
		return True

	def quit(self, noun):
		# quit function
		quit()

	def save(self, noun):
		# save game
		self.demo_save()
		return True

	def demo_save(self):
		# save transcript for debug
		self.game.app.save()

	def end_game(self):
		self.game.game_finished = True
		self.game.printer.pprint("You find yourself in a large hall, designed so that the light streaming in through the stained glass windows is distributed evenly across the space, colours mixing and changing as motes of dust move gently in the almost still air. This place holds a power unlike one you have felt before.")
		self.game.printer.pprint("At the far end of the hall rests a throne, and seated demurely on top is a figure of immense grace, quite unlike anyone you have seen so far on your journey. Although the appearance of the person is striking, you are unable to guess anything about them, so alien are their features to you. You would guess that the man leading you down the hall towards the throne is some kind of fetid sub-species, tainted by who knows what perverting force. The thought strikes you as unsavoury, but you cannot help but compare everyone you have ever met with this perfect being you are now standing in front of.")
		self.game.printer.pprint("The man in front of you has dropped to the floor, prostrated himself in a pityful gesture of complete subjugation. \"I have brought them to you, oh Grand Collector, in the hopes that their actions have proven them worthy of your forgiveness!\", the man gabbles into the floor. You feel as though you too should be demonstrating how unworthy you are in the face of the Grand Collector, but you find yourself transfixed, stuck in place. The mention of forgiveness troubles you distantly, what have you done wrong?")
		self.game.printer.pprint("The man is still babbling, but is interrupted by a voice that speaks a language that you have not heard the entire time you have been here, but which you can still understand. The voice reminds you of a star: benevolent, but with a deadly edge. It is the voice of the Grand Collector.")
		self.game.printer.pprint("YOU ARE BOLD TO ACT WITHOUT OUR PERMISSION.")
		self.game.printer.pprint("The man stutters as he picks himself off the ground, head hung in shame. \"I - I only felt that given the opportunity, they might feel some compassion towards those they met on their journey. Perhaps repent...\" He is finally cowed into silence. The Grand Collector makes no movement, but you feel the weight of a gaze upon you.")
		self.game.printer.pprint("WELL? DO YOU REPENT?")
		self.game.printer.pprint("(Yes or No?)")
		self.game.app.command_text.bind("<Return>", self.end_game2)
		# Since self.game.game_finished == True, we don't need to return True or False anymore.

	def end_game2(self, event):
		#self.game.player.karma
		response = self.game.app.command_text.get()
		if len(response) == 0:
			return
		self.game.app.command_text["state"] = "disabled"
		self.game.app.command_text.bind("<Return>", self.game.printer.skipText)
		if response.lower() == 'y' or response.lower() == 'yes':
			self.game.app.insert("\"Yes.\"", True)
			self.game.printer.pprint("WHAT FOR? I FIND IT HIGHLY UNLIKELY THAT YOU KNOW.")
		elif response.lower() == 'n' or response.lower() == 'no':
			self.game.app.insert("\"No.\"", True)
			self.game.printer.pprint("WELL... NO MATTER. IT IS MEANINGLESS WHEN YOU KNOW NOT WHAT YOU ARE REPENTING FOR.")
		else:
			self.game.app.insert(response[0] + "amblewamble...", True)
			self.game.printer.pprint("In your rush to express a more coherent thought than a simple \"yes\" or \"no\", you stumble over your words, finding your attention inexorably drawn to the face of The Grand Collector, looking down at you in barely concealed disgust.")
			self.game.printer.pprint("EVEN NOW YOU ARE... DISAPPOINTING. IT IS A WONDER YOU WERE NOT DISCOVERED EARLIER.")

		self.game.printer.pprint("Now you are really intrigued. What is going on here? The little man is hurrying towards you. You are unsure if he is trying to protect you or himself at this point.")
		self.game.printer.pprint("\"I am sorry for deceiving you like this, but you must understand that it was necessary to give you a chance, to save your life!\" Once again he tails off, and you are left staring at him, waiting for him to go on.")
		self.game.printer.pprint("\"You have surely heard the legend of The Messenger on your travels? You can't go anywhere without seeing the repurcussions... I - I am sorry to say that this story is not a legend, but a memory. A recent one at that. One that you appear to have lost.")
		self.game.printer.pprint("\"You, friend, you are the The Messenger of that story. The army of your people is currently amassing just outside the territory of the Collective. You arrived on your ship nearly two solar rotations ago, bringing examples of the wealth of your people and the apparent willingness to learn our languages and culture.")
		self.game.printer.pprint("\"Until recently, we had offered you every hospitality we could. As your time here had reached one solar rotation, we allowed you to place your sign, in a language we could not read, in the center of our settlement. You said it was a welcome to the rest of your people for when they arrived. Knowing know what your plan was, I dread to think of what it actally said.")
		self.game.printer.pprint("\"Perhaps you can work out the rest. Paxak found you out, that you were not running from war but bringing it. That you learned our languages only to learn of our planets' resources and the Ultimate Weapon. That you betrayed our trust. Your treachery cost many lives that day, but somehow not your own. Perhaps you had some shielding technology that saved you from the blast. It doesn't matter.")
		self.game.printer.pprint("\"What matters is that when I found you, wandering hopelessly, without the faintest idea where your ship was, I knew that we had a chance to save ourselves. What you have with you now, the Ultimate Weapon, has the power to save or destroy everyone you can ever remember meeting. You have heard how your people plan to dispose of us. Can you still do that now, now that you know us?\"")
		self.game.printer.pprint("You have to take a moment to let all the new information sink in. You remember how welcoming that first sign had looked: it was you who had made it. You remember how surprised you were that you could read all the other signs: it was you who learned the languages.")
		self.game.printer.pprint("The two are both watching you, one eager, one impassive. You feel a sudden pressure, just as suddenly lifted. You realise in panic, that your own army has just warped in to orbit around the very planet you are stood on. You have to make a choice, and now.")
		self.game.printer.pprint("Will you fire the weapon at your own people, or attempt to use the teleporter on the warship above you to get out of range and fire the weapon at the Collective?")
		self.game.printer.pprint("\t1. Fire on your people.")
		self.game.printer.pprint("\t2. Fire on the Collective.")

		self.game.app.command_text["state"] = "normal"
		self.game.app.command_text.delete(0, "end")
		self.game.app.command_text.bind("<Return>", self.end_game3)

	def end_game3(self, event):
		response = self.game.app.command_text.get()
		if len(response) == 0:
			return
		self.game.app.command_text["state"] = "disabled"
		self.game.app.command_text.bind("<Return>", self.game.printer.skipText)

		if response == "1" or response == "2":
			self.end_selector(response, self.game.player.karma)
		else:
			self.game.printer.pprint("You must select either 1 or 2.")
			self.game.app.command_text["state"] = "normal"
			self.game.app.command_text.delete(0, "end")
			self.game.app.command_text.bind("<Return>", self.end_game3)
			return False

	def end_selector(self, response, karma):
		cutoff = len(self.game.planets) / 2
		if response == "1":
			if karma > cutoff:
				self.good_karma_fire_on_people()
			else:
				self.bad_karma_fire_on_people()
		else:
			if karma > cutoff:
				self.good_karma_fire_on_collective()
			else:
				self.bad_karma_fire_on_collective()

		self.game.printer.pprint("Thank you for playing Hail Traveller! I hope you enjoyed it. Press 'Enter' again to quit the game.")
		self.game.app.command_text["state"] = "normal"
		self.game.app.command_text.delete(0, "end")
		self.game.app.command_text.bind("<Return>", lambda e: quit())

	def good_karma_fire_on_people(self):
		self.game.printer.pprint("You fire on your own people, with good karma. You feel happy that you have saved these peaceful people, but you will never know a part of your identity.")

	def bad_karma_fire_on_people(self):
		self.game.printer.pprint("You try to fire on your own people, with bad karma. The Collective do not give you the chance, killing you as they expect you to betray them. You see the war start but will never know how it ends.")

	def good_karma_fire_on_collective(self):
		self.game.printer.pprint("You fire on the Collective, with good karma. Your own people have seen that you have been good to the people there and thus no longer trust you. They take the weapon from you and use it on the planet you are on.")

	def bad_karma_fire_on_collective(self):
		self.game.printer.pprint("You fire on the Collective, with bad karma. You escape to your ship and watch as all the planets you've ever known are destroyed. You try to learn your peoples' ways, but are forever an outsider.")

	def cheat(self, state):
		if "npc" in state:
			self.reveal_people()
		if "citadel" in state:
			self.reveal_people()
			self.game.citadel.second_sign.description = "In front of you is a giant building, towers and flying buttresses everywhere. The doors that once were barred are now blocked only by the man."
			self.game.citadel.second_sign.set_direction("citadel", self.game.citadel.citadel_loc)
			self.game.citadel.game_begin.objects.remove(self.game.citadel.npc1)
			self.game.citadel.second_sign.objects.append(self.game.citadel.npc1)
			self.game.citadel.npc1.state = NPCState.after_task
			words = state.split(' ')
			for word in words:
				try:
					self.game.player.karma = int(word)
					break
				except:
					continue
		self.game.printer.pprint("Cheating")
		return True

	def debug(self, command):
		if command == "l":
			print(self.game.current_location.location_id)
		elif command == "i":
			print(self.game.current_location.objects)
		elif command == "e":
			for event in self.events:
				print(event.cue, event.location_id)
		elif command == "p":
			print(EventName.planets_visited_before_npcs)
		elif command == "k":
			print(self.game.player.karma)
		return True

	def check_events(self, event_name, calling_f, *npc):
		self.events[:] = [event for event in self.events if not self.event_complete(event, event_name, calling_f, npc)]

	def event_complete(self, event, event_name, calling_f, *npc):
		# Checks if any events exist which need to be done now.
		if event.cue != event_name:
			return False

		if event_name == EventName.on_arrival:
			if event.location_id == self.game.current_location.location_id:
				exec(event.function)
				return True
		elif event_name == EventName.on_sign_read:
			if self.location_equals(event.location_id, self.game.current_location.location_id):
				if calling_f == self.read:
					exec(event.function)
					return True
		elif event_name == EventName.planets_visited_before_npcs:
			if event.location_id == self.game.current_location.location_id:
				if event_name == "A" * (len(self.game.planets) - 1):
					exec(event.function)
					return True
		elif event_name == EventName.on_talking:
			if event.location_id == self.game.current_location.location_id:
				if calling_f == self.talk:
					if npc[0][0].state == event.npc_state:
						try:
							exec(event.function)
						except:
							pass
							############################
							#print("Exception raised")
							############################
						return True
		elif event_name == EventName.gun_collecting:
			if event.location_id == self.game.current_location.location_id:
				if self.game.player.gun_pieces == (len(self.game.planets) - 1):
					exec(event.function)
					return True

		return False

	def location_equals(self, l1, l2):
		if l1[0] != l2[0]:
			return False
		if l1[1] == l2[1]:
			return True
		if l1[1] == "-" or l2[1] == "-":
			return True
		return False
