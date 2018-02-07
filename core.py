from citadel import Citadel
from fireplanet import Fireplanet

from ship import Ship
from window import Window

from printer import Printer
from parser import Parser
from errors import InvalidCommandError

from stateholder import StateHolder
from player import Player

from main import App

class Core(object):
	def __init__(self):
		self.game_finished = False

		# The App
		self.app = App(self)

		# the Printer
		self.printer = self.app.init_printer(10)

		# the Player
		self.player = Player(self.printer)

		# the Ship
		the_window = Window(self.printer)
		self.ship = Ship(the_window, self.printer)

		# Planets and initialisation
		self.citadel = Citadel("Citadel", self.ship, self.printer, self)
		self.fireplanet = Fireplanet("Paxak", self.ship, self.printer, self)
		self.planets = [self.citadel, self.fireplanet]

		# Initial Values of Important Fields
		self.current_planet = self.citadel
		self.current_location = self.citadel.current_location
		#self.game_finished = False

		# Final initialisation now that enough exists
		the_window.initialise(self)
		self.citadel.land()

		# the Parser and helpers
		self.parser = Parser()

		self.directions = ["left", "right", "forwards", "forward", "ship", "spaceship", "out", "outside", "in", "inside", "back", "backwards", "citadel"]
		noun_list = []
		for object in self.current_location.objects:
			noun_list.extend(object.noun_names)
		self.parser.nouns = noun_list + self.directions

		# the StateHolder
		self.stateholder = StateHolder(self)

		self.start_game()

	def start_game(self):
		self.app.mainloop()

	def get_instruction(self, command):
		# Parser.parse returns a verb (which is a function) and a noun on which it operates.
################################################
# 		if command in ["l", "i", "e", "p", "k"]:
# 			self.stateholder.debug(command)
# 			return
 		if "cheat" in command:
 			self.stateholder.cheat(command)
 			return True
################################################
		try:
			f, a = self.parser.parse(command)
			# The function (within StateHolder) is called below.
			bind_to_execute = f(self.stateholder, a)
			self.printer.pprint("\n")
			self.app.set_tags()
			if self.game_finished:
				bind_to_execute = False
			return bind_to_execute
		# If an exception is raised, print its message and move on
		except InvalidCommandError as e:
			self.printer.pprint(e.message + "\n")
			return True

	def get_sign_list(self):
		# File contains python code creating all_signs
		sign_file = open("HailTraveller/signs.txt")
		exec(sign_file.read())
		return all_signs

e = Core()
