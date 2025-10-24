import random

class Board:
	def __init__(self):
		self.segments = [] # (x, y)
		self.board = [[0 for _ in range(10)] for _ in range(10)]
		self.direction = "UP"
		self.len = 0
		self.reset()
		pass

	def snk_eats_apple(self, apple):
		while True:
			x = random.randint(0, 9)
			y = random.randint(0, 9)
			if self.board[y][x] == 0:
				break
		self.board[y][x] = apple

	DIRECTIONS = {
		"UP": (0, -1),
		"DOWN": (0, 1),
		"LEFT": (-1, 0),
		"RIGHT": (1, 0)
	}

	def is_valid_position(self, new_x, new_y):
		return 0 <= new_x < 10 and 0 <= new_y < 10

	def move_snake(self, direction):
		dy, dx = self.DIRECTIONS[direction]
		new_x = self.segments[0][0] + dx
		new_y = self.segments[0][1] + dy
		
		# Validar límites
		if not self.is_valid_position(new_x, new_y):
			self.game_over = True
			return False
		
		val = self.board[new_y][new_x]
		
		# Colisión consigo mismo
		if val == 1:
			self.game_over = True
			return False
		
		# Mover cabeza
		self.segments.insert(0, (new_x, new_y))
		self.board[new_y][new_x] = 1
		
		# Según qué come
		if val == 2:  # manzana verde
			self.length += 1
			self.snk_eats_apple(2)
		elif val == 3:  # manzana roja
			self.length -= 1
			self.snk_eats_apple(3)
			if self.length == 0:
				self.game_over = True
				return False
		else:  # val == 0
			self.segments.pop()
			old_x, old_y = self.segments[-1]
			self.board[old_y][old_x] = 0
		
		return True

	def reset(self):
		self.board = [[0 for _ in range(10)] for _ in range(10)]
		self.len = 3
		self.segments = []
		while True:
			x = random.randint(0, 9)
			y = random.randint(0, 9)
			if self.board[y][x] == 0:
				break
		for direction_name, (dx, dy) in self.DIRECTIONS.items():
			if (self.is_valid_position(x + dx * 2, y + dy * 2)):
				self.segments.insert(0, (x, y))
				self.segments.insert(0, (x + dx, y + dy))
				self.segments.insert(0, (x + dx * 2, y + dy * 2))
				self.board[y + dy * 2][x + dx * 2] = 1
				self.board[y + dy][x + dx] = 1
				self.board[y][x] = 1
				
				self.direction = direction_name
				break
		self.snk_eats_apple(2)
		self.snk_eats_apple(3)

	def get_cell(self, x, y):
		"""Devuelve qué hay en una posición"""
		if not self.is_valid_position(x, y):
			return None
		return self.board[y][x]

	def get_head_position(self):
		"""Devuelve (x, y) de la cabeza"""
		return self.segments[0]

	def get_length(self):
		"""Devuelve la longitud actual"""
		return self.len

	def is_game_over(self):
		"""Devuelve si terminó"""
		return self.game_over

	def printmap(self):
		for i in self.board:
			print(i)