import random


class Agent:
    def __init__(self):
        self.q_table = {}
        self.epsilon = 1.0
        self.alpha = 0.1
        self.gamma = 0.9
    
    def seleccionar_accion(self, estado):
        """
        Epsilon-greedy: explora con probabilidad epsilon,
        de lo contrario explota (mejor acción conocida)
        """
        if random.random() < self.epsilon:
            return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        else:
            return self.mejor_accion(estado)
    
    def mejor_accion(self, estado):
        """
        Devuelve la acción con mayor Q-value para ese estado.
        Si hay empate, elige aleatoriamente entre las mejores.
        """
        q_values = {
            "UP": self.q_table.get((estado, "UP"), 0),
            "DOWN": self.q_table.get((estado, "DOWN"), 0),
            "LEFT": self.q_table.get((estado, "LEFT"), 0),
            "RIGHT": self.q_table.get((estado, "RIGHT"), 0)
        }
        
        max_q = max(q_values.values())
        mejores_acciones = [a for a, q in q_values.items() if q == max_q]
        return random.choice(mejores_acciones)
    
    def update_q_value(self, estado, accion, recompensa, siguiente_estado):
        """
        Actualiza Q-table usando la ecuación de Bellman:
        Q(s,a) = Q(s,a) + alpha * (r + gamma * max(Q(s',a')) - Q(s,a))
        
        Si siguiente_estado es None (game over), solo usa la recompensa.
        """
        if siguiente_estado is None:
            # Terminal state: no hay futuro
            q_target = recompensa
        else:
            # Calcular máximo Q-value del siguiente estado
            mejor_siguiente = max(
                self.q_table.get((siguiente_estado, a), 0)
                for a in ["UP", "DOWN", "LEFT", "RIGHT"]
            )
            q_target = recompensa + self.gamma * mejor_siguiente
        
        # Obtener Q-value actual (0 si no existe)
        q_actual = self.q_table.get((estado, accion), 0)
        
        # Actualizar Q-table
        self.q_table[(estado, accion)] = q_actual + self.alpha * (q_target - q_actual)
    
    def decay_epsilon(self):
        """Reduce epsilon después de cada episodio para favorecer explotación"""
        self.epsilon *= 0.99
        self.epsilon = max(self.epsilon, 0.01)  # No bajar de 0.01