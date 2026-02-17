import csv
import random
import os
import tkinter as tk
from PIL import Image, ImageTk
import platform

# -----------------------------
# Configuración
# -----------------------------

archivo_csv = "datapalabra.csv"
carpeta_imagenes = "imagen"

puntaje = 0
palabra_correcta = ""
palabras = []
palabras_disponibles = []

imagenes_botones = []
imagenes_tk = []

# -----------------------------
# Leer CSV
# -----------------------------

if not os.path.exists(archivo_csv):
    print("No se encontró el archivo CSV")
    exit()

with open(archivo_csv, newline="", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        palabra = fila["palabra"].strip()
        if palabra:
            palabras.append(palabra)
            

# -----------------------------
# Ventana
# -----------------------------

ventana = tk.Tk()
ventana.title("🎮 Adivina la palabra PRO")
ventana.geometry("600x700")
ventana.config(bg="#1e1e2f")

# -----------------------------
# Global Variables
# -----------------------------

gif_job = None # Stores the current GIF animation loop ID (used to stop previous animation)

# -----------------------------
# Sonido multiplataforma robusto
# -----------------------------

def beep(frecuencia=1000, duracion=200):
    sistema = platform.system()

    if sistema == "Windows":
        try:
            import winsound
            winsound.Beep(frecuencia, duracion)
        except:
            pass

    else:
        # Linux / Raspberry Pi
        try:
            # Try system beep command
            exit_code = os.system(f'beep -f {frecuencia} -l {duracion}')
            
            # If beep command failed, fallback to ASCII bell
            if exit_code != 0:
                print('\a', end='', flush=True)

        except:
            # Final fallback
            print('\a', end='', flush=True)


def sonido_correcto():
    beep(1200, 150)


def sonido_incorrecto():
    beep(400, 300)


# -----------------------------
# UI ELEMENTS
# -----------------------------

titulo = tk.Label(
    ventana,
    text="🧠 ADIVINA LA PALABRA",
    font=("Arial Black", 20),
    bg="#1e1e2f",
    fg="white"
)
titulo.pack(pady=10)

nivel_var = tk.StringVar(value="Fácil")

menu_nivel = tk.OptionMenu(
    ventana,
    nivel_var,
    "Fácil",
    "Medio"
)
menu_nivel.pack()

etiqueta_palabra = tk.Label(
    ventana,
    font=("Arial Black", 22),
    bg="#1e1e2f",
    fg="#00ffcc"
)
etiqueta_palabra.pack(pady=10)

frame_imagenes = tk.Frame(ventana, bg="#1e1e2f")
frame_imagenes.pack(pady=10)

etiqueta_imagen = tk.Label(ventana, bg="#1e1e2f")
etiqueta_imagen.pack()

entrada = tk.Entry(ventana, font=("Arial", 16), justify="center")
entrada.pack(pady=10)

boton = tk.Button(
    ventana,
    text="COMPROBAR",
    font=("Arial Black", 14),
    bg="#00cc99",
    command=lambda: comprobar_respuesta()
)
boton.pack(pady=10)

etiqueta_resultado = tk.Label(
    ventana,
    font=("Arial", 14),
    bg="#1e1e2f"
)
etiqueta_resultado.pack()

etiqueta_puntaje = tk.Label(
    ventana,
    text="⭐ Puntaje: 0",
    font=("Arial", 14, "bold"),
    bg="#1e1e2f",
    fg="#00ffcc"
)
etiqueta_puntaje.pack(pady=5)

# -----------------------------
# Buscar imagen
# -----------------------------

def buscar_imagen(nombre_palabra):
    extensiones = [".png", ".jpg", ".jpeg", ".gif"]

    for archivo in os.listdir(carpeta_imagenes):
        nombre, extension = os.path.splitext(archivo)
        if extension.lower() in extensiones:
            if nombre.lower() == nombre_palabra.lower():
                return os.path.join(carpeta_imagenes, archivo)
    return None

# -----------------------------
# NUEVA PALABRA
# -----------------------------

def cargar_nueva_palabra():
    global palabra_correcta, imagenes_tk

    etiqueta_resultado.config(text="")
    entrada.delete(0, tk.END)

    if not palabras:
        return

    palabra_correcta = random.choice(palabras)

    if nivel_var.get() == "Fácil":
        modo_facil()
    else:
        modo_medio()
        
# -----------------------------
# GIF Animation Handler
# -----------------------------
        
def animar_gif(label, gif_path, size):
    global gif_job

    # Stop previous animation if running
    if gif_job is not None:
        ventana.after_cancel(gif_job)
        gif_job = None

    gif = Image.open(gif_path)

    frames = []
    try:
        while True:
            frame = gif.copy()
            frame = frame.resize(size, Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame))
            gif.seek(len(frames))
    except EOFError:
        pass

    def actualizar(indice=0):
        global gif_job
        frame = frames[indice]
        label.config(image=frame)
        label.image = frame
        gif_job = ventana.after(
            100,
            actualizar,
            (indice + 1) % len(frames)
        )

    actualizar()


