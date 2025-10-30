import random


class Board:
    def __init__(self):
        self.segments = []  # (x, y)
        self.board = [[0 for _ in range(10)] for _ in range(10)]
        self.direction = "UP"
        self.len = 0
        self.game_over = False
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
        "RIGHT": (1, 0),
    }

    def is_valid_position(self, new_x, new_y):
        return 0 <= new_x < 10 and 0 <= new_y < 10

    def move_snake(self, direction):
        dx, dy = self.DIRECTIONS[direction]
        new_x = self.segments[0][0] + dx
        new_y = self.segments[0][1] + dy

        # 1. PRIMERO: Validar límites del tablero
        if not self.is_valid_position(new_x, new_y):
            self.game_over = True
            return -10, self.game_over

        # 2. SEGUNDO: Ver qué hay en la nueva posición ANTES de moverse
        val = self.board[new_y][new_x]

        # 3. TERCERO: Validar colisión con cuerpo
        if val == 1:  # Es parte de la serpiente
            self.game_over = True
            return -10, self.game_over

        # 4. AHORA SÍ: Mover la cabeza
        self.segments.insert(0, (new_x, new_y))
        self.board[new_y][new_x] = 1

        # 5. Procesar según qué comió
        if val == 2:  # Manzana verde
            self.len += 1
            self.snk_eats_apple(2)
            return 10, self.game_over  # Recompensa alta

        elif val == 3:  # Manzana roja
            # Reducir longitud (eliminar 2 segmentos)
            for _ in range(2):
                if len(self.segments) > 1:
                    tail_x, tail_y = self.segments[-1]
                    self.board[tail_y][tail_x] = 0
                    self.segments.pop()

            self.len -= 1
            self.snk_eats_apple(3)

            if self.len <= 0:
                self.game_over = True
                return -10, self.game_over
            else:
                return -1, self.game_over
        else:  # Casilla vacía (val == 0)
            # Eliminar la cola
            tail_x, tail_y = self.segments[-1]
            self.board[tail_y][tail_x] = 0
            self.segments.pop()
            reward_pos = self._calcular_bonus_proximidad(new_x, new_y)
            return reward_pos, self.game_over

    def reset(self):
        self.board = [[0 for _ in range(10)] for _ in range(10)]
        self.len = 3
        self.game_over = False
        self.segments = []
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if self.board[y][x] == 0:
                break
        for direction_name, (dx, dy) in self.DIRECTIONS.items():
            if self.is_valid_position(x + dx * 2, y + dy * 2):
                self.segments.insert(0, (x, y))
                self.segments.insert(0, (x + dx, y + dy))
                self.segments.insert(0, (x + dx * 2, y + dy * 2))
                self.board[y + dy * 2][x + dx * 2] = 1
                self.board[y + dy][x + dx] = 1
                self.board[y][x] = 1

                self.direction = direction_name
                break
        self.snk_eats_apple(2)
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

    def _calcular_bonus_proximidad(self, head_x, head_y):
        """
        Da pequeño bonus si la cabeza está cerca de una manzana verde
        """
        min_dist = float("inf")

        # Encontrar manzana verde más cercana
        for y in range(10):
            for x in range(10):
                if self.board[y][x] == 2:  # Manzana verde
                    dist = abs(head_x - x) + abs(head_y - y)  # Distancia
                    min_dist = min(min_dist, dist)

        # Bonus muy pequeño basado en proximidad
        if min_dist <= 2:
            return 0.5
        elif min_dist <= 4:
            return 0.2
        else:
            return 0
