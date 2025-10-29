# Intentar importar librerías gráficas en orden de preferencia
try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

if not TKINTER_AVAILABLE and not PYGAME_AVAILABLE:
    print("Warning: No GUI library available (tkinter/pygame). Visual mode disabled.")


class Display:
    def __init__(self, board_size=10, cell_size=40, delay_ms=200):
        self.board_size = board_size
        self.cell_size = cell_size
        self.delay_ms = delay_ms
        self.enabled = True
        self.step_by_step = False
        self.waiting_for_step = False
        
        # Decidir qué backend usar
        if TKINTER_AVAILABLE:
            self.backend = 'tkinter'
        elif PYGAME_AVAILABLE:
            self.backend = 'pygame'
        else:
            self.backend = None
        
        # Variables específicas de cada backend
        self.window = None
        self.canvas = None
        self.screen = None
        self.clock = None
        self.info_label = None
        self.step_button = None
    
    def init_window(self):
        """Inicializa la ventana gráfica según el backend disponible"""
        if not self.enabled:
            return
        
        if self.backend == 'tkinter':
            self._init_tkinter()
        elif self.backend == 'pygame':
            self._init_pygame()
    
    def draw_board(self, board_obj, episode=0, steps=0):
        """Dibuja el estado actual del tablero"""
        if not self.enabled:
            return
        
        if self.backend == 'tkinter':
            self._draw_tkinter(board_obj, episode, steps)
        elif self.backend == 'pygame':
            self._draw_pygame(board_obj, episode, steps)
    
    def close(self):
        """Cierra la ventana"""
        if self.backend == 'tkinter':
            self._close_tkinter()
        elif self.backend == 'pygame':
            self._close_pygame()
    
    def set_speed(self, delay_ms):
        """Establece velocidad de actualización (en milisegundos)"""
        self.delay_ms = delay_ms
    
    # ========== BACKEND TKINTER ==========
    
    def _init_tkinter(self):
        """Inicializa ventana con tkinter"""
        if not TKINTER_AVAILABLE:
            return
        
        self.window = tk.Tk()
        self.window.title("Snake Game - Learn2Slither")
        
        # Canvas para el tablero
        canvas_width = self.board_size * self.cell_size
        canvas_height = self.board_size * self.cell_size
        
        self.canvas = tk.Canvas(
            self.window,
            width=canvas_width,
            height=canvas_height,
            bg='black'
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Info panel
        self.info_label = tk.Label(
            self.window,
            text="Episode: 0 | Length: 0 | Steps: 0",
            font=('Arial', 12),
            bg='lightgray',
            fg='black'
        )
        self.info_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Botón para step-by-step
        if self.step_by_step:
            self.step_button = tk.Button(
                self.window,
                text="Next Step",
                command=self._continue_step,
                font=('Arial', 10)
            )
            self.step_button.pack(pady=5)
        
        self.window.update()
    
    def _draw_tkinter(self, board_obj, episode, steps):
        """Dibuja el tablero con tkinter"""
        if self.canvas is None:
            return
        
        # Limpiar canvas
        self.canvas.delete("all")
        
        # Dibujar grid
        for i in range(self.board_size + 1):
            # Líneas verticales
            x = i * self.cell_size
            self.canvas.create_line(
                x, 0, x, self.board_size * self.cell_size,
                fill='gray30'
            )
            # Líneas horizontales
            y = i * self.cell_size
            self.canvas.create_line(
                0, y, self.board_size * self.cell_size, y,
                fill='gray30'
            )
        
        # Dibujar elementos del tablero
        board = board_obj.board
        for y in range(self.board_size):
            for x in range(self.board_size):
                cell_value = board[y][x]
                if cell_value != 0:
                    color = self._get_color(cell_value)
                    x1 = x * self.cell_size + 2
                    y1 = y * self.cell_size + 2
                    x2 = x1 + self.cell_size - 4
                    y2 = y1 + self.cell_size - 4
                    
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=color,
                        outline=color
                    )
        
        # Marcar la cabeza de la serpiente
        head_x, head_y = board_obj.get_head_position()
        x1 = head_x * self.cell_size + 2
        y1 = head_y * self.cell_size + 2
        x2 = x1 + self.cell_size - 4
        y2 = y1 + self.cell_size - 4
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill='cyan',
            outline='white',
            width=2
        )
        
        # Actualizar info
        length = board_obj.get_length()
        self.info_label.config(
            text=f"Episode: {episode} | Length: {length} | Steps: {steps}"
        )
        
        self.window.update()
        
        # Modo paso a paso
        if self.step_by_step:
            self.waiting_for_step = True
            while self.waiting_for_step:
                self.window.update()
                self.window.after(50)
        else:
            # Delay normal
            import time
            time.sleep(self.delay_ms / 1000.0)
    
    def _close_tkinter(self):
        """Cierra ventana tkinter"""
        if self.window:
            self.window.destroy()
            self.window = None
            self.canvas = None
    
    def _continue_step(self):
        """Callback para continuar en modo paso a paso"""
        self.waiting_for_step = False
    
    # ========== BACKEND PYGAME ==========
    
    def _init_pygame(self):
        """Inicializa ventana con pygame"""
        if not PYGAME_AVAILABLE:
            return
        
        pygame.init()
        
        # Dimensiones de la ventana
        window_width = self.board_size * self.cell_size
        window_height = self.board_size * self.cell_size + 60  # +60 para info panel
        
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Snake Game - Learn2Slither")
        
        self.clock = pygame.time.Clock()
        
        # Font para texto
        self.font = pygame.font.Font(None, 24)
    
    def _draw_pygame(self, board_obj, episode, steps):
        """Dibuja el tablero con pygame"""
        if self.screen is None:
            return
        
        # Procesar eventos de pygame (necesario para que no se cuelgue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                return
            # Modo paso a paso con SPACE
            if self.step_by_step and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.waiting_for_step = False
        
        # Limpiar pantalla
        self.screen.fill((0, 0, 0))  # Negro
        
        # Dibujar grid
        for i in range(self.board_size + 1):
            # Líneas verticales
            pygame.draw.line(
                self.screen,
                (50, 50, 50),  # Gris oscuro
                (i * self.cell_size, 0),
                (i * self.cell_size, self.board_size * self.cell_size),
                1
            )
            # Líneas horizontales
            pygame.draw.line(
                self.screen,
                (50, 50, 50),
                (0, i * self.cell_size),
                (self.board_size * self.cell_size, i * self.cell_size),
                1
            )
        
        # Dibujar elementos del tablero
        board = board_obj.board
        for y in range(self.board_size):
            for x in range(self.board_size):
                cell_value = board[y][x]
                if cell_value != 0:
                    color = self._get_color_rgb(cell_value)
                    rect = pygame.Rect(
                        x * self.cell_size + 2,
                        y * self.cell_size + 2,
                        self.cell_size - 4,
                        self.cell_size - 4
                    )
                    pygame.draw.rect(self.screen, color, rect)
        
        # Marcar la cabeza de la serpiente
        head_x, head_y = board_obj.get_head_position()
        head_rect = pygame.Rect(
            head_x * self.cell_size + 2,
            head_y * self.cell_size + 2,
            self.cell_size - 4,
            self.cell_size - 4
        )
        pygame.draw.rect(self.screen, (0, 255, 255), head_rect)  # Cyan
        pygame.draw.rect(self.screen, (255, 255, 255), head_rect, 2)  # Borde blanco
        
        # Panel de información
        length = board_obj.get_length()
        info_text = f"Episode: {episode} | Length: {length} | Steps: {steps}"
        
        # Fondo del panel
        info_rect = pygame.Rect(0, self.board_size * self.cell_size, 
                                self.board_size * self.cell_size, 60)
        pygame.draw.rect(self.screen, (200, 200, 200), info_rect)
        
        # Texto
        text_surface = self.font.render(info_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(
            self.board_size * self.cell_size // 2,
            self.board_size * self.cell_size + 20
        ))
        self.screen.blit(text_surface, text_rect)
        
        # Instrucción para step-by-step
        if self.step_by_step:
            step_text = "Press SPACE for next step"
            step_surface = self.font.render(step_text, True, (0, 0, 0))
            step_rect = step_surface.get_rect(center=(
                self.board_size * self.cell_size // 2,
                self.board_size * self.cell_size + 45
            ))
            self.screen.blit(step_surface, step_rect)
        
        # Actualizar pantalla
        pygame.display.flip()
        
        # Modo paso a paso
        if self.step_by_step:
            self.waiting_for_step = True
            while self.waiting_for_step:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.close()
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.waiting_for_step = False
                pygame.time.wait(50)
        else:
            # Delay normal
            pygame.time.wait(self.delay_ms)
    
    def _close_pygame(self):
        """Cierra ventana pygame"""
        if PYGAME_AVAILABLE and self.screen:
            pygame.quit()
            self.screen = None
    
    # ========== HELPERS ==========
    
    def _get_color(self, cell_value):
        """Devuelve el color según el tipo de celda (para tkinter)"""
        colors = {
            1: 'blue',      # Serpiente
            2: 'green',     # Manzana verde
            3: 'red'        # Manzana roja
        }
        return colors.get(cell_value, 'white')
    
    def _get_color_rgb(self, cell_value):
        """Devuelve el color RGB según el tipo de celda (para pygame)"""
        colors = {
            1: (0, 0, 255),      # Serpiente (azul)
            2: (0, 255, 0),      # Manzana verde
            3: (255, 0, 0)       # Manzana roja
        }
        return colors.get(cell_value, (255, 255, 255))