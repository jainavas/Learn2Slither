class Interpreter:
	def __init__(self, board):
		self.env = board
		pass

	def get_state(self):
		head_x, head_y = self.env.get_head_position()
		state = ""
	
		# UP - construir desde arriba hacia la cabeza para que aparezca arriba
		for x in range(0, head_x + 1):
			state += " "
		state += "W\n"
		for y in range(0, head_y): # Desde 0 hasta justo antes de la cabeza
			for x in range(0, head_x + 1):
				state += " " 
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
			for x in range(0, head_x + 1):
				state += " "
			char = self.get_char_at(head_x, y)
			state += char + "\n"
			if char == "W":
				break
		for x in range(0, head_x + 1):
			state += " "
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

	def get_compressed_state(self):
		"""
		Versión comprimida del estado, extrayendo info del get_state() original.
		Garantiza que usamos EXACTAMENTE la misma información visible.
		"""
		# Obtener el estado completo en string
		full_state = self.get_state()
		
		# Dividir por líneas
		lines = full_state.strip().split('\n')
		
		# Encontrar la línea con la H (cabeza)
		head_line_idx = None
		for i, line in enumerate(lines):
			if 'H' in line:
				head_line_idx = i
				head_col = line.index('H')
				break
		
		# Extraer información de cada dirección
		state_compressed = []
		
		# UP: desde head_line_idx-1 hacia arriba (índice 0)
		up_info = self._extract_direction_info(lines, head_line_idx, head_col, 'UP')
		state_compressed.append(up_info)
		
		# DOWN: desde head_line_idx+1 hacia abajo
		down_info = self._extract_direction_info(lines, head_line_idx, head_col, 'DOWN')
		state_compressed.append(down_info)
		
		# LEFT: en la misma línea, desde head_col-1 hacia la izquierda
		left_info = self._extract_direction_info(lines, head_line_idx, head_col, 'LEFT')
		state_compressed.append(left_info)
		
		# RIGHT: en la misma línea, desde head_col+1 hacia la derecha
		right_info = self._extract_direction_info(lines, head_line_idx, head_col, 'RIGHT')
		state_compressed.append(right_info)
		
		return tuple(state_compressed)

	def _extract_direction_info(self, lines, head_line, head_col, direction):
		"""
		Extrae el primer objeto no-vacío en una dirección desde el string de estado.
		Devuelve tupla (tipo, distancia)
		"""
		distance = 0
		
		if direction == 'UP':
			# Recorrer líneas hacia arriba
			for i in range(head_line - 1, -1, -1):
				distance += 1
				if head_col < len(lines[i]):
					char = lines[i][head_col]
					if char != ' ' and char != '0':
						return (char, distance)
			return ('W', distance)  # Si no encontró nada, es el muro
		
		elif direction == 'DOWN':
			# Recorrer líneas hacia abajo
			for i in range(head_line + 1, len(lines)):
				distance += 1
				if head_col < len(lines[i]):
					char = lines[i][head_col]
					if char != ' ' and char != '0':
						return (char, distance)
			return ('W', distance)
		
		elif direction == 'LEFT':
			# Recorrer la misma línea hacia la izquierda
			line = lines[head_line]
			for i in range(head_col - 1, -1, -1):
				distance += 1
				char = line[i]
				if char != ' ' and char != '0':
					return (char, distance)
			return ('W', distance)
		
		elif direction == 'RIGHT':
			# Recorrer la misma línea hacia la derecha
			line = lines[head_line]
			for i in range(head_col + 1, len(line)):
				distance += 1
				char = line[i]
				if char != ' ' and char != '0':
					return (char, distance)
			return ('W', distance)
		
		return ('W', 0)  # Fallback