from pynput import mouse
import time
import keyboard
import random

# Dimensiones de la ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Número de objetivos
NUM_TARGETS = 10

def generate_random_targets(num_targets, width, height):
    """
    Genera coordenadas aleatorias para los objetivos dentro de los límites de la ventana.
    
    Args:
        num_targets (int): Número de objetivos a generar.
        width (int): Ancho de la ventana.
        height (int): Alto de la ventana.
    
    Returns:
        list: Lista de coordenadas de los objetivos.
    """
    targets = []
    for _ in range(num_targets):
        x = random.randint(0, width)
        y = random.randint(0, height)
        targets.append((x, y))
    return targets

def on_click(x, y, button, pressed, stats, training_active, targets):
    """
    Función que maneja los eventos de clic del mouse.
    
    Args:
        x (int): Coordenada x del clic.
        y (int): Coordenada y del clic.
        button (pynput.mouse.Button): Botón del mouse presionado.
        pressed (bool): Indica si el botón fue presionado o soltado.
        stats (dict): Diccionario con las estadísticas del entrenamiento.
        training_active (bool): Indica si el entrenamiento está activo.
        targets (list): Lista de coordenadas de los objetivos.
    """
    if pressed and training_active:
        stats['total_clicks'] += 1
        if (x, y) in targets:
            stats['successful_clicks'] += 1
            print(f'Successful click at ({x}, {y})')
        else:
            print(f'Missed click at ({x}, {y})')
        
        # Calcular el tiempo transcurrido
        elapsed_time = time.time() - stats['start_time']
        print(f'Elapsed time: {elapsed_time:.2f} seconds')
        
        # Calcular la precisión
        accuracy = (stats['successful_clicks'] / stats['total_clicks']) * 100 if stats['total_clicks'] > 0 else 0
        print(f'Accuracy: {accuracy:.2f}%')
        
        # Calcular la velocidad de clicks
        if elapsed_time > 0:
            click_speed = stats['total_clicks'] / elapsed_time
            print(f'Click speed: {click_speed:.2f} clicks per second')

def start_training():
    """
    Inicia el entrenamiento de aim.
    """
    stats = {
        'total_clicks': 0,
        'successful_clicks': 0,
        'start_time': time.time()
    }
    training_active = False
    targets = generate_random_targets(NUM_TARGETS, WINDOW_WIDTH, WINDOW_HEIGHT)

    def toggle_training():
        nonlocal training_active
        training_active = not training_active
        if training_active:
            print("Aim training started. Press F8 to stop.")
            stats['start_time'] = time.time()
        else:
            print("Aim training stopped.")
            show_final_stats(stats)

    # Iniciar el listener del mouse
    with mouse.Listener(on_click=lambda x, y, button, pressed: on_click(x, y, button, pressed, stats, training_active, targets)) as listener:
        try:
            keyboard.add_hotkey('F8', toggle_training)
            print("Press F8 to start the aim training.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            listener.stop()
            print("\nTraining interrupted by user.")
        finally:
            keyboard.remove_hotkey('F8')

def show_final_stats(stats):
    """
    Muestra las estadísticas finales del entrenamiento.
    
    Args:
        stats (dict): Diccionario con las estadísticas del entrenamiento.
    """
    print("\nTraining completed!")
    print(f'Total clicks: {stats["total_clicks"]}')
    print(f'Successful clicks: {stats["successful_clicks"]}')
    accuracy = (stats['successful_clicks'] / stats['total_clicks']) * 100 if stats['total_clicks'] > 0 else 0
    print(f'Final accuracy: {accuracy:.2f}%')
    elapsed_time = time.time() - stats['start_time']
    print(f'Total elapsed time: {elapsed_time:.2f} seconds')
    if elapsed_time > 0:
        click_speed = stats['total_clicks'] / elapsed_time
        print(f'Final click speed: {click_speed:.2f} clicks per second')

if __name__ == "__main__":
    start_training()