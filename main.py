import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random

# Variables globales
tematica_elegida = None
palabra_seleccionada = None
intentos = 3
victorias = 0
derrotas = 0

# jugador existe?
def verificar_jugador(nombre):
    conn = None  # Aseguramos que la variable conn esté inicializada
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Ahorcado"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Jugador WHERE nombre = %s", (nombre,))
        jugador = cursor.fetchone()

        if jugador:
            return True
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        if conn:
            conn.close()

# victorias y derrotas
def actualizar_estadisticas(nombre, victoria):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Ahorcado"
        )
        cursor = conn.cursor()
        if victoria:
            cursor.execute("UPDATE Jugador SET victorias = victorias + 1 WHERE nombre = %s", (nombre,))
        else:
            cursor.execute("UPDATE Jugador SET derrotas = derrotas + 1 WHERE nombre = %s", (nombre,))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn:
            conn.close()

# jugar
def jugar():
    nombre = entry_nombre.get()

    if nombre == "":
        messagebox.showwarning("Ingresa Nombre", "Por favor ingresa tu nombre")
        return

    if not verificar_jugador(nombre):
        messagebox.showinfo("Nuevo jugador", f"Hola, {nombre}, Se ha creado tu perfil")

    # Cerrar la ventana de inicio
    root.destroy()

    # Iniciar la ventana de juego
    iniciar_ventana_juego(nombre)

# Función para iniciar la ventana del juego
def iniciar_ventana_juego(nombre):
    global palabra_seleccionada, intentos
    intentos = 3

    # Palabras de las temáticas
    palabras_frutas = ['manzana', 'plátano', 'pomelo', 'piña', 'melon']
    palabras_informatica = ['python', 'java', 'kotlin', 'C#', 'javascript']
    palabras_personas = ['martin', 'raul', 'pablo', 'ivan', 'rodri']

    if tematica_elegida == 'Frutas':
        palabras = palabras_frutas
    elif tematica_elegida == 'Conceptos informáticos':
        palabras = palabras_informatica
    elif tematica_elegida == 'Nombres de personas':
        palabras = palabras_personas
    else:
        palabras = []

    palabra_seleccionada = random.choice(palabras)  # Selección aleatoria de palabra
    letras_adivinadas = ['_'] * len(palabra_seleccionada)

    def actualizar_palabra_letras():
        label_palabra.config(text=' '.join(letras_adivinadas))

    def comprobar_letra():
        global intentos

        letra = entry_letra.get().lower()
        entry_letra.delete(0, tk.END)

        if letra in palabra_seleccionada:
            for i in range(len(palabra_seleccionada)):
                if palabra_seleccionada[i] == letra:
                    letras_adivinadas[i] = letra
            actualizar_palabra_letras()

            if '_' not in letras_adivinadas:
                messagebox.showinfo("Ganaste", f" {nombre}Adivinaste la palabra: {palabra_seleccionada}")
                actualizar_estadisticas(nombre, True)
                return
        else:
            intentos -= 1
            if intentos == 0:
                messagebox.showinfo("Perdiste", f"La palabra era: {palabra_seleccionada}")
                actualizar_estadisticas(nombre, False)
                return

        if intentos > 0:
            label_intentos.config(text=f"Intentos restantes: {intentos}")
        else:
            label_intentos.config(text="¡Fin del juego!")

    # Crear ventana del juego
    ventana_juego = tk.Tk()
    ventana_juego.title("Juego Ahorcado")
    ventana_juego.geometry("400x400")

    label_titulo = tk.Label(ventana_juego, text=f"Temática: {tematica_elegida}", font=("Arial", 14))
    label_titulo.pack(pady=10)

    label_palabra = tk.Label(ventana_juego, text='_ ' * len(palabra_seleccionada), font=("Arial", 14))
    label_palabra.pack(pady=10)

    label_intentos = tk.Label(ventana_juego, text=f"Intentos restantes: {intentos}", font=("Arial", 12))
    label_intentos.pack(pady=10)

    label_ingresa_letra = tk.Label(ventana_juego, text="Ingresa una letra:")
    label_ingresa_letra.pack(pady=5)

    entry_letra = tk.Entry(ventana_juego, font=("Arial", 14))
    entry_letra.pack(pady=5)

    btn_comprobar = tk.Button(ventana_juego, text="Comprobar", command=comprobar_letra)
    btn_comprobar.pack(pady=20)

    # Botón para volver a jugar con la misma temática
    def volver_a_jugar():
        ventana_juego.destroy()
        iniciar_ventana_juego(nombre)

    btn_volver_a_jugar = tk.Button(ventana_juego, text="Volver a jugar", command=volver_a_jugar)
    btn_volver_a_jugar.pack(pady=20)

    ventana_juego.mainloop()

# Función para elegir la temática
def elegir_tematica():
    global tematica_elegida
    tematica_elegida = tema_escogido.get()

root = tk.Tk()
root.title("Ahorcado - Inicio")
root.geometry("400x400")

label_nombre = tk.Label(root, text="Ingresa tu nombre:")
label_nombre.pack(pady=10)

entry_nombre = tk.Entry(root, font=("Arial", 14))
entry_nombre.pack(pady=10)

label_tematica = tk.Label(root, text="Selecciona una temática:")
label_tematica.pack(pady=10)

tema_escogido = tk.StringVar()
tema_escogido.set(None)

radio_frutas = tk.Radiobutton(root, text="Frutas", variable=tema_escogido, value="Frutas", command=elegir_tematica)
radio_frutas.pack()

radio_informatica = tk.Radiobutton(root, text="Conceptos informáticos", variable=tema_escogido, value="Conceptos informáticos", command=elegir_tematica)
radio_informatica.pack()

radio_personas = tk.Radiobutton(root, text="Nombres de personas", variable=tema_escogido, value="Nombres de personas", command=elegir_tematica)
radio_personas.pack()

btn_jugar = tk.Button(root, text="Jugar", command=jugar)
btn_jugar.pack(pady=20)

root.mainloop()
