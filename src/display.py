try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("Warning: tkinter not available. Visual mode disabled.")


class Display:
    def __init__(self, board_size=10, cell_size=40, delay_ms=200):
        self.board_size = board_size
        self.cell_size = cell_size
        self.window = None
        self.canvas = None
        self.enabled = True
        self.step_by_step = False
        self.waiting_for_step = False
        self.delay_ms = delay_ms  # Delay entre frames en milisegundos

    def init_window(self):
        """Inicializa la ventana gráfica"""
        if not self.enabled or not TKINTER_AVAILABLE:
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

    def _continue_step(self):
        """Callback para continuar en modo paso a paso"""
        self.waiting_for_step = False

    def draw_board(self, board_obj, episode=0, steps=0):
        """Dibuja el estado actual del tablero"""
        if not self.enabled or self.canvas is None:
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
            # Delay normal para que se pueda ver la animación
            import time
            time.sleep(self.delay_ms / 1000.0)

    def _get_color(self, cell_value):
        """Devuelve el color según el tipo de celda"""
        colors = {
            1: 'blue',      # Serpiente
            2: 'green',     # Manzana verde
            3: 'red'        # Manzana roja
        }
        return colors.get(cell_value, 'white')

    def close(self):
        """Cierra la ventana"""
        if self.window:
            self.window.destroy()
            self.window = None
            self.canvas = None

    def set_speed(self, delay_ms):
        """Establece velocidad de actualización (en milisegundos)"""
        if self.window:
            self.window.after(delay_ms)