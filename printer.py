import textwrap
import time
import sys

class Printer(object):
	def __init__(self, ms, app):
		self.ms = ms / 1000.0
		self.app = app
		self.text = ''
		self.skip = False
		
	def pprint(self, text):
		self.text = text
		columns = int(self.app.text_w.cget("width"))
		to_print = ''
		if self.ms == 0:
			for line in str.splitlines(self.text):
				to_print += textwrap.fill(line, columns) + "\n"
			self.app.insert(to_print, False)
		else:
			for line in str.splitlines(self.text):
				to_print += textwrap.fill(line, columns)
				to_print += "\n"
			while len(to_print) > 0:
				time.sleep(self.ms)
				self.app.insert(to_print[0], False)
				to_print = to_print[1:]
				self.app.parent.update()
				if (self.skip):
					self.app.insert(to_print, False)
					break
		self.skip = False
					
				
	def skipText(self, *event):
		self.skip = True
	