
import pygame
from config.constantes import TIEMPO_PREGUNTA, NEGRO


def crear_estado_juego(nivel):
    """
    Crea un nuevo estado de juego
    
    Args:
        nivel: 'facil', 'medio' o 'dificil'
        
    Returns:
        Diccionario con el estado inicial del juego
    """
    return {
        'vidas': 3,
        'comodines': 3,
        'comodines_usados': [],
        'puntos': 0,
        'tiempo_restante': TIEMPO_PREGUNTA,
        'tiempo_extra': 0,
        'pregunta_actual': None,
        'respuesta_usuario': "",
        'mensaje': "",
        'color_mensaje': NEGRO,
        'tiempo_inicio': pygame.time.get_ticks(),
        'mostrar_mensaje': False,
        'tiempo_mensaje': 0,
        'nivel': nivel,
        'preguntas_usadas': set(),
        'gano': False 
    }


def reiniciar_estado(estado_juego):
    """
    Reinicia el estado del juego manteniendo el nivel
    
    Args:
        estado_juego: diccionario con el estado actual
    """
    nivel = estado_juego['nivel']
    nuevo_estado = crear_estado_juego(nivel)
    
    # Copiar todos los campos del nuevo estado al estado actual
    for clave in nuevo_estado:
        estado_juego[clave] = nuevo_estado[clave]
