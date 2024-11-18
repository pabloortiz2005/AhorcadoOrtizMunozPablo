import tkinter as tk
from tkinter import messagebox
import mysql.connector

tematica_elegida = None

def verificar_jugador(nombre):
    try:
        #Conexion
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Ahorcado"
        )
        cursor = conn.cursor()
        #comprobar si existe el usuario
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
#boton
def jugar():
    nombre = entry_nombre.get()

    if nombre == "":
        messagebox.showwarning("Ingresa Nombre", "Por favor ingresa tu nombre")
        return

    if verificar_jugador(nombre):
        messagebox.showinfo("Jugador encontrado", f"Hola {nombre}")
    else:
        messagebox.showinfo("Nuevo jugador", f"Hola, {nombre}, Se ha creado tu perfil")

#elegir el tema
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

#para solo poder escoger una tematica
tema_escogido = tk.StringVar()
tema_escogido.set(None)

#radiobuttons para las tematicas
radio_frutas = tk.Radiobutton(root, text="Frutas", variable=tema_escogido, value="Frutas", command=elegir_tematica)
radio_frutas.pack()

radio_informatica = tk.Radiobutton(root, text="Conceptos informáticos", variable=tema_escogido, value="Conceptos informáticos", command=elegir_tematica)
radio_informatica.pack()

radio_personas = tk.Radiobutton(root, text="Nombres de personas", variable=tema_escogido, value="Nombres de personas", command=elegir_tematica)
radio_personas.pack()

btn_jugar = tk.Button(root, text="Jugar", command=jugar)
btn_jugar.pack(pady=20)


root.mainloop()
