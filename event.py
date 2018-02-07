class Event(object):
	def __init__(self, cue, function, location_id, *npc_state):
		self.cue = cue
		self.function = function
		self.called = False
		self.active = True
		self.location_id = location_id
		if npc_state:
			self.npc_state = npc_state[0]
		
class EventName(object):
	on_arrival = 1
	on_sign_read = 2
	on_talking = 3
	gun_collecting = 4
	planets_visited_before_npcs = "" 