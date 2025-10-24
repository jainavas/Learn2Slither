import random


class Agent:
    def __init__(self):
        self.q_table = {}
        self.epsilon = 1.0
        self.alpha = 0.3
        self.gamma = 0.99
        self.replay_buffer = []  # Para guardar experiencias exitosas
    
    def seleccionar_accion(self, estado):
        """
        Epsilon-greedy con seguridad: no elegir acciones suicidas obvias
        """
        acciones_validas = self._get_acciones_seguras(estado)
        
        if not acciones_validas:
            # Si no hay acciones seguras, elegir cualquiera
            acciones_validas = ["UP", "DOWN", "LEFT", "RIGHT"]
        
        if random.random() < self.epsilon:
            # Exploración: elegir aleatoriamente entre acciones válidas
            return random.choice(acciones_validas)
        else:
            # Explotación: mejor acción entre las válidas
            return self.mejor_accion_segura(estado, acciones_validas)
    
    def _get_acciones_seguras(self, estado):
        """
        Devuelve acciones que NO llevan directamente a muerte obvia.
        Ahora estado = (UP_categoria, DOWN_categoria, LEFT_categoria, RIGHT_categoria)
        donde cada categoria es un string como 'DANGER_CLOSE', 'FOOD_NEAR', etc.
        """
        acciones_seguras = []
        
        # UP es segura si no hay peligro cercano
        up_cat = estado[0]
        if up_cat != 'DANGER_CLOSE':
            acciones_seguras.append("UP")
        
        # DOWN es segura si no hay peligro cercano
        down_cat = estado[1]
        if down_cat != 'DANGER_CLOSE':
            acciones_seguras.append("DOWN")
        
        # LEFT es segura si no hay peligro cercano
        left_cat = estado[2]
        if left_cat != 'DANGER_CLOSE':
            acciones_seguras.append("LEFT")
        
        # RIGHT es segura si no hay peligro cercano
        right_cat = estado[3]
        if right_cat != 'DANGER_CLOSE':
            acciones_seguras.append("RIGHT")
        
        return acciones_seguras
    
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
    
    def mejor_accion_segura(self, estado, acciones_validas):
        """
        Devuelve la mejor acción entre las válidas
        """
        q_values = {
            accion: self.q_table.get((estado, accion), 0)
            for accion in acciones_validas
        }
        
        max_q = max(q_values.values())
        mejores_acciones = [a for a, q in q_values.items() if q == max_q]
        return random.choice(mejores_acciones)
    
    def update_q_value(self, estado, accion, recompensa, siguiente_estado):
        """
        Actualiza Q-table usando la ecuación de Bellman.
        También guarda experiencias exitosas para replay.
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
        
        # Guardar experiencias exitosas (comer manzana verde)
        if recompensa >= 100:
            self.replay_buffer.append((estado, accion, recompensa, siguiente_estado))
            
            # Limitar buffer a las últimas 100 experiencias
            if len(self.replay_buffer) > 100:
                self.replay_buffer.pop(0)
    
    def replay_experiences(self, num_replays=10):
        """
        Re-aprende de experiencias exitosas pasadas.
        Esto refuerza comportamientos que llevaron a comer manzanas.
        """
        if len(self.replay_buffer) < 5:
            return
        
        for _ in range(num_replays):
            estado, accion, recompensa, siguiente_estado = random.choice(self.replay_buffer)
            
            # Re-actualizar Q-value
            if siguiente_estado is None:
                q_target = recompensa
            else:
                mejor_siguiente = max(
                    self.q_table.get((siguiente_estado, a), 0)
                    for a in ["UP", "DOWN", "LEFT", "RIGHT"]
                )
                q_target = recompensa + self.gamma * mejor_siguiente
            
            q_actual = self.q_table.get((estado, accion), 0)
            self.q_table[(estado, accion)] = q_actual + self.alpha * (q_target - q_actual)
    
    def decay_epsilon(self):
        """
        Reduce epsilon después de cada episodio.
        Decay más rápido para llegar antes a explotación.
        """
        self.epsilon *= 0.98
        self.epsilon = max(self.epsilon, 0.1)  # Mantener 10% de exploración