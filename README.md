# Learn2Slither - Snake con Q-Learning

Proyecto de Reinforcement Learning que entrena una serpiente para jugar Snake usando Q-learning.

## Estructura del Proyecto

```
.
├── main.py              # Programa principal con CLI
├── src/
│   ├── environment.py   # Tablero y lógica del juego
│   ├── interpreter.py   # Procesamiento del estado (visión de la serpiente)
│   ├── agent.py         # Agente con Q-learning
│   └── display.py       # Interfaz gráfica (opcional, requiere tkinter)
├── models/
│   ├── 1sess.txt        # Modelo entrenado con 1 sesión
│   ├── 10sess.txt       # Modelo entrenado con 10 sesiones
│   └── 100sess.txt      # Modelo entrenado con 100 sesiones
└── requirements.txt     # Dependencias del proyecto
```

## Instalación

```bash
pip install -r requirements.txt
```

**Nota:** La visualización gráfica requiere `tkinter`. Si no está disponible, el programa funcionará en modo texto.

## Uso

### Entrenar un nuevo modelo

```bash
# Entrenar 10 sesiones y guardar modelo
python3 main.py -sessions 10 -save models/nuevo.txt -visual off

# Entrenar con visualización
python3 main.py -sessions 5 -save models/visual.txt -visual on
```

### Cargar y probar un modelo existente

```bash
# Cargar modelo y ejecutar 5 sesiones de prueba (sin aprender)
python3 main.py -load models/100sess.txt -sessions 5 -dontlearn -visual on

# Modo paso a paso para depuración
python3 main.py -load models/10sess.txt -sessions 1 -dontlearn -visual on -step-by-step
```

### Continuar entrenamiento desde un modelo existente

```bash
# Cargar modelo y entrenar 50 sesiones más
python3 main.py -load models/100sess.txt -sessions 50 -save models/150sess.txt -visual off
```

## Argumentos de CLI

- `-sessions N`: Número de sesiones de entrenamiento/prueba
- `-save PATH`: Guardar modelo entrenado en ruta especificada
- `-load PATH`: Cargar modelo desde ruta especificada
- `-visual on|off`: Mostrar interfaz gráfica (default: off)
- `-dontlearn`: Modo testing (no actualiza Q-table)
- `-step-by-step`: Modo paso a paso (requiere -visual on)
- `-verbose on|off`: Mostrar información detallada (default: on)

## Resultados de Entrenamiento

### Modelo 1sess.txt (1 sesión)
- Q-table: 91 estados
- Mejor longitud: 9
- Manzanas verdes: 7

### Modelo 10sess.txt (10 sesiones)
- Q-table: 534 estados
- Mejor longitud: 24
- Manzanas verdes totales: 121

### Modelo 100sess.txt (100 sesiones)
- Q-table: 1225 estados
- **Mejor longitud: 42** ✅
- Manzanas verdes totales: 1378
- Promedio por sesión: ~13.8 manzanas

## Reglas del Juego

- **Tablero:** 10x10 celdas
- **Serpiente inicial:** 3 segmentos
- **Manzanas verdes (2):** +1 longitud, +10 recompensa
- **Manzanas rojas (1):** -1 longitud, -1 recompensa
- **Game Over:** Chocar con pared o con sí misma

## Implementación de Q-Learning

### Estado (State)
La serpiente solo ve en 4 direcciones desde su cabeza:
- `DANGER_IMM/NEAR/FAR`: Pared o cuerpo
- `FOOD_CLOSE/NEAR/FAR`: Manzana verde
- `BAD_CLOSE/FAR`: Manzana roja
- `SAFE`: Espacio vacío

### Acciones (Actions)
4 posibles: UP, DOWN, LEFT, RIGHT

### Recompensas (Rewards)
- Manzana verde: +10
- Manzana roja: -1
- Muerte: -10
- Proximidad a comida: +0.2 a +0.5

### Parámetros
- **Alpha (α):** 0.35 (learning rate)
- **Gamma (γ):** 0.95 (discount factor)
- **Epsilon:** Decay desde 1.0 → 0.01 (exploration rate)

### Técnicas Adicionales
- **Epsilon-greedy:** Exploración vs explotación
- **Replay buffer:** Re-aprendizaje de experiencias exitosas
- **Safe actions:** Evita peligros inmediatos durante exploración

## Objetivo Alcanzado

✅ **Longitud objetivo de 10 superada:** La serpiente alcanzó longitud 42 en el mejor caso.

## Autor

Proyecto Learn2Slither - 42 Madrid