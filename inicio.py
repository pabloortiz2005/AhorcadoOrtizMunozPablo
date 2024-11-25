import tkinter as tk
from tkinter import messagebox
from juego import Juego
from conexion import Conexion

class Inicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Ahorcado - Inicio")
        self.root.geometry("1800x1800")
        self.tematica_elegida = None
        self.conn = Conexion()
        self.root.configure(bg='gray')

        self.crear_ventana()

    def crear_ventana(self):
        self.imagenes_intentos = {
            0: tk.PhotoImage(file="resources/kiko.png")
        }
        self.imagen = tk.Label(self.root, image=self.imagenes_intentos[0], bg="gray")
        self.imagen.pack(pady=10)

        label_nombre = tk.Label(self.root, text="Ingresa tu nombre:")
        label_nombre.pack(pady=10)

        self.entry_nombre = tk.Entry(self.root, font=("Arial", 14))
        self.entry_nombre.pack(pady=10)

        label_tematica = tk.Label(self.root, text="Selecciona una temática:")
        label_tematica.pack(pady=10)

        self.tema_escogido = tk.StringVar()
        self.tema_escogido.set(None)

        radio_frutas = tk.Radiobutton(self.root, text="Frutas", variable=self.tema_escogido, value="Frutas", command=self.elegir_tematica, bg="gray",font=("Arial", 14, "bold"))
        radio_frutas.pack()

        radio_informatica = tk.Radiobutton(self.root, text="Conceptos informáticos", variable=self.tema_escogido, value="Conceptos informáticos", command=self.elegir_tematica,bg="gray",font=("Arial", 14, "bold"))
        radio_informatica.pack()

        radio_personas = tk.Radiobutton(self.root, text="Nombres de personas", variable=self.tema_escogido, value="Nombres de personas", command=self.elegir_tematica,bg="gray",font=("Arial", 14, "bold"))
        radio_personas.pack()

        # Botón para jugar
        btn_jugar = tk.Button(self.root, text="Jugar", command=self.jugar)
        btn_jugar.pack(pady=20)


    def elegir_tematica(self):
        self.tematica_elegida = self.tema_escogido.get()

    def jugar(self):
        nombre = self.entry_nombre.get()

        if nombre == "":
            messagebox.showwarning("Ingresa Nombre", "Por favor ingresa tu nombre")
            return

        if not self.tematica_elegida:
            messagebox.showwarning("Selecciona una temática", "Por favor selecciona una temática para jugar.")
            return

        if not self.conn.conectar():
            messagebox.showerror("Error de conexión", "No se pudo conectar con la base de datos.")
            return

        if self.conn.verificar_jugador(nombre):
            messagebox.showinfo("Jugador encontrado", f"Hola {nombre}")
        else:
            if self.conn.insertar_jugador(nombre):
                messagebox.showinfo("Nuevo jugador", f"Hola, {nombre}, Se ha creado tu perfil")
            else:
                messagebox.showerror("Error", "Hubo un problema al crear tu perfil.")

        self.root.destroy()

        Juego(nombre, self.tematica_elegida)



