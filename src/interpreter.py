from environment import Board

class Interpreter:
	def __init__(self, board):
		self.env = board
		pass

	def get_state(self):
		head_x, head_y = self.env.get_head_position()
		state = ""
	
		# UP - construir desde arriba hacia la cabeza para que aparezca arriba
		state += "W\n"
		for y in range(0, head_y):  # Desde 0 hasta justo antes de la cabeza
			char = self.get_char_at(head_x, y)
			state += char + "\n"
			if char == "W":
				break
		# LEFT - construir desde la izquierda hacia la cabeza
		state += "W"
		for x in range(0, head_x):  # Desde 0 hasta justo antes de la cabeza
			char = self.get_char_at(x, head_y)
			state += char
			if char == "W":
				break
		
		# HEAD
		state += 'H'
		
		# RIGHT - desde la cabeza hacia la derecha
		for x in range(head_x + 1, 10):
			char = self.get_char_at(x, head_y)
			state += char
			if char == "W":
				break		
		state += "W\n"
		
		# DOWN - desde la cabeza hacia abajo
		for y in range(head_y + 1, 10):
			char = self.get_char_at(head_x, y)
			state += char + "\n"
			if char == "W":
				break
		
		state += "W"
		
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
