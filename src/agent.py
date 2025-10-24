import random
from interpreter import Interpreter

class Agent:
	def __init__(self):
		self.q_table = {}
		self.epsilon = 1 # Al principio es todo explorar
		self.alpha = 0.1 # Valor tipico, placeholder
		self.gamma = 0.9 # Valor tipico, placeholder
		pass
	def seleccionar_accion(self):
		if random.random() < self.epsilon:
			# Explorar: acción aleatoria
			return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
		else:
			# Explotar: mejor acción según Q-table
			return self.mejor_accion(self.state)
	def mejor_accion(self, estado):
		# Obtener Q-values para este estado
		q_values = {
			"UP": self.q_table.get((estado, "UP"), 0),
			"DOWN": self.q_table.get((estado, "DOWN"), 0),
			"LEFT": self.q_table.get((estado, "LEFT"), 0),
			"RIGHT": self.q_table.get((estado, "RIGHT"), 0)
		}
		# Retornar la acción con mayor Q-value
		return max(q_values, key=q_values.get)
	def update_q_value(self, state, action, reward, next_state):
		pass
	
