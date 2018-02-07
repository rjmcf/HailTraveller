class Size_getter(object):
	def get_terminal_size(self):
		import os
		rows, columns = os.popen('stty size', 'r').read().split()
		return rows, columns
		