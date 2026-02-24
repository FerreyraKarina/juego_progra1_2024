import random


def bubble_sort_puntajes(puntajes):
    """
    Ordena los puntajes de mayor a menor usando Bubble Sort
    
    Args:
        puntajes: lista de diccionarios con puntajes
        
    Returns:
        Lista ordenada de puntajes
    """
    n = len(puntajes)
    
    i = 0
    while i < n:
        j = 0
        while j < n - i - 1:
            if puntajes[j]['puntos'] < puntajes[j + 1]['puntos']:
                # Intercambiar
                temp = puntajes[j]
                puntajes[j] = puntajes[j + 1]
                puntajes[j + 1] = temp
            j = j + 1
        i = i + 1
    
    return puntajes


def obtener_top_10(puntajes):
    """
    Obtiene los 10 mejores puntajes
    
    Args:
        puntajes: lista de puntajes
        
    Returns:
        Lista con los 10 mejores puntajes
    """
    puntajes_ordenados = bubble_sort_puntajes(puntajes)
    
    top_10 = []
    i = 0
    while i < 10 and i < len(puntajes_ordenados):
        top_10.append(puntajes_ordenados[i])
        i = i + 1
    
    return top_10


def filtrar_preguntas_por_nivel(preguntas, nivel):
    """
    Filtra las preguntas por nivel de dificultad
    
    Args:
        preguntas: lista completa de preguntas
        nivel: 'facil', 'medio' o 'dificil'
        
    Returns:
        Lista de preguntas del nivel especificado
    """
    preguntas_filtradas = []
    
    i = 0
    while i < len(preguntas):
        if preguntas[i]['nivel'] == nivel:
            preguntas_filtradas.append(preguntas[i])
        i = i + 1
    
    return preguntas_filtradas


def obtener_pregunta_aleatoria(preguntas, preguntas_usadas):
    """
    Obtiene una pregunta aleatoria que no haya sido usada
    
    Args:
        preguntas: lista de preguntas disponibles
        preguntas_usadas: set de índices de preguntas usadas
        
    Returns:
        Diccionario con la pregunta o None si se terminaron todas
    """
    # Si se terminaron todas las preguntas, retornar None (Victoria)
    if len(preguntas_usadas) >= len(preguntas):
        return None
    
    preguntas_disponibles = []
    i = 0
    while i < len(preguntas):
        if i not in preguntas_usadas:
            preguntas_disponibles.append({'pregunta': preguntas[i], 'indice': i})
        i = i + 1
    
    if len(preguntas_disponibles) == 0:
        return None
    
    pregunta_seleccionada = random.choice(preguntas_disponibles)
    preguntas_usadas.add(pregunta_seleccionada['indice'])
    
    return pregunta_seleccionada['pregunta']
