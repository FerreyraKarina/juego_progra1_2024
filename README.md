# Juego Matemático

Juego educativo de matemáticas desarrollado en Python con Pygame.

##  Características

- ✅ 3 niveles de dificultad (Fácil, Medio, Difícil)
- ✅ 3 vidas por partida
- ✅ 3 comodines únicos (Cambiar pregunta, Pista, +5 segundos)
- ✅ 10 segundos por pregunta
- ✅ Sistema de puntos (1 punto por respuesta correcta)
- ✅ Historial de Top 10 puntajes
- ✅ Pantalla de victoria al completar todas las preguntas
- ✅ Código modularizado sin clases

##  Instalación

```bash
pip install pygame
```

##  Ejecutar el juego

```bash
python main.py
```

##  Estructura del proyecto

```
juego_modular_final/
├── main.py                 # Punto de entrada
├── preguntas.csv          # 60 preguntas (20 por nivel)
├── preguntas_test_mini.csv # 9 preguntas para testing rápido
├── puntajes.json          # Historial de puntajes
├── config/
│   ├── __init__.py
│   └── constantes.py      # Configuración y constantes
└── modulos/
    ├── __init__.py
    ├── archivos.py        # Manejo de CSV y JSON
    ├── algoritmos.py      # Bubble Sort y filtrado
    ├── estado.py          # Gestión del estado del juego
    ├── logica.py          # Mecánicas del juego
    ├── dibujado.py        # Renderizado con Pygame
    └── eventos.py         # Procesamiento de inputs
```

##  Cómo jugar

1. **Menú Principal**: Elige JUGAR, ver HISTORIAL o SALIR
2. **Selección de Nivel**: Elige Fácil, Medio o Difícil
3. **Juego**: 
   - Escribe tu respuesta con el teclado
   - Presiona ENTER para verificar
   - Usa BACKSPACE para borrar
4. **Comodines**:
   -  **Cambiar**: Nueva pregunta aleatoria
   -  **Pista**: Muestra la mitad de la respuesta
   -  **+5seg**: Agrega 5 segundos (máximo 15s)
5. **Victoria**: Responde TODAS las preguntas correctamente
6. **Game Over**: Pierdes si se acaban las 3 vidas

##  Testing Rápido

Para probar rápidamente victoria/derrota:

```bash
# Reemplazar preguntas.csv con preguntas_test_mini.csv
# Este archivo tiene solo 3 preguntas por nivel (1+1, 2+2, 3+3)
```


## Autor
Karina Ferreyra
Proyecto educativo - Programación en Python

##  Licencia

Proyecto educativo de código abierto
