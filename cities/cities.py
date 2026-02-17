import os
import random
import tkinter as tk
from PIL import Image, ImageTk

# -----------------------------
# Configuración inicial
# -----------------------------
carpeta_imagenes = "imagen"
puntaje = 0
palabra_correcta = ""
imagenes_tk = []

# -----------------------------
# Leer nombres de imágenes
# -----------------------------
archivos = [
    f for f in os.listdir(carpeta_imagenes)
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
]

palabras = [os.path.splitext(f)[0] for f in archivos]
palabras_disponibles = palabras.copy()

# -----------------------------
# Crear ventana
# -----------------------------
ventana = tk.Tk()
ventana.title("Adivina la imagen")
ventana.geometry("800x600")  # tamaño de ventana más grande

# Etiqueta con el nombre a adivinar
etiqueta_nombre = tk.Label(ventana, text="", font=("Arial", 24))
etiqueta_nombre.pack(pady=20)

# Frame para mostrar imágenes
frame_imagenes = tk.Frame(ventana)
frame_imagenes.pack(pady=10)

# Etiquetas de resultado y puntaje
etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 16))
etiqueta_resultado.pack(pady=10)

etiqueta_puntaje = tk.Label(ventana, text=f"Puntaje: {puntaje}", font=("Arial", 16))
etiqueta_puntaje.pack(pady=10)

# -----------------------------
# Funciones
# -----------------------------
def cargar_nueva_palabra():
    global palabra_correcta, imagenes_tk, palabras_disponibles

    # Limpiar frame
    for widget in frame_imagenes.winfo_children():
        widget.destroy()

    if len(palabras_disponibles) == 0:
        etiqueta_nombre.config(text="")
        etiqueta_resultado.config(text="🎉 ¡Juego terminado!")
        return

    # Elegir palabra correcta sin repetir
    palabra_correcta = random.choice(palabras_disponibles)
    palabras_disponibles.remove(palabra_correcta)

    # Elegir solo **una palabra incorrecta**
    palabra_incorrecta = random.choice([p for p in palabras if p != palabra_correcta])

    opciones = [palabra_correcta, palabra_incorrecta]
    random.shuffle(opciones)  # mezclar para que la correcta no siempre esté a la izquierda

    imagenes_tk = []

    for palabra in opciones:
        ruta_imagen = None
        for ext in [".png", ".jpg", ".jpeg", ".gif"]:
            posible = os.path.join(carpeta_imagenes, palabra + ext)
            if os.path.exists(posible):
                ruta_imagen = posible
                break

        if ruta_imagen is None:
            continue

        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((300, 300))  # imágenes grandes
        img_tk = ImageTk.PhotoImage(imagen)
        imagenes_tk.append(img_tk)

        boton_img = tk.Button(
            frame_imagenes,
            image=img_tk,
            command=lambda p=palabra: comprobar_respuesta(p)
        )
        boton_img.pack(side=tk.LEFT, padx=40, pady=10)  # espacio entre las dos imágenes

    etiqueta_nombre.config(text=f"Selecciona: {palabra_correcta}")
    etiqueta_resultado.config(text="")

def comprobar_respuesta(seleccion):
    global puntaje

    if seleccion == palabra_correcta:
        puntaje += 1
        etiqueta_resultado.config(text="✅ ¡Correcto!")
    else:
        etiqueta_resultado.config(text=f"❌ Incorrecto. Era: {palabra_correcta}")

    etiqueta_puntaje.config(text=f"Puntaje: {puntaje}")
    ventana.after(1500, cargar_nueva_palabra)

# -----------------------------
# Iniciar juego
# -----------------------------
cargar_nueva_palabra()
ventana.mainloop()
