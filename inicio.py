# inicio.py

import tkinter as tk
from tkinter import messagebox
from juego import Juego
from conexion import Conexion

class Inicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Ahorcado - Inicio")
        self.root.geometry("400x400")
        self.tematica_elegida = None
        self.conn = Conexion()

        self.crear_widgets()

    def crear_widgets(self):
        label_nombre = tk.Label(self.root, text="Ingresa tu nombre:")
        label_nombre.pack(pady=10)

        self.entry_nombre = tk.Entry(self.root, font=("Arial", 14))
        self.entry_nombre.pack(pady=10)

        label_tematica = tk.Label(self.root, text="Selecciona una temática:")
        label_tematica.pack(pady=10)

        self.tema_escogido = tk.StringVar()
        self.tema_escogido.set(None)

        radio_frutas = tk.Radiobutton(self.root, text="Frutas", variable=self.tema_escogido, value="Frutas", command=self.elegir_tematica)
        radio_frutas.pack()

        radio_informatica = tk.Radiobutton(self.root, text="Conceptos informáticos", variable=self.tema_escogido, value="Conceptos informáticos", command=self.elegir_tematica)
        radio_informatica.pack()

        radio_personas = tk.Radiobutton(self.root, text="Nombres de personas", variable=self.tema_escogido, value="Nombres de personas", command=self.elegir_tematica)
        radio_personas.pack()

        btn_jugar = tk.Button(self.root, text="Jugar", command=self.jugar)
        btn_jugar.pack(pady=20)

    def elegir_tematica(self):
        self.tematica_elegida = self.tema_escogido.get()

    def jugar(self):
        nombre = self.entry_nombre.get()

        if nombre == "":
            messagebox.showwarning("Ingresa Nombre", "Por favor ingresa tu nombre")
            return

        if not self.conn.conectar():
            messagebox.showerror("Error de conexión", "No se pudo conectar con la base de datos.")
            return

        if self.conn.verificar_jugador(nombre):
            messagebox.showinfo("Jugador encontrado", f"Hola {nombre}")
        else:
            messagebox.showinfo("Nuevo jugador", f"Hola, {nombre}, Se ha creado tu perfil")

        self.root.destroy()
        Juego(nombre, self.tematica_elegida)
