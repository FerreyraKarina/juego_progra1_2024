
import json
import os
import datetime
fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

def cargar_preguntas_csv(archivo):
    """
    Carga las preguntas desde un archivo CSV
    
    Args:
        archivo: ruta del archivo CSV
        
    Returns:
        Lista de diccionarios con preguntas
    """
    preguntas = []
    
    try:
        archivo_abierto = open(archivo, 'r', encoding='utf-8')
        lineas = archivo_abierto.readlines()
        archivo_abierto.close()
        
        
        i = 1  # Saltar la primera línea 
        while i < len(lineas):
            linea = lineas[i].strip()
            if linea:
                partes = linea.split(',')
                if len(partes) >= 3:
                    pregunta_dict = {
                        'pregunta': partes[0],
                        'respuesta': partes[1].strip(),
                        'nivel': partes[2].strip()
                    }
                    preguntas.append(pregunta_dict)
            i = i + 1
        
        return preguntas
    except:
        print(f"Error al cargar preguntas desde {archivo}")
        return []


def cargar_puntajes_json(archivo):
    """
    Carga los puntajes desde un archivo JSON
    
    Args:
        archivo: ruta del archivo JSON
        
    Returns:
        Lista de diccionarios con puntajes
    """
    if os.path.exists(archivo):
        try:
            archivo_abierto = open(archivo, 'r')
            puntajes = json.load(archivo_abierto)
            archivo_abierto.close()
            return puntajes
        except:
            return []
    return []


def guardar_puntajes_json(archivo, puntajes):
    """
    Guarda los puntajes en un archivo JSON
    
    Args:
        archivo: ruta del archivo JSON
        puntajes: lista de diccionarios con puntajes
    """
    try:
        archivo_abierto = open(archivo, 'w')
        json.dump(puntajes, archivo_abierto, indent=2)
        archivo_abierto.close()
    except:
        print(f"Error al guardar puntajes en {archivo}")


def agregar_puntaje(puntajes, puntos, nivel):
    """
    Agrega un nuevo puntaje a la lista
    
    Args:
        puntajes: lista de puntajes existente
        puntos: puntos obtenidos
        nivel: nivel jugado
        
    Returns:
        Lista actualizada de puntajes
    """
    
    
    nuevo_puntaje = {
        'puntos': puntos,
        'fecha': fecha,
        'nivel': nivel
    }
    
    puntajes.append(nuevo_puntaje)
    return puntajes