# -----------------------------
# MODO FÁCIL
# -----------------------------

def modo_facil():
    global imagenes_tk

    # ---- Hide medio mode widgets ----
    entrada.pack_forget()
    boton.pack_forget()
    etiqueta_imagen.config(image="")
    etiqueta_imagen.pack_forget()

    # ---- Show word ----
    etiqueta_palabra.config(text=palabra_correcta.upper())

    # ---- Prepare image frame ----
    frame_imagenes.pack(pady=15)

    # Clear previous buttons
    for widget in frame_imagenes.winfo_children():
        widget.destroy()

    # ---- Create 3 options (1 correct + 2 random) ----
    opciones = [palabra_correcta]

    while len(opciones) < 3:
        candidata = random.choice(palabras)
        if candidata not in opciones:
            opciones.append(candidata)

    random.shuffle(opciones)

    imagenes_tk = []  # keep references alive

    # ---- Create buttons ----
    for palabra in opciones:
        path = buscar_imagen(palabra)

        if not path:
            continue  # skip if image missing

        img = Image.open(path)
        img = img.resize((160, 160), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        imagenes_tk.append(img_tk)

        btn = tk.Button(
            frame_imagenes,
            image=img_tk,
            bd=3,
            relief="raised",
            command=lambda p=palabra: verificar_click(p)
        )
        btn.pack(side="left", padx=15)


# -----------------------------
# VERIFICAR CLICK
# -----------------------------

def verificar_click(palabra_seleccionada):
    global puntaje

    if palabra_seleccionada == palabra_correcta:
        puntaje += 1
        etiqueta_resultado.config(text="✅ ¡Correcto!", fg="#00ff88")
        sonido_correcto()
    else:
        etiqueta_resultado.config(
            text=f"❌ Era: {palabra_correcta}",
            fg="#ff4444"
        )
        sonido_incorrecto()

    etiqueta_puntaje.config(text=f"⭐ Puntaje: {puntaje}")
    ventana.after(1200, cargar_nueva_palabra)

# -----------------------------
# MODO MEDIO
# -----------------------------

def modo_medio():
    
    global gif_job
    if gif_job is not None:
        ventana.after_cancel(gif_job)
        gif_job = None
        
    etiqueta_palabra.config(text="")

    # 🔴 Remove all easy-mode image buttons
    for widget in frame_imagenes.winfo_children():
        widget.destroy()

    frame_imagenes.pack_forget()   # Hide the 3-image frame

    entrada.pack(pady=10)
    boton.pack(pady=10)
    etiqueta_imagen.pack(pady=10)

    path = buscar_imagen(palabra_correcta)

    if path:
        if path.lower().endswith(".gif"):
            animar_gif(etiqueta_imagen, path, (300, 300))
        else:
            img = Image.open(path)
            img = img.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)

            etiqueta_imagen.config(image=img_tk)
            etiqueta_imagen.image = img_tk



# -----------------------------
# COMPROBAR RESPUESTA (MEDIO)
# -----------------------------

def comprobar_respuesta():
    global puntaje

    respuesta = entrada.get().strip().lower()

    if respuesta == palabra_correcta.lower():
        puntaje += 1
        etiqueta_resultado.config(text="✅ ¡Correcto!", fg="#00ff88")
        sonido_correcto()
    else:
        etiqueta_resultado.config(
            text=f"❌ Era: {palabra_correcta}",
            fg="#ff4444"
        )
        sonido_incorrecto()

    etiqueta_puntaje.config(text=f"⭐ Puntaje: {puntaje}")
    ventana.after(1200, cargar_nueva_palabra)

# -----------------------------
# Eventos
# -----------------------------

nivel_var.trace_add("write", lambda *args: cargar_nueva_palabra())
ventana.bind("<Return>", lambda event: comprobar_respuesta())

# -----------------------------
# Iniciar
# -----------------------------

cargar_nueva_palabra()
ventana.mainloop()
