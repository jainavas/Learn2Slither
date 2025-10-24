from src.environment import Board
from src.interpreter import Interpreter
from src.agent import Agent


def train(num_episodes=10, verbose=True):
    """
    Loop principal de entrenamiento.
    
    Args:
        num_episodes: número de sesiones de juego
        verbose: si imprime info de cada episodio
    """
    board = Board()
    interpreter = Interpreter(board)
    agent = Agent()
    
    total_green_apples = 0  # Contador total
    
    for episode in range(num_episodes):
        board.reset()
        
        # DEBUG: Ver primer estado
        if episode == 0:
            print("\n" + "=" * 50)
            print("=== DEBUG PRIMER EPISODIO ===")
            print("=" * 50)
            print("\nEstado visual completo:")
            print(interpreter.get_state())
            print("\nEstado comprimido:")
            estado_comp = interpreter.get_compressed_state()
            print(estado_comp)
            print("\nInterpretación del estado comprimido:")
            direcciones = ["UP", "DOWN", "LEFT", "RIGHT"]
            for i, dir_name in enumerate(direcciones):
                categoria = estado_comp[i]  # Ya no es tupla, es string
                print(f"  {dir_name}: {categoria}")
            print("=" * 50)
        
        estado = interpreter.get_compressed_state()
        game_over = False
        steps = 0
        max_length = 0
        green_apples_eaten = 0  # Por episodio
        
        while not game_over:
            # Agent elige acción
            accion = agent.seleccionar_accion(estado)
            
            # DEBUG: Ver decisiones en primer episodio
            if episode == 0 and steps < 5:
                print(f"\n--- Step {steps + 1} ---")
                print(f"Estado actual: {estado}")
                print(f"Acción elegida: {accion}")
                print(f"Epsilon actual: {agent.epsilon:.3f}")
            
            # Environment ejecuta acción
            recompensa, game_over = board.move_snake(accion)
            
            # Contar manzanas verdes
            if recompensa == 10:  # Actualizado a 100
                green_apples_eaten += 1
            
            # DEBUG: Ver resultado
            if episode == 0 and steps < 5:
                print(f"Recompensa recibida: {recompensa}")
                print(f"Game over: {game_over}")
                if not game_over:
                    print("\nNuevo estado comprimido:")
                    nuevo_estado = interpreter.get_compressed_state()
                    print(nuevo_estado)
                else:
                    print("\n¡GAME OVER! La serpiente murió.")
            
            # Obtener siguiente estado
            if game_over:
                siguiente_estado = None
            else:
                siguiente_estado = interpreter.get_compressed_state()
            
            # Agent aprende
            agent.update_q_value(estado, accion, recompensa, siguiente_estado)
            
            # Actualizar estado para siguiente iteración
            estado = siguiente_estado if siguiente_estado is not None else interpreter.get_compressed_state()
            
            steps += 1
            max_length = max(max_length, board.get_length())
            
            # Límite de pasos por episodio (evitar loops infinitos)
            if steps > 1000:
                game_over = True
        
        total_green_apples += green_apples_eaten
        
        # Replay de experiencias exitosas (si implementaste replay_buffer)
        if hasattr(agent, 'replay_experiences'):
            agent.replay_experiences(num_replays=10)
        
        # Reducir epsilon después de cada episodio
        agent.decay_epsilon()
        
        if verbose and (episode + 1) % max(1, num_episodes // 10) == 0:
            print(f"\nEpisode {episode + 1}/{num_episodes} | "
                  f"Length: {board.get_length()} | "
                  f"Max Length: {max_length} | "
                  f"Green apples: {green_apples_eaten} | "
                  f"Steps: {steps} | "
                  f"Epsilon: {agent.epsilon:.3f} | "
                  f"Q-table size: {len(agent.q_table)}")
    
    print(f"\nEntrenamiento completado. Q-table final: {len(agent.q_table)} estados")
    print(f"Total green apples eaten: {total_green_apples}/{num_episodes}")
    return agent


def test(agent, num_episodes=3, verbose=True):
    """
    Prueba el agente entrenado sin aprender (solo explotación).
    """
    board = Board()
    interpreter = Interpreter(board)
    
    # Guardar epsilon original y establecer a 0 (sin exploración)
    original_epsilon = agent.epsilon
    agent.epsilon = 0.05
    
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
            accion = agent.seleccionar_accion(estado)
            recompensa, game_over = board.move_snake(accion)
            
            if recompensa == 10:  # Manzana verde
                green_apples += 1
            
            if not game_over:
                estado = interpreter.get_compressed_state()
            
            steps += 1
            current_length = board.get_length()
            max_length_episode = max(max_length_episode, current_length)
            
            if steps > 5000:  # Límite aumentado
                game_over = True
        
        length = board.get_length()
        total_length += length
        total_steps += steps
        total_green_apples += green_apples
        max_length_achieved = max(max_length_achieved, max_length_episode)
        
        if verbose:
            print(f"Test Episode {episode + 1}/{num_episodes} | "
                  f"Final Length: {length} | "
                  f"Max Length: {max_length_episode} | "
                  f"Green Apples: {green_apples} | "
                  f"Steps: {steps}")
    
    avg_length = total_length / num_episodes
    avg_steps = total_steps / num_episodes
    avg_apples = total_green_apples / num_episodes
    
    print(f"\n=== RESULTADOS TESTING ===")
    print(f"Promedio - Length: {avg_length:.1f} | Steps: {avg_steps:.1f} | Apples: {avg_apples:.1f}")
    print(f"Mejor longitud alcanzada: {max_length_achieved}")
    
    # Restaurar epsilon
    agent.epsilon = original_epsilon


if __name__ == "__main__":
    print("=== TRAINING ===")
    trained_agent = train(num_episodes=100, verbose=True)
    
    print("\n=== TESTING ===")
    test(trained_agent, num_episodes=5, verbose=True)