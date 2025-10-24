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
    
    for episode in range(num_episodes):
        board.reset()
        estado = interpreter.get_state()
        game_over = False
        steps = 0
        max_length = 0
        
        while not game_over:
            # Agent elige acción
            accion = agent.seleccionar_accion(estado)
            
            # Environment ejecuta acción
            recompensa, game_over = board.move_snake(accion)
            
            # Obtener siguiente estado
            if game_over:
                siguiente_estado = None
            else:
                siguiente_estado = interpreter.get_state()
            
            # Agent aprende
            agent.update_q_value(estado, accion, recompensa, siguiente_estado)
            
            # Actualizar estado para siguiente iteración
            estado = siguiente_estado if siguiente_estado is not None else interpreter.get_state()
            
            steps += 1
            max_length = max(max_length, board.get_length())
            
            # Límite de pasos por episodio (evitar loops infinitos)
            if steps > 1000:
                game_over = True
        
        # Reducir epsilon después de cada episodio
        agent.decay_epsilon()
        
        if verbose and (episode + 1) % max(1, num_episodes // 10) == 0:
            print(f"Episode {episode + 1}/{num_episodes} | "
                  f"Length: {board.get_length()} | "
                  f"Max Length: {max_length} | "
                  f"Steps: {steps} | "
                  f"Epsilon: {agent.epsilon:.3f} | "
                  f"Q-table size: {len(agent.q_table)}")
    
    print(f"\nEntrenamiento completado. Q-table final: {len(agent.q_table)} estados")
    return agent


def test(agent, num_episodes=3, verbose=True):
    """
    Prueba el agente entrenado sin aprender (solo explotación).
    """
    board = Board()
    interpreter = Interpreter(board)
    
    # Guardar epsilon original y establecer a 0 (sin exploración)
    original_epsilon = agent.epsilon
    agent.epsilon = 0.0
    
    total_length = 0
    total_steps = 0
    
    for episode in range(num_episodes):
        board.reset()
        estado = interpreter.get_state()
        game_over = False
        steps = 0
        
        while not game_over:
            accion = agent.seleccionar_accion(estado)
            recompensa, game_over = board.move_snake(accion)
            
            if not game_over:
                estado = interpreter.get_state()
            
            steps += 1
            if steps > 1000:
                game_over = True
        
        length = board.get_length()
        total_length += length
        total_steps += steps
        
        if verbose:
            print(f"Test Episode {episode + 1}/{num_episodes} | "
                  f"Final Length: {length} | Steps: {steps}")
    
    avg_length = total_length / num_episodes
    avg_steps = total_steps / num_episodes
    print(f"\nPromedio - Length: {avg_length:.1f} | Steps: {avg_steps:.1f}")
    
    # Restaurar epsilon
    agent.epsilon = original_epsilon


if __name__ == "__main__":
    print("=== TRAINING ===")
    trained_agent = train(num_episodes=100, verbose=True)
    
    print("\n=== TESTING ===")
    test(trained_agent, num_episodes=5, verbose=True)