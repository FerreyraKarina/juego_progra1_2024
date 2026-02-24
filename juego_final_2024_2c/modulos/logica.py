
import pygame
from config.constantes import TIEMPO_PREGUNTA, VERDE, ROJO, AZUL, AMARILLO
from modulos.algoritmos import obtener_pregunta_aleatoria


def actualizar_tiempo(estado_juego):
    """
    Actualiza el tiempo restante
    
    Args:
        estado_juego: diccionario con el estado del juego
        
    Returns:
        True si el tiempo se agotó, False si aún hay tiempo
    """
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = (tiempo_actual - estado_juego['tiempo_inicio']) / 1000
    
    # Tiempo total = tiempo base + tiempo extra de comodines
    tiempo_total = TIEMPO_PREGUNTA + estado_juego['tiempo_extra']
    estado_juego['tiempo_restante'] = tiempo_total - tiempo_transcurrido
    
    if estado_juego['tiempo_restante'] <= 0:
        estado_juego['tiempo_restante'] = 0
        return True  # Tiempo agotado
    
    return False


def verificar_respuesta(estado_juego):
  
    """Verifica si la respuesta del usuario es correcta"""
    
    es_correcta = False
    

    if estado_juego['pregunta_actual']:
      
        respuesta_correcta = estado_juego['pregunta_actual']['respuesta']
        respuesta_correcta = respuesta_correcta.strip()
        
        respuesta_usuario = estado_juego['respuesta_usuario']
        respuesta_usuario = respuesta_usuario.strip()
        

        if respuesta_usuario == respuesta_correcta:
            es_correcta = True
        else:
            es_correcta = False
    else:
        es_correcta = False
    
    return es_correcta




def procesar_respuesta_correcta(estado_juego):
    """
    Procesa una respuesta correcta
    
    
    Args:
        estado_juego: diccionario con el estado del juego
    """
    estado_juego['puntos'] = estado_juego['puntos'] + 1
    
    estado_juego['mensaje'] = f"¡CORRECTO! +1  punto"
    estado_juego['color_mensaje'] = AMARILLO
    estado_juego['mostrar_mensaje'] = True # no muestra el mensaje
    estado_juego['tiempo_mensaje'] = pygame.time.get_ticks()


def procesar_respuesta_incorrecta(estado_juego):
    """
    Procesa una respuesta incorrecta
    
    Args:
        estado_juego: diccionario con el estado del juego
    """
    estado_juego['vidas'] = estado_juego['vidas'] - 1
    
    respuesta_correcta = estado_juego['pregunta_actual']['respuesta']
    estado_juego['mensaje'] = f"INCORRECTO. Era: {respuesta_correcta}"
    estado_juego['color_mensaje'] = ROJO
    estado_juego['mostrar_mensaje'] = True
    estado_juego['tiempo_mensaje'] = pygame.time.get_ticks()


def nueva_pregunta(estado_juego, preguntas_nivel):
    """
    Carga una nueva pregunta
    
    Args:
        estado_juego: diccionario con el estado del juego
        preguntas_nivel: lista de preguntas del nivel actual
        
    Returns:
        True si hay pregunta disponible, False si se terminaron todas (Victoria)
    """
    pregunta = obtener_pregunta_aleatoria(
        preguntas_nivel, 
        estado_juego['preguntas_usadas']
    )
    
    # Si no hay más preguntas, el jugador ganó
    if pregunta is None:
        return False
    
    estado_juego['pregunta_actual'] = pregunta
    estado_juego['respuesta_usuario'] = ""
    estado_juego['tiempo_inicio'] = pygame.time.get_ticks()
    estado_juego['tiempo_restante'] = TIEMPO_PREGUNTA
    estado_juego['tiempo_extra'] = 0
    estado_juego['mostrar_mensaje'] = False
    
    return True


def usar_comodin(estado_juego, preguntas_nivel, indice_comodin):
    """
    Usa un comodín según su tipo
    
    Args:
        estado_juego: diccionario con el estado del juego
        preguntas_nivel: lista de preguntas del nivel actual
        indice_comodin: 0 (Cambiar), 1 (Pista), 2 (+5seg)
    """
    # Verificar que se puede usar
    if estado_juego['comodines'] > 0 and indice_comodin not in estado_juego['comodines_usados']:
        
        # Validación para comodín de tiempo
        if indice_comodin == 2 and estado_juego['tiempo_restante'] <= 0:
            estado_juego['mensaje'] = "¡Tiempo agotado!"
            estado_juego['color_mensaje'] = ROJO
            estado_juego['mostrar_mensaje'] = True
            estado_juego['tiempo_mensaje'] = pygame.time.get_ticks()
            return
        
        # Marcar como usado
        estado_juego['comodines'] = estado_juego['comodines'] - 1
        estado_juego['comodines_usados'].append(indice_comodin)
        
        # COMODÍN 0: Cambiar Pregunta
        if indice_comodin == 0:
            nueva_pregunta(estado_juego, preguntas_nivel)
            estado_juego['mensaje'] = "¡Nueva pregunta!"
            estado_juego['color_mensaje'] = AZUL
            estado_juego['mostrar_mensaje'] = True
            estado_juego['tiempo_mensaje'] = pygame.time.get_ticks()
        
        # COMODÍN 1: Mostrar Pista
        elif indice_comodin == 1:
            if estado_juego['pregunta_actual']:
                respuesta = estado_juego['pregunta_actual']['respuesta']
                mitad = len(respuesta) // 2
                if mitad > 0:
                    pista = respuesta[:mitad]
                else:
                    pista = respuesta[0]
                
                estado_juego['mensaje'] = f"Pista: {pista}..."
                estado_juego['color_mensaje'] = AMARILLO
                estado_juego['mostrar_mensaje'] = True
                estado_juego['tiempo_mensaje'] = pygame.time.get_ticks()
        
        # COMODÍN 2: +5 Segundos
        elif indice_comodin == 2:
            estado_juego['tiempo_extra'] = estado_juego['tiempo_extra'] + 5
            
            # Límite máximo: 15 segundos totales
            tiempo_total = TIEMPO_PREGUNTA + estado_juego['tiempo_extra']
            if tiempo_total > 15:
                estado_juego['tiempo_extra'] = 15 - TIEMPO_PREGUNTA
            
            estado_juego['mensaje'] = "¡+5 segundos!"
            estado_juego['color_mensaje'] = VERDE
            estado_juego['mostrar_mensaje'] = True
            estado_juego['tiempo_mensaje'] = pygame.time.get_ticks()


# def ocultar_mensaje_si_necesario(estado_juego):
#     """
#     Oculta el mensaje después de 2 segundos
    
#     Args:
#         estado_juego: diccionario con el estado del juego
#     """
#     if estado_juego['mostrar_mensaje']:
#         tiempo_actual = pygame.time.get_ticks()
#         if tiempo_actual - estado_juego['tiempo_mensaje'] > 2000:
#             estado_juego['mostrar_mensaje'] = False
