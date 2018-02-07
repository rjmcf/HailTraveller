from item import Item
from errors import InvalidStateError

class NPC(Item):
	def __init__(self, names, item_description, description, has_task, gives_task, speeches, printer, events, game):
		super(NPC, self).__init__(False, False, True, names, item_description, description, printer)
		self.speeches = speeches
		self.has_task = has_task
		self.gives_task = gives_task
		self.state = NPCState.before_task
		self.printer = printer
		self.game = game

		# Events might cause another NPC to change state, and/or change the players karma
		self.events = None
		if events:
			self.events = events

	def accept_response(self, event):
		response = self.game.app.command_text.get().upper()
		self.game.app.command_text["state"] = "disabled"
		self.command_text.bind("<Return>", self.game.printer.skipText)
		self.game.app.insert(response, True)
		if not (response == "Y" or response == "N"):
			self.printer.pprint("\n\nWill you help the " + self.noun_names[0]+ "? Type 'Y' for Yes or 'N' for No.")
			self.game.app.command_text.bind("<Return>", self.accept_response)
			return
		if response == "Y":
			self.printer.pprint('"' + self.speeches[1]["Yes"] + '"')
			self.state = NPCState.during_task
			self.game.app.command_text["state"] = "normal"
			self.game.app.command_text.delete(0, "end")
			self.game.app.command_text.bind("<Return>", self.game.app.execute_command)
			return self.events
		else:
			self.printer.pprint('"' + self.speeches[1]["No"] + '"')
			self.state = NPCState.task_complete
			self.game.app.command_text["state"] = "normal"
			self.game.app.command_text.delete(0, "end")
			self.game.app.command_text.bind("<Return>", self.game.app.execute_command)
			return self.events

	def be_talked_to(self):
		self.printer.pprint("The " + self.noun_names[0]+ " talks to you:")
		if not self.has_task:
			self.printer.pprint('"' + self.speeches[0] + '"')
			return (self.events, True)
		else:
			if self.state == NPCState.before_task:
				self.printer.pprint('"' + self.speeches[0] + '"')
				if self.gives_task:
					self.printer.pprint("\n\nWill you help the " + self.noun_names[0]+ "? Type 'Y' for Yes or 'N' for No.")
					self.game.app.command_text.bind("<Return>", self.accept_response)
					return (self.events, False)
				else:
					return (self.events, True)

			elif self.state == NPCState.during_task:
				if self.gives_task:
					self.printer.pprint('"' + self.speeches[1]["Yes"] + '"')
				else:
					self.printer.pprint('"' + self.speeches[1] + '"')
				return (self.events, True)

			elif self.state == NPCState.task_complete:
				self.printer.pprint('"' + self.speeches[2] + '"')
				self.state = NPCState.after_task
				return ([], True)

			elif self.state == NPCState.after_task:
				self.printer.pprint('"' + self.speeches[3] + '"')
				return ([], True)
			else:
				raise InvalidStateError("NPC does not have correct state")



class NPCState(object):
	before_task = 0
	during_task = 1
	task_complete = 2
	after_task = 3
