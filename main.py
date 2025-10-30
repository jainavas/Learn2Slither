import argparse
import json
from src.environment import Board
from src.interpreter import Interpreter
from src.agent import Agent
from src.display import Display


def train(
    agent,
    board,
    interpreter,
    display,
    num_episodes=10,
    verbose=True,
    show_visual=False,
    save_path=None,
):
    """
    Loop principal de entrenamiento.

    Args:
        agent: Agente con Q-learning
        board: Tablero del juego
        interpreter: Intérprete del estado
        display: Objeto de visualización
        num_episodes: número de sesiones de juego
        verbose: si imprime info de cada episodio
        show_visual: si muestra la interfaz gráfica
        save_path: ruta donde guardar el modelo
    """
    if show_visual and display.enabled:
        display.init_window()

    total_green_apples = 0
    best_length = 0

    for episode in range(num_episodes):
        board.reset()
        estado = interpreter.get_compressed_state()
        game_over = False
        steps = 0
        max_length = 0
        green_apples_eaten = 0

        while not game_over:
            # Mostrar estado visual
            if show_visual and display.enabled:
                display.draw_board(board, episode + 1, steps)

            # Agent elige acción
            accion = agent.seleccionar_accion(estado)

            # Environment ejecuta acción
            recompensa, game_over = board.move_snake(accion)

            # Contar manzanas verdes
            if recompensa == 10:
                green_apples_eaten += 1

            # Obtener siguiente estado
            if game_over:
                siguiente_estado = None
            else:
                siguiente_estado = interpreter.get_compressed_state()

            # Agent aprende
            agent.update_q_value(estado, accion, recompensa, siguiente_estado)

            # Actualizar estado para siguiente iteración
            estado = (
                siguiente_estado
                if siguiente_estado is not None
                else interpreter.get_compressed_state()
            )

            steps += 1
            max_length = max(max_length, board.get_length())

            # Límite de pasos por episodio
            if steps > 1000:
                game_over = True

        total_green_apples += green_apples_eaten
        best_length = max(best_length, max_length)

        # Replay de experiencias exitosas
        if hasattr(agent, "replay_experiences"):
            agent.replay_experiences(num_replays=10)

        # Reducir epsilon después de cada episodio
        agent.decay_epsilon()

        if verbose and (episode + 1) % max(1, num_episodes // 10) == 0:
            print(
                f"Episode {episode + 1}/{num_episodes} | "
                f"Length: {board.get_length()} | "
                f"Max Length: {max_length} | "
                f"Green apples: {green_apples_eaten} | "
                f"Steps: {steps} | "
                f"Epsilon: {agent.epsilon:.3f} | "
                f"Q-table size: {len(agent.q_table)}"
            )

    print("\nEntrenamiento completado. Q-table final: ")
    print(f"{len(agent.q_table)} estados")
    print(f"Total green apples eaten: {total_green_apples}/{num_episodes}")
    print(f"Best length achieved: {best_length}")

    # Guardar modelo si se especifica
    if save_path:
        save_model(agent, save_path)
        print(f"Save learning state in {save_path}")

    if show_visual and display.enabled:
        display.close()

    return agent


def test(agent, num_episodes=3, verbose=True, show_visual=False, delay_ms=200):
    """
    Prueba el agente entrenado sin aprender (solo explotación).
    """
    board = Board()
    interpreter = Interpreter(board)
    display = Display(delay_ms=delay_ms)

    if show_visual:
        display.init_window()

    # Guardar epsilon original y establecer a 0 (sin exploración)
    original_epsilon = agent.epsilon
    agent.epsilon = 0.05  # Dejar un minimo de exploracion para evitar bucles
    total_length = 0
    total_steps = 0
    total_green_apples = 0
    max_length_achieved = 0

    for episode in range(num_episodes):
        board.reset()
        estado = interpreter.get_compressed_state()
        game_over = False
        steps = 0
        green_apples = 0
        max_length_episode = 3

        while not game_over:
            if show_visual:
                display.draw_board(board, episode + 1, steps)

            accion = agent.seleccionar_accion(estado)
            recompensa, game_over = board.move_snake(accion)

            if recompensa == 10:
                green_apples += 1

            if not game_over:
                estado = interpreter.get_compressed_state()

            steps += 1
            current_length = board.get_length()
            max_length_episode = max(max_length_episode, current_length)

            if steps > 5000:
                game_over = True

        length = board.get_length()
        total_length += length
        total_steps += steps
        total_green_apples += green_apples
        max_length_achieved = max(max_length_achieved, max_length_episode)

        if verbose:
            print(
                f"Test Episode {episode + 1}/{num_episodes} | "
                f"Final Length: {length} | "
                f"Max Length: {max_length_episode} | "
                f"Green Apples: {green_apples} | "
                f"Steps: {steps}"
            )

    avg_length = total_length / num_episodes
    avg_steps = total_steps / num_episodes
    avg_apples = total_green_apples / num_episodes

    print("\n=== RESULTADOS TESTING ===")
    print(
        f"Promedio - Length: {avg_length:.1f} | "
        f"Steps: {avg_steps:.1f} | Apples: {avg_apples:.1f}"
    )
    print(f"Mejor longitud alcanzada: {max_length_achieved}")

    # Restaurar epsilon
    agent.epsilon = original_epsilon

    if show_visual:
        display.close()


def save_model(agent, filepath):
    """Guarda el modelo (Q-table) en un archivo"""
    model_data = {
        "q_table": {str(k): v for k, v in agent.q_table.items()},
        "epsilon": agent.epsilon,
        "alpha": agent.alpha,
        "gamma": agent.gamma,
    }

    with open(filepath, "w") as f:
        json.dump(model_data, f, indent=2)


def load_model(agent, filepath):
    """Carga el modelo (Q-table) desde un archivo"""
    with open(filepath, "r") as f:
        model_data = json.load(f)

    # Reconstruir Q-table (las keys son tuplas)
    agent.q_table = {}
    for key_str, value in model_data["q_table"].items():
        # Convertir string de vuelta a tupla
        key = eval(key_str)
        agent.q_table[key] = value

    agent.epsilon = model_data.get("epsilon", agent.epsilon)
    agent.alpha = model_data.get("alpha", agent.alpha)
    agent.gamma = model_data.get("gamma", agent.gamma)

    print(f"Load trained model from {filepath}")
    print(f"Q-table size: {len(agent.q_table)} estados")


def main():
    parser = argparse.ArgumentParser(description="Learn2Slither")

    parser.add_argument(
        "-sessions",
        type=int,
        default=1,
        help="Número de sesiones de entrenamiento",
    )
    parser.add_argument(
        "-save",
        type=str,
        default=None,
        help="Guardar modelo en ruta especificada",
    )
    parser.add_argument(
        "-load",
        type=str,
        default=None,
        help="Cargar modelo desde ruta especificada",
    )
    parser.add_argument(
        "-visual",
        type=str,
        default="off",
        choices=["on", "off"],
        help="Mostrar interfaz gráfica",
    )
    parser.add_argument(
        "-dontlearn",
        action="store_true",
        help="No aprender, solo ejecutar (testing)",
    )
    parser.add_argument(
        "-step-by-step",
        action="store_true",
        help="Modo paso a paso",
    )
    parser.add_argument(
        "-verbose",
        type=str,
        default="on",
        choices=["on", "off"],
        help="Mostrar información detallada",
    )
    parser.add_argument(
        "-speed",
        type=int,
        default=200,
        help="Velocidad de visualización en ms \
            (default: 200, más bajo = más rápido)",
    )

    args = parser.parse_args()

    # Configurar agente
    agent = Agent()

    # Cargar modelo si se especifica
    if args.load:
        load_model(agent, args.load)

    # Configurar visualización
    show_visual = args.visual == "on"
    verbose = args.verbose == "on"

    # Modo testing (sin aprender)
    if args.dontlearn:
        print("=== TESTING MODE (no learning) ===")
        test(
            agent,
            num_episodes=args.sessions,
            verbose=verbose,
            show_visual=show_visual,
            delay_ms=args.speed,
        )
    else:
        # Modo entrenamiento
        print("=== TRAINING MODE ===")
        board = Board()
        interpreter = Interpreter(board)
        display = Display(delay_ms=args.speed)
        display.enabled = show_visual
        display.step_by_step = args.step_by_step

        train(
            agent,
            board,
            interpreter,
            display,
            num_episodes=args.sessions,
            verbose=verbose,
            show_visual=show_visual,
            save_path=args.save,
        )


if __name__ == "__main__":
    main()
