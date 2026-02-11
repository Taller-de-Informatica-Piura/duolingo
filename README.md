# Duolingo Piura – Proyecto de Aprendizaje de Inglés

Este proyecto es un **mini-Duolingo** desarrollado en Python para que los estudiantes puedan **aprender inglés jugando**. Cada palabra se asocia con una imagen, y los alumnos deben escribir la palabra correcta en inglés. El proyecto está diseñado para usar **Thonny** como entorno de programación, ideal para principiantes y compatible con Windows.

---

## 📁 Estructura del Proyecto

duolingopiura/
│
├── datapalabra.csv # CSV con la lista de palabras (columna: palabra)
├── imagen/ # Carpeta con imágenes (.png o .gif) de las palabras
│ ├── cat.png
│ ├── dog.gif
│ └── house.png
├── duolingopiura.py # Script principal del juego
└── Thonny_python-installer-windows/
├── Thonny-<version>.exe # Instalador de Thonny para Windows
├── Pillow‑<version>.whl # Archivo para instalar Pillow
└── pygame‑<version>.whl # Archivo para instalar Pygame



---

## 📝 Función del Script Principal

**`duolingopiura.py`** es el corazón del juego y hace lo siguiente:

1. Carga las palabras del archivo `datapalabra.csv`.
2. Elige aleatoriamente una palabra que aún no se haya mostrado.
3. Busca la imagen correspondiente en la carpeta `imagen`.
4. Muestra la imagen en una ventana de **Tkinter**.
5. Permite que el usuario escriba la palabra en inglés y la compruebe con un botón.
6. Muestra si la respuesta es correcta o incorrecta y actualiza el **puntaje**.
7. Después de 1.5 segundos, muestra automáticamente la siguiente palabra.
8. Cuando no quedan más palabras, muestra un mensaje de **“Juego terminado”**.

---

## 💻 Instalación en Windows

Para poder ejecutar el proyecto, necesitamos:

- **Python 3** (ya viene con Thonny)
- **Thonny IDE** (para ejecutar y modificar los scripts)
- **Pillow** (para mostrar imágenes)
- **(Opcional) Pygame** si quieren agregar sonido después

---

### Opción 1 – Descargar Thonny desde la web

1. Ir a la página oficial: [https://thonny.org](https://thonny.org)
2. Descargar el instalador para Windows.
3. Ejecutar el instalador y seguir las instrucciones.
4. Abrir Thonny y luego:
   ```bash
   pip install pillow
   pip install pygame

## Opción 2 – Usar el instalador incluido en el proyecto

1. Abrir la carpeta `Thonny_python-installer-windows`.
2. Ejecutar `Thonny-<version>.exe` para instalar Thonny en Windows.
3. Abrir Thonny y luego instalar los paquetes desde los **.whl**:
   - Ir a `Tools → Manage packages → Install from local file`
   - Seleccionar `Pillow‑<version>.whl` y hacer click en **Instalar**
   - Repetir para `pygame‑<version>.whl` si se desea

---

## 🚀 Cómo ejecutar el juego

1. Abrir Thonny.
2. Abrir el archivo `duolingopiura.py`.
3. Asegurarse de que las carpetas `imagen` y el CSV `datapalabra.csv` estén en la misma carpeta que el script.
4. Ejecutar el script con **Run → Run current script (F5)**.
5. Escribir la palabra en inglés en la caja de texto y hacer click en **Comprobar**.
6. Seguir jugando hasta que aparezcan todas las palabras.

---

## 🎓 Sugerencias de extensión para los estudiantes

- Agregar más palabras y sus imágenes.
- Añadir niveles o vidas.
- Cambiar la interfaz con colores o fuentes más divertidas.
- Añadir sonido usando Pygame.
- Guardar un **high score** para competir.

---

## 👍 Notas

- El juego es **cross-platform**: funciona en Windows y Raspberry Pi OS.
- Tkinter viene incluido con Python y Thonny, por lo que no requiere instalación adicional.
- Pillow es necesario para mostrar las imágenes en Tkinte









