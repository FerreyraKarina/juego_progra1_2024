#!/usr/bin/env python3
# main.py
"""
Juego Matemático - Punto de entrada principal
Proyecto modularizado sin clases, solo funciones
"""

import pygame
import sys

# Importar configuración
from config.constantes import *

# Importar módulos
from modulos.archivos import cargar_preguntas_csv, cargar_puntajes_json, guardar_puntajes_json, agregar_puntaje
from modulos.algoritmos import filtrar_preguntas_por_nivel
from modulos.estado import crear_estado_juego
from modulos.logica import actualizar_tiempo, nueva_pregunta, procesar_respuesta_incorrecta
from modulos.dibujado import (
    dibujar_menu, 
    dibujar_seleccion_nivel, 
    dibujar_juego, 
    dibujar_historial, 
    dibujar_game_over
)
from modulos.eventos import (
    procesar_eventos_menu,
    procesar_eventos_seleccion_nivel,
    procesar_eventos_juego,
    procesar_eventos_historial,
    procesar_eventos_game_over
)


def main():


    pygame.init()
    pygame.mixer.init()
    
    # Crear ventana
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Juego Matemático")
    
    # Reloj para controlar FPS
    reloj = pygame.time.Clock()
    
    # Fuentes
    fuente_grande = pygame.font.Font(None, 72)
    fuente_mediana = pygame.font.Font(None, 48)
    fuente_pequena = pygame.font.Font(None, 36)
    
    # Cargar datos
    todas_las_preguntas = cargar_preguntas_csv(ARCHIVO_PREGUNTAS)
    puntajes = cargar_puntajes_json(ARCHIVO_PUNTAJES)
    
    # Estado inicial
    pantalla_actual = 'menu'
    estado_juego = None
    
    preguntas_nivel_actual = []
   
    musica_fondo = pygame.mixer.Sound("utils/musica_fondo.mp3")
    musica_fondo.play(-1)
    musica_fondo.set_volume(0.3)
    
  
    # LOOP PRINCIPAL
   
    ejecutando = True
    
    while ejecutando:
        
        mouse_pos = pygame.mouse.get_pos()
       
        eventos = pygame.event.get()
        
     
        # PROCESAR EVENTOS
       
        
        if pantalla_actual == 'menu':
            resultado = procesar_eventos_menu(eventos)
            if resultado == 'salir':
                ejecutando = False
            elif resultado:
                pantalla_actual = resultado
        
        elif pantalla_actual == 'seleccion_nivel':
            nueva_pantalla, nivel = procesar_eventos_seleccion_nivel(eventos)
            
            if nueva_pantalla == 'salir':
                ejecutando = False
            elif nueva_pantalla == 'jugando' and nivel:
               
                preguntas_nivel_actual = filtrar_preguntas_por_nivel(todas_las_preguntas, nivel)
                estado_juego = crear_estado_juego(nivel)
                nueva_pregunta(estado_juego, preguntas_nivel_actual)
                pantalla_actual = 'jugando'
            elif nueva_pantalla:
                pantalla_actual = nueva_pantalla
        
        elif pantalla_actual == 'jugando':
            resultado = procesar_eventos_juego(eventos, estado_juego, preguntas_nivel_actual, puntajes)
            
            if resultado == 'salir':
                ejecutando = False
            elif resultado:
                pantalla_actual = resultado
        
        elif pantalla_actual == 'historial':
            resultado = procesar_eventos_historial(eventos)
            
            if resultado == 'salir':
                ejecutando = False
            elif resultado:
                pantalla_actual = resultado
        
        elif pantalla_actual == 'game_over':
            resultado = procesar_eventos_game_over(eventos)
            
            if resultado == 'salir':
                ejecutando = False
            elif resultado:
                pantalla_actual = resultado
                if resultado == 'seleccion_nivel':
                    estado_juego = None
        
       
        # ACTUALIZAR ESTADO
      
        
        if pantalla_actual == 'jugando' and estado_juego:
            # Actualizar tiempo
            tiempo_agotado = actualizar_tiempo(estado_juego)
            
            if tiempo_agotado:
                procesar_respuesta_incorrecta(estado_juego)
                
                if estado_juego['vidas'] <= 0:
                    estado_juego['gano'] = False
                    agregar_puntaje(puntajes, estado_juego['puntos'], estado_juego['nivel'])
                    guardar_puntajes_json(ARCHIVO_PUNTAJES, puntajes)
                    pantalla_actual = 'game_over'
                else:
                    # Intentar cargar nueva pregunta
                    hay_pregunta = nueva_pregunta(estado_juego, preguntas_nivel_actual)
                    
                  
                    if not hay_pregunta:
                        estado_juego['gano'] = True
                        agregar_puntaje(puntajes, estado_juego['puntos'], estado_juego['nivel'])
                        guardar_puntajes_json(ARCHIVO_PUNTAJES, puntajes)
                        pantalla_actual = 'game_over'
            
         
        
        # DIBUJAR
       
        
        if pantalla_actual == 'menu':
            dibujar_menu(ventana, mouse_pos, fuente_grande, fuente_mediana)
        
        elif pantalla_actual == 'seleccion_nivel':
            dibujar_seleccion_nivel(ventana, mouse_pos, fuente_grande, fuente_mediana)
        
        elif pantalla_actual == 'jugando':
            dibujar_juego(ventana, estado_juego, mouse_pos, 
                          fuente_grande, fuente_mediana, fuente_pequena)
        
        elif pantalla_actual == 'historial':
            dibujar_historial(ventana, puntajes, mouse_pos, 
                              fuente_grande, fuente_mediana, fuente_pequena)
        
        elif pantalla_actual == 'game_over':
            if estado_juego:
                dibujar_game_over(ventana, estado_juego['puntos'], estado_juego['nivel'],
                                  estado_juego['gano'], mouse_pos, fuente_grande, fuente_mediana)
        

      
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
