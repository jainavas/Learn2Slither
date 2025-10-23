from environment import Board

class Interpreter:
	def __init__(self, board):
		self.env = board
		pass

	def get_state(self):
		head_x, head_y = self.env.get_head_position()
		state = ""
		
		# UP
		for i in range(1, 10):
			y = head_y - i
			char = self.get_char_at(head_x, y)
			state += char
			state += "\n"
			if char == "W":
				break
		
		# LEFT - recorre al revés
		for i in range(9, 0, -1):
			x = head_x - i
			char = self.get_char_at(x, head_y)
			state += char
			if char == "W":
				break

		state += 'H'

		# RIGHT
		for i in range(1, 10):
			x = head_x + i
			char = self.get_char_at(x, head_y)
			state += char
			if char == "W":
				break

		# DOWN
		for i in range(1, 10):
			y = head_y + i
			char = self.get_char_at(head_x, y)
			state += char
			state += "\n"
			if char == "W":
				break

		return state

	def get_char_at(self, x, y):
		cell = self.env.get_cell(x, y)
		if cell is None:
			return "W"
		elif cell == 0:
			return "0"
		elif cell == 1:
			return "S"
		elif cell == 2:
			return "G"
		elif cell == 3:
			return "R"
		
# main.py o test simple
from environment import Board

env = Board()
env.reset()

interp = Interpreter(env)
state = interp.get_state()
print(state)