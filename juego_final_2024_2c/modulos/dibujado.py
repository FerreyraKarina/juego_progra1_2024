import pygame
from config.constantes import *
from modulos.algoritmos import obtener_top_10

def dibujar_boton(ventana, x, y, ancho, alto, texto, color, color_hover, mouse_pos, fuente):
    """
    Dibuja un botón con efecto hover
    
    Args:
        ventana: superficie de pygame donde dibujar
        x, y: posición de la esquina superior izquierda
        ancho, alto: dimensiones del botón
        texto: texto a mostrar en el botón
        color: color normal del botón
        color_hover: color cuando el mouse está encima
        mouse_pos: tupla (x, y) de la posición del mouse
        fuente: fuente de pygame para el texto
        
    Returns:
        bool: True si hay hover, False si no
    """
    hover = False
    
    # Detectar hover

    if mouse_pos[0] >= x:  # si el mouse esta a la derecha del borde izquierdo
        if mouse_pos[0] <= x + ancho:  # si el mouse esta a la izquierda del borde derecho
            if mouse_pos[1] >= y:  # si el mouse esta debajo del borde superior
                if mouse_pos[1] <= y + alto:  # si el mouse esta arriba del borde inferior
                    hover = True
                    color_actual = color_hover
                else:
                    hover = False
                    color_actual = color
            else:
                hover = False
                color_actual = color
        else:
            hover = False
            color_actual = color
    else:
        hover = False
        color_actual = color
                
    
    
    # Dibujar rectángulo del botón
    pygame.draw.rect(ventana, color_actual, (x, y, ancho, alto), border_radius=10)
    
    # Dibujar borde del botón
    pygame.draw.rect(ventana, NEGRO, (x, y, ancho, alto), 3, border_radius=10)
    
    # Renderizar texto
    texto_surf = fuente.render(texto, True, BLANCO)
    
    # Centrar texto en el botón
    texto_rect = texto_surf.get_rect()
    texto_rect.center = (x + ancho // 2, y + alto // 2)
    
    # Dibujar texto
    ventana.blit(texto_surf, texto_rect)
    
    return hover


def verificar_click_boton(x, y, ancho, alto, pos_click):
    """
    Verifica si el click fue dentro del botón
    
    Args:
        x, y: posición del botón
        ancho, alto: dimensiones del botón
        pos_click: tupla (x, y) de la posición del click
        
    Returns:
        bool: True si el click fue dentro del botón
    """
    click_dentro = False
    click_x = pos_click[0]
    click_y = pos_click[1]
    
    if click_x >= x and click_x <= x + ancho:
        if click_y >= y and click_y <= y + alto:
            click_dentro = True
        
    return click_dentro


def dibujar_menu(ventana, mouse_pos, fuente_grande, fuente_mediana):
    """Dibuja el menú principal"""
    fondo_menu = pygame.image.load("utils/fondo_menu.png")
    fondo_menu = pygame.transform.scale(fondo_menu,(ANCHO_VENTANA, ALTO_VENTANA))
    ventana.blit(fondo_menu, (0,0))
    
  
    titulo = fuente_grande.render("JUEGO MATEMÁTICO", True, AMARILLO)
    titulo_rect = titulo.get_rect(center=(ANCHO_VENTANA // 2, 100))
    ventana.blit(titulo, titulo_rect)
    
    
    dibujar_boton(ventana, 250, 220, 400, 70, "JUGAR", VERDE, VERDE_OSCURO, mouse_pos, fuente_mediana)
    dibujar_boton(ventana, 250, 320, 400, 70, "HISTORIAL", AZUL, AZUL_OSCURO, mouse_pos, fuente_mediana)
    dibujar_boton(ventana, 250, 420, 400, 70, "SALIR", ROJO, ROJO_OSCURO, mouse_pos, fuente_mediana)


def dibujar_seleccion_nivel(ventana, mouse_pos, fuente_grande, fuente_mediana):
    """Dibuja la pantalla de selección de nivel"""
    fondo_nivel = pygame.image.load("utils/fondo_nivel.png")
    fondo_nivel = pygame.transform.scale(fondo_nivel,(ANCHO_VENTANA, ALTO_VENTANA))
    ventana.blit(fondo_nivel, (0,0))
    
    # Título
    titulo = fuente_grande.render("SELECCIONA NIVEL", True, BLANCO)
    titulo_rect = titulo.get_rect(center=(ANCHO_VENTANA // 2, 100))
    ventana.blit(titulo, titulo_rect)
    
    # Botones de nivel
    dibujar_boton(ventana, 250, 200, 400, 70, "FÁCIL", VERDE, VERDE_OSCURO, mouse_pos, fuente_mediana)
    dibujar_boton(ventana, 250, 300, 400, 70, "MEDIO", AMARILLO, AMARILLO, mouse_pos, fuente_mediana)
    dibujar_boton(ventana, 250, 400, 400, 70, "DIFÍCIL", ROJO, ROJO_OSCURO, mouse_pos, fuente_mediana)
    dibujar_boton(ventana, 250, 520, 400, 60, "VOLVER", AZUL, GRIS_OSCURO, mouse_pos, fuente_mediana)


def dibujar_juego(ventana, estado_juego, mouse_pos, fuente_grande, fuente_mediana, fuente_pequena):
    """Dibuja la pantalla de juego"""
    fondo_pregunta = pygame.image.load("utils/fondo_pregunta.jpg")
    fondo_pregunta = pygame.transform.scale(fondo_pregunta,(ANCHO_VENTANA, ALTO_VENTANA))
    ventana.blit(fondo_pregunta, (0,0))
    
    # Información superior
    texto_vidas = fuente_pequena.render(f"Vidas: {estado_juego['vidas']}", True, ROJO)
    ventana.blit(texto_vidas, (20, 20))
    
    texto_puntos = fuente_pequena.render(f"Puntos: {estado_juego['puntos']}", True, VERDE)
    ventana.blit(texto_puntos, (400, 20))
    
    texto_nivel = fuente_pequena.render(f"Nivel: {estado_juego['nivel'].upper()}", True, AZUL)
    ventana.blit(texto_nivel, (700, 20))
    
    # Tiempo (rojo si quedan ≤ 3 segundos)
    tiempo_restante = estado_juego['tiempo_restante']
    
    if tiempo_restante <= 3:
        color_tiempo = ROJO 
        #podria poner  musica de suspenso
    else:
        color_tiempo =BLANCO
    
    texto_tiempo = fuente_pequena.render(f"Tiempo: {int(tiempo_restante)}s", True, color_tiempo)
    ventana.blit(texto_tiempo, (20, 60))
    
    # Pregunta
    if estado_juego['pregunta_actual']:
        pregunta = estado_juego['pregunta_actual']['pregunta']
        texto_pregunta = fuente_grande.render(pregunta, True, BLANCO)
        texto_rect = texto_pregunta.get_rect(center=(ANCHO_VENTANA // 2, 200))
        ventana.blit(texto_pregunta, texto_rect)
    
    # Campo de respuesta
    pygame.draw.rect(ventana, BLANCO, (250, 300, 400, 60))
    pygame.draw.rect(ventana, NEGRO, (250, 300, 400, 60), 3)
    
    respuesta = estado_juego['respuesta_usuario']
    texto_respuesta = fuente_mediana.render(respuesta, True, NEGRO)
    texto_rect = texto_respuesta.get_rect(center=(450, 330))
    ventana.blit(texto_respuesta, texto_rect)
    
    # Mensaje temporal
    if estado_juego['mostrar_mensaje']:
        texto_mensaje = fuente_mediana.render(estado_juego['mensaje'], True, estado_juego['color_mensaje'])
        texto_rect = texto_mensaje.get_rect(center=(ANCHO_VENTANA // 2, 420))
        ventana.blit(texto_mensaje, texto_rect)
    
    # Comodines
    nombres_comodines = ["Cambiar", " Pista", "+5seg"]
    i = 0
    while i < 3:
        x = 50 + i * 200
        y = 500
        
        if i in estado_juego['comodines_usados']:
            color = GRIS
            color_hover = GRIS_OSCURO
            texto = "Usado"
        else:
            color = NARANJA
            color_hover = NARANJA_OSCURO
            texto = nombres_comodines[i]
        
        dibujar_boton(ventana, x, y, 180, 50, texto, color, color_hover, mouse_pos, fuente_pequena)
        i = i + 1
    
    # Botón rendirse
    dibujar_boton(ventana, 325, 600, 250, 50, "RENDIRSE", ROJO, ROJO_OSCURO, mouse_pos, fuente_pequena)


def dibujar_historial(ventana, puntajes, mouse_pos, fuente_grande, fuente_mediana, fuente_pequena):
    """Dibuja el historial de puntajes"""
    
    fondo_puntaje = pygame.image.load("utils/fondo_puntaje.png")
    fondo_puntaje = pygame.transform.scale(fondo_puntaje,(ANCHO_VENTANA, ALTO_VENTANA))
    ventana.blit(fondo_puntaje, (0,0))
    
    # Título
    titulo = fuente_grande.render("TOP 10 PUNTAJES", True, BLANCO)
    titulo_rect = titulo.get_rect(center=(ANCHO_VENTANA // 2, 50))
    ventana.blit(titulo, titulo_rect)
    
    # Encabezados
    pygame.draw.line(ventana, BLANCO, (50, 155), (850, 155), 2)
    texto_pos = fuente_mediana.render("Pos", True, BLANCO)
    ventana.blit(texto_pos, (80, 120))
    
    texto_puntos = fuente_mediana.render("Puntos", True, BLANCO)
    ventana.blit(texto_puntos, (200, 120))
    
    texto_nivel = fuente_mediana.render("Nivel", True, BLANCO)
    ventana.blit(texto_nivel, (400, 120))
    
    texto_fecha = fuente_mediana.render("Fecha", True, BLANCO)
    ventana.blit(texto_fecha, (600, 120))
    
    # Top 10
    top_10 = obtener_top_10(puntajes)
    
    i = 0
    while i < len(top_10):
        puntaje = top_10[i]
        y = 180 + i * 45
        
        # Posición
        texto = fuente_pequena.render(f"{i + 1}", True, BLANCO)
        ventana.blit(texto, (90, y))
        
        # Puntos
        texto = fuente_pequena.render(str(puntaje['puntos']), True, AMARILLO)
        ventana.blit(texto, (220, y))
        
        # Nivel
        texto = fuente_pequena.render(puntaje['nivel'].upper(), True, BLANCO)
        ventana.blit(texto, (420, y))
        
        # Fecha
        texto = fuente_pequena.render(puntaje['fecha'], True, BLANCO)
        ventana.blit(texto, (610, y))
        
        i = i + 1
    
    # Botón volver
    btn_volver = dibujar_boton(ventana, 325, 620, 250, 50, "VOLVER", 
                                 AZUL, AZUL_OSCURO, mouse_pos, fuente_mediana)
    
    return {'volver': btn_volver}


def dibujar_game_over(ventana, puntos, nivel, gano, mouse_pos, fuente_grande, fuente_mediana):
    """Dibuja la pantalla de game over (victoria o derrota)"""
    
    fondo_final_juego = pygame.image.load("utils/fondo_victoria.png")
    fondo_final_juego = pygame.transform.scale(fondo_final_juego,(ANCHO_VENTANA,ALTO_VENTANA))
    ventana.blit(fondo_final_juego, (0,0))
    
    # Título y mensajes según si ganó o perdió
    if gano:
        # VICTORIA
        titulo = fuente_grande.render("¡VICTORIA!", True, AMARILLO)
        subtitulo = f"¡Completaste el nivel {nivel.upper()}!"
        mensaje = "¡Respondiste TODAS las preguntas correctamente!"
        color_mensaje = BLANCO
    else:
        # DERROTA
        titulo = fuente_grande.render("¡JUEGO TERMINADO!", True, ROJO)
        subtitulo = f"Nivel: {nivel.upper()}"
        mensaje = "¡Sigue intentando!"
        color_mensaje = BLANCO
    
    # Dibujar título
    titulo_rect = titulo.get_rect(center=(ANCHO_VENTANA // 2, 100))
    ventana.blit(titulo, titulo_rect)
    
    # Dibujar subtítulo
    texto_sub = fuente_mediana.render(subtitulo, True, NEGRO)
    texto_sub_rect = texto_sub.get_rect(center=(ANCHO_VENTANA // 2, 200))
    ventana.blit(texto_sub, texto_sub_rect)
    
    # Puntaje final
    texto_puntos = fuente_mediana.render(f"Puntaje Final: {puntos}", True, BLANCO)
    texto_rect = texto_puntos.get_rect(center=(ANCHO_VENTANA // 2, 280))
    ventana.blit(texto_puntos, texto_rect)
    
    # Mensaje adicional
    texto_mensaje = fuente_mediana.render(mensaje, True, color_mensaje)
    texto_mensaje_rect = texto_mensaje.get_rect(center=(ANCHO_VENTANA // 2, 350))
    ventana.blit(texto_mensaje, texto_mensaje_rect)
    
    # Botones (iguales para ambos casos)
    btn_jugar = dibujar_boton(ventana, 250, 450, 400, 70, "JUGAR DE NUEVO", 
                               VERDE, VERDE_OSCURO, mouse_pos, fuente_mediana)
    btn_menu = dibujar_boton(ventana, 250, 550, 400, 70, "VOLVER AL MENÚ", 
                              AZUL, AZUL_OSCURO, mouse_pos, fuente_mediana)
    
    return {'jugar': btn_jugar, 'menu': btn_menu}
