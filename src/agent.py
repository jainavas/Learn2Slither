import random


class Agent:
    def __init__(self):
        self.q_table = {}
        self.epsilon = 1.0
        self.alpha = 0.35
        self.gamma = 0.95
        self.replay_buffer = []

    def seleccionar_accion(self, estado):
        """
        Epsilon-greedy con sesgo hacia comida cuando explora
        """
        vld_act = self._get_acciones_seguras(estado)
        acciones_con_comida = self._get_acciones_hacia_comida(estado)

        if not vld_act:
            vld_act = ["UP", "DOWN", "LEFT", "RIGHT"]

        if random.random() < self.epsilon:
            # Exploración: preferir comida si hay
            if acciones_con_comida and random.random() < 0.7:
                return random.choice(acciones_con_comida)
            return random.choice(vld_act)
        else:
            # Explotación: mejor acción entre las válidas
            return self.mejor_accion_segura(estado, vld_act)

    def _get_acciones_seguras(self, estado):
        """
        Devuelve acciones que NO llevan a peligro inmediato.
        estado = (UP_cat, DOWN_cat, LEFT_cat, RIGHT_cat)
        """
        acciones_seguras = []

        # UP es segura si no hay peligro inmediato
        if estado[0] != "DANGER_IMM":
            acciones_seguras.append("UP")

        # DOWN es segura si no hay peligro inmediato
        if estado[1] != "DANGER_IMM":
            acciones_seguras.append("DOWN")

        # LEFT es segura si no hay peligro inmediato
        if estado[2] != "DANGER_IMM":
            acciones_seguras.append("LEFT")

        # RIGHT es segura si no hay peligro inmediato
        if estado[3] != "DANGER_IMM":
            acciones_seguras.append("RIGHT")

        return acciones_seguras

    def _get_acciones_hacia_comida(self, estado):
        """
        Devuelve acciones que van hacia manzanas verdes
        """
        acciones_comida = []
        direcciones = ["UP", "DOWN", "LEFT", "RIGHT"]

        for i, dir_name in enumerate(direcciones):
            cat = estado[i]
            if "FOOD" in cat:  # FOOD_CLOSE, FOOD_NEAR, FOOD_FAR
                acciones_comida.append(dir_name)

        return acciones_comida

    def mejor_accion(self, estado):
        """
        Devuelve la acción con mayor Q-value para ese estado.
        """
        q_values = {
            "UP": self.q_table.get((estado, "UP"), 0),
            "DOWN": self.q_table.get((estado, "DOWN"), 0),
            "LEFT": self.q_table.get((estado, "LEFT"), 0),
            "RIGHT": self.q_table.get((estado, "RIGHT"), 0),
        }

        max_q = max(q_values.values())
        mejores_acciones = [a for a, q in q_values.items() if q == max_q]
        return random.choice(mejores_acciones)

    def mejor_accion_segura(self, estado, vld_act):
        """
        Devuelve la mejor acción entre las válidas
        """
        q_values = {}
        for accion in vld_act:
            q_values[accion] = self.q_table.get((estado, accion), 0)

        max_q = max(q_values.values())
        mejores_acciones = [a for a, q in q_values.items() if q == max_q]
        return random.choice(mejores_acciones)

    def update_q_value(self, estado, accion, recompensa, siguiente_estado):
        """
        Actualiza Q-table usando la ecuación de Bellman.
        """
        if siguiente_estado is None:
            q_target = recompensa
        else:
            mejor_siguiente = max(
                self.q_table.get((siguiente_estado, a), 0)
                for a in ["UP", "DOWN", "LEFT", "RIGHT"]
            )
            q_target = recompensa + self.gamma * mejor_siguiente

        q_actual = self.q_table.get((estado, accion), 0)
        self.q_table[(estado, accion)] = q_actual + self.alpha * (
            q_target - q_actual
        )

        # Guardar experiencias exitosas
        if recompensa >= 10:
            self.replay_buffer.append(
                (estado, accion, recompensa, siguiente_estado)
            )
            if len(self.replay_buffer) > 100:
                self.replay_buffer.pop(0)

    def replay_experiences(self, num_replays=20):
        """
        Re-aprende de experiencias exitosas, priorizando las mejores
        """
        if len(self.replay_buffer) < 5:
            return

        # Ordenar por recompensa (mejores primero)
        sorted_buffer = sorted(
            self.replay_buffer, key=lambda x: x[2], reverse=True
        )

        for i in range(num_replays):
            # Tomar más de las mejores experiencias
            if i < num_replays // 2:
                idx = i % min(len(sorted_buffer) // 2, len(sorted_buffer))
                estado, accion, recompensa, siguiente_estado = sorted_buffer[
                    idx
                ]
            else:
                estado, accion, recompensa, siguiente_estado = random.choice(
                    self.replay_buffer
                )

            if siguiente_estado is None:
                q_target = recompensa
            else:
                mejor_siguiente = max(
                    self.q_table.get((siguiente_estado, a), 0)
                    for a in ["UP", "DOWN", "LEFT", "RIGHT"]
                )
                q_target = recompensa + self.gamma * mejor_siguiente

            q_actual = self.q_table.get((estado, accion), 0)
            self.q_table[(estado, accion)] = q_actual + self.alpha * (
                q_target - q_actual
            )

    def decay_epsilon(self):
        """
        Reduce epsilon después de cada episodio
        """
        self.epsilon *= 0.98
        self.epsilon = max(self.epsilon, 0.01)
