
import pygame
from modulos.dibujado import verificar_click_boton
from modulos.logica import (
    verificar_respuesta, 
    procesar_respuesta_correcta, 
    procesar_respuesta_incorrecta,
    nueva_pregunta,
    usar_comodin
)
from modulos.archivos import agregar_puntaje, guardar_puntajes_json
from config.constantes import ARCHIVO_PUNTAJES


def procesar_eventos_menu(eventos):
    """
    Procesa eventos en el menú principal
    
    Args:
        eventos: lista de eventos de pygame
        
    Returns:
        Nueva pantalla o None si no hay cambio
    """
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return 'salir'
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if verificar_click_boton(250, 220, 400, 70, evento.pos):
                return 'seleccion_nivel'
            elif verificar_click_boton(250, 320, 400, 70, evento.pos):
                return 'historial'
            elif verificar_click_boton(250, 420, 400, 70, evento.pos):
                return 'salir'
    
    return None


def procesar_eventos_seleccion_nivel(eventos):
    """
    Procesa eventos en la selección de nivel
    
    Args:
        eventos: lista de eventos de pygame
        
    Returns:
        Tupla (nueva_pantalla, nivel_seleccionado) o (None, None)
    """
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return ('salir', None)
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if verificar_click_boton(250, 200, 400, 70, evento.pos):
                return ('jugando', 'facil')
            elif verificar_click_boton(250, 300, 400, 70, evento.pos):
                return ('jugando', 'medio')
            elif verificar_click_boton(250, 400, 400, 70, evento.pos):
                return ('jugando', 'dificil')
            elif verificar_click_boton(250, 520, 400, 60, evento.pos):
                return ('menu', None)
    
    return (None, None)


def procesar_eventos_juego(eventos, estado_juego, preguntas_nivel, puntajes):
    """
    Procesa eventos durante el juego
    
    Args:
        eventos: lista de eventos de pygame
        estado_juego: diccionario con el estado del juego
        preguntas_nivel: lista de preguntas del nivel actual
        puntajes: lista de puntajes
        
    Returns:
        Nueva pantalla o None si no hay cambio
    """
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return 'salir'
        
        # Eventos de teclado
        if evento.type == pygame.KEYDOWN:
            resultado = procesar_tecla(evento, estado_juego, preguntas_nivel, puntajes)
            if resultado:
                return resultado
        
        # Eventos de mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            resultado = procesar_click_juego(evento, estado_juego, preguntas_nivel, puntajes)
            if resultado:
                return resultado
    
    return None


def procesar_tecla(evento, estado_juego, preguntas_nivel, puntajes):
    """
    Procesa eventos de teclado durante el juego
    
    Args:
        evento: evento de pygame
        estado_juego: diccionario con el estado del juego
        preguntas_nivel: lista de preguntas del nivel actual
        puntajes: lista de puntajes
        
    Returns:
        Nueva pantalla o None
    """
    # ENTER: Verificar respuesta
    if evento.key == pygame.K_RETURN:
        if verificar_respuesta(estado_juego):
            procesar_respuesta_correcta(estado_juego)
        else:
            procesar_respuesta_incorrecta(estado_juego)
        
        # Verificar si perdi
        if estado_juego['vidas'] <= 0:
            estado_juego['gano'] = False  
            agregar_puntaje(puntajes, estado_juego['puntos'], estado_juego['nivel'])
            guardar_puntajes_json(ARCHIVO_PUNTAJES, puntajes)
            return 'game_over'
        else:
            # Intentar cargar nueva pregunta
            hay_pregunta = nueva_pregunta(estado_juego, preguntas_nivel)
            
            # Si no hay mas preguntas gana
            if not hay_pregunta: 
                estado_juego['gano'] = True  
                agregar_puntaje(puntajes, estado_juego['puntos'], estado_juego['nivel'])
                guardar_puntajes_json(ARCHIVO_PUNTAJES, puntajes)
                return 'game_over' 
    
   
    elif evento.key == pygame.K_BACKSPACE:
        estado_juego['respuesta_usuario'] = estado_juego['respuesta_usuario'][:-1]
    
    # Números y guión
    else:
        if evento.unicode in '0123456789-':
            if len(estado_juego['respuesta_usuario']) < 10:
                estado_juego['respuesta_usuario'] = estado_juego['respuesta_usuario'] + evento.unicode
    
    return None


def procesar_click_juego(evento, estado_juego, preguntas_nivel, puntajes):
    """
    Procesa clicks del mouse durante el juego
    
    Args:
        evento: evento de pygame
        estado_juego: diccionario con el estado del juego
        preguntas_nivel: lista de preguntas del nivel actual
        puntajes: lista de puntajes
        
    Returns:
        Nueva pantalla o None
    """
    # Verificar click en comodines
    i = 0
    while i < 3:
        x = 50 + i * 200
        y = 500
        if verificar_click_boton(x, y, 180, 50, evento.pos):
            if i not in estado_juego['comodines_usados']:
                usar_comodin(estado_juego, preguntas_nivel, i)
        i = i + 1
    
    # Verificar click en rendirse
    if verificar_click_boton(325, 600, 250, 50, evento.pos):
        estado_juego['gano'] = False  
        agregar_puntaje(puntajes, estado_juego['puntos'], estado_juego['nivel'])
        guardar_puntajes_json(ARCHIVO_PUNTAJES, puntajes)
        return 'game_over'
    
    return None


def procesar_eventos_historial(eventos):
    """
    Procesa eventos en el historial
    
    Args:
        eventos: lista de eventos de pygame
        
    Returns:
        Nueva pantalla o None
    """
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return 'salir'
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if verificar_click_boton(325, 620, 250, 50, evento.pos):
                return 'menu'
    
    return None


def procesar_eventos_game_over(eventos):
    """
    Procesa eventos en game over
    
    Args:
        eventos: lista de eventos de pygame
        
    Returns:
        Nueva pantalla o None
    """
    for evento in eventos:
        if evento.type == pygame.QUIT:
            return 'salir'
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if verificar_click_boton(250, 450, 400, 70, evento.pos):
                return 'seleccion_nivel'
            elif verificar_click_boton(250, 550, 400, 70, evento.pos):
                return 'menu'
    
    return None
