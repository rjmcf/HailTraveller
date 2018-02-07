import Tkinter as tk
import os.path

from printer import Printer

class App(tk.Frame):
	def __init__(self, game, master = None):
		self.game = game

		root = tk.Tk()
		w, h = root.winfo_screenwidth(), root.winfo_screenheight()
		root.geometry("%dx%d+0+0" % (w, h))

		self.parent = root

		tk.Frame.__init__(self, root)
		self.pack(fill = tk.BOTH, expand = True)
		self.make_widgets()

	def init_printer(self, ms):
		self.printer = Printer(ms, self)
		self.command_text["state"] = "disabled"
		self.printer.pprint("You wake up.")
		self.printer.pprint("You have no idea who you are, where you are, or why you are here.")
		self.printer.pprint("Type 'help' for hints on how to play.\n\n")
		self.command_text["state"] = "normal"
		return self.printer

	def make_widgets(self):
		self.title = tk.Label(self, text = "Welcome!")
		self.title.pack(fill = "x", expand = False, ipady = 10)

		self.text_w = CustomText(self, state = tk.DISABLED, bg = "bisque")
		self.text_w.pack(fill = "y", expand = True, pady = 20)
		self.text_w.tag_config("command", foreground="blue")
		self.text_w.tag_config("noun", foreground = "red")
		self.text_w.tag_config("verb", foreground = "#00aa00")

		self.holder_frame2 = tk.Frame(self)
		self.holder_frame2.pack(fill = "x", expand = False, ipady = 10)
		self.holder_frame2.grid_columnconfigure(0, weight = 1)
		self.holder_frame2.grid_columnconfigure(1, weight = 1)
		self.holder_frame2.grid_columnconfigure(2, weight = 1)
		self.holder_frame2.grid_columnconfigure(3, weight = 1)

		self.command_text = tk.Entry(self.holder_frame2, width = 90)
		self.command_text.grid(column = 1, row = 0, sticky = "ew", padx = 20)
		self.command_text.bind("<Return>", self.execute_command)

		self.add_button = tk.Button(self.holder_frame2, text = "Execute Command")
		self.add_button.grid(column = 2, row = 0)
		self.add_button["command"] = self.execute_command

	def set_tags(self):
		for object in self.game.current_location.objects:
			for name in object.noun_names:
				self.text_w.highlight_pattern(name, "noun")
		for key in self.game.parser.verb_map.keys():
			for verb in key:
				self.text_w.highlight_pattern(verb, "verb")
		self.text_w.section_start = self.text_w.index("end")


	def insert(self, text, command):
		self.text_w["state"] = "normal"
		if command:
			text = "> " + text + "\n"
			self.text_w.insert(tk.END, text, "command")
		else:
			self.text_w.insert(tk.END, text)
		self.text_w.see(tk.END)
		self.text_w["state"] = "disabled"

	def execute_command(self, *event):
		text = self.command_text.get()
		if len(text) > 0:
			self.command_text["state"] = "disabled"
			self.command_text.bind("<Return>", self.printer.skipText)
			self.insert(text, True)
			bind_to_execute = self.game.get_instruction(text)
			self.command_text["state"] = "normal"
			self.command_text.delete(0, tk.END)
			if bind_to_execute:
				self.command_text.bind("<Return>", self.execute_command)

	def save(self):
		self.printer.pprint("saving game!")
		count = 0
		while os.path.isfile("saves/save_game_" + str(count) + ".txt"):
			count += 1
		file = open("saves/save_game_" + str(count) + ".txt", "w")
		file.write(self.text_w.get("1.0", "end"))
		file.close()
		self.printer.pprint("saved game!")

class CustomText(tk.Text):
	def __init__(self, *args, **kwargs):
		tk.Text.__init__(self, *args, **kwargs)
		self.punc = [" ", ".", ",", "?", "!", "\n", "'", '"']
		self.section_start = "1.0"

	def highlight_pattern(self, pattern, tag, start = None, end = "end", regexp = False, whole = True):
		if start:
			start = self.index(start)
		else:
			start = self.index(self.section_start)

		self.mark_set("matchStart", start)
		self.mark_set("matchEnd", start)

		end = self.index(end)
		self.mark_set("searchLimit", end)

		count = tk.IntVar()
		while True:
			index = self.search(pattern, "matchEnd", "searchLimit", count = count, regexp = regexp)
			if index == "":
				break
			self.mark_set("matchStart", index)
			self.mark_set("matchEnd", "%s+%sc" %(index, count.get()))
			if not self.tag_names(index = "matchStart"):
				if whole:
					if self.get("%s+%sc" %(index, -1)) in self.punc and self.get("matchEnd") in self.punc:
						self.tag_add(tag, "matchStart", "matchEnd")
				else:
					self.tag_add(tag, "matchStart", "matchEnd")
