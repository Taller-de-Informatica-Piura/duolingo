import csv
import random
import os
import tkinter as tk
from PIL import Image, ImageTk

# -----------------------------
# Configuración inicial
# -----------------------------

archivo_csv = "datapalabra.csv"
carpeta_imagenes = "imagen"
puntaje = 0

palabra_correcta = ""

# -----------------------------
# Leer palabras desde el CSV
# -----------------------------

palabras = []

with open(archivo_csv, newline="", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        palabras.append(fila["palabra"])

# Copia de palabras para no repetir
palabras_disponibles = palabras.copy()

# -----------------------------
# Crear ventana
# -----------------------------

ventana = tk.Tk()
ventana.title("Adivina la palabra")
ventana.geometry("400x500")

# -----------------------------
# Imagen
# -----------------------------

etiqueta_imagen = tk.Label(ventana)
etiqueta_imagen.pack()

# -----------------------------
# Entrada de texto
# -----------------------------

entrada = tk.Entry(ventana, font=("Arial", 14))
entrada.pack(pady=10)

# -----------------------------
# Resultado y puntaje
# -----------------------------

etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 12))
etiqueta_resultado.pack()

etiqueta_puntaje = tk.Label(ventana, text="Puntaje: 0", font=("Arial", 12))
etiqueta_puntaje.pack()

# -----------------------------
# Cargar nueva palabra
# -----------------------------

def cargar_nueva_palabra():
    global palabra_correcta, imagen_tk, palabras_disponibles

    # Si ya no quedan palabras
    if len(palabras_disponibles) == 0:
        etiqueta_imagen.config(image="")
        etiqueta_resultado.config(text="🎉 ¡Juego terminado!")
        return

    # Elegir palabra sin repetir
    palabra_correcta = random.choice(palabras_disponibles)
    palabras_disponibles.remove(palabra_correcta)

    imagen_path = None
    for extension in [".png", ".gif"]:
        posible_path = os.path.join(carpeta_imagenes, palabra_correcta + extension)
        if os.path.exists(posible_path):
            imagen_path = posible_path
            break

    if imagen_path is None:
        etiqueta_resultado.config(
            text=f"No hay imagen para: {palabra_correcta}"
        )
        return

    imagen = Image.open(imagen_path)
    imagen = imagen.resize((300, 300))
    imagen_tk = ImageTk.PhotoImage(imagen)

    etiqueta_imagen.config(image=imagen_tk)
    etiqueta_resultado.config(text="")
    entrada.delete(0, tk.END)

# -----------------------------
# Comprobar respuesta
# -----------------------------

def comprobar_respuesta():
    global puntaje

    respuesta = entrada.get().strip().lower()

    if respuesta == palabra_correcta.lower():
        puntaje += 1
        etiqueta_resultado.config(text="✅ ¡Correcto!")
    else:
        etiqueta_resultado.config(
            text=f"❌ Incorrecto. Era: {palabra_correcta}"
        )

    etiqueta_puntaje.config(text=f"Puntaje: {puntaje}")

    # Cargar siguiente palabra después de 1.5 segundos
    ventana.after(1500, cargar_nueva_palabra)

# -----------------------------
# Botón
# -----------------------------

boton = tk.Button(
    ventana,
    text="Comprobar",
    font=("Arial", 14),
    command=comprobar_respuesta
)
boton.pack(pady=10)

# -----------------------------
# Primera palabra
# -----------------------------

cargar_nueva_palabra()

ventana.mainloop()
