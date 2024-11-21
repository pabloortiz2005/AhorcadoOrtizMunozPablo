import tkinter as tk
from tkinter import messagebox
import random
from conexion import Conexion

class Juego:
    def __init__(self, nombre, tematica):
        self.nombre = nombre
        self.tematica = tematica
        self.conn = Conexion()
        self.intentos = 6
        self.palabra_seleccionada = None
        self.letras_adivinadas = []


        self.conn.conectar()
        self.iniciar_ventana()

    def iniciar_ventana(self):
        palabras_frutas = ['manzana', 'plátano', 'piña', 'pomelo', 'limon']
        palabras_informatica = ['python', 'java', 'C#', 'kotlin', 'al']
        palabras_personas = ['pablo', 'martin', 'raul', 'rafa', 'niko']
        palabras = []


        if self.tematica == 'Frutas':
            palabras = palabras_frutas
        elif self.tematica == 'Conceptos informáticos':
            palabras = palabras_informatica
        elif self.tematica == 'Nombres de personas':
            palabras = palabras_personas

        self.palabra_seleccionada = random.choice(palabras)
        self.letras_adivinadas = ['_'] * len(self.palabra_seleccionada)

        self.ventana_juego = tk.Tk()
        self.ventana_juego.configure(bg='gray')
        self.ventana_juego.title("Juego Ahorcado")
        self.ventana_juego.geometry("1800x1800")

        self.imagenes_intentos = {
            6: tk.PhotoImage(file="resources/ahorcado.png"),
            5: tk.PhotoImage(file="resources/ahorcadokiko1.png"),
            4: tk.PhotoImage(file="resources/ahorcadokiko2.png"),
            3: tk.PhotoImage(file="resources/ahorcadokiko3.png"),
            2: tk.PhotoImage(file="resources/ahorcadokiko4.png"),
            1: tk.PhotoImage(file="resources/ahorcadokiko5.png"),
            0: tk.PhotoImage(file="resources/ahorcadokikodead.png")
        }

        self.imagen = tk.Label(self.ventana_juego, image=self.imagenes_intentos[6], bg="white")
        self.imagen.pack(pady=10)

        # Etiquetas y otros elementos de la ventana
        self.label_palabra = tk.Label(self.ventana_juego, text='_ ' * len(self.palabra_seleccionada),
                                      font=("Arial", 14))
        self.label_palabra.pack(pady=10)

        self.label_intentos = tk.Label(self.ventana_juego, text=f"Intentos restantes: {self.intentos}",
                                       font=("Arial", 12))
        self.label_intentos.pack(pady=10)

        label_ingresa_letra = tk.Label(self.ventana_juego, text="Ingresa una letra:")
        label_ingresa_letra.pack(pady=5)

        self.mete_letra = tk.Entry(self.ventana_juego, font=("Arial", 14))
        self.mete_letra.pack(pady=5)

        btn_comprobar = tk.Button(self.ventana_juego, text="Comprobar", command=self.comprobar_letra)
        btn_comprobar.pack(pady=20)

        btn_volver_a_jugar = tk.Button(self.ventana_juego, text="Volver a jugar", command=self.volver_a_jugar)
        btn_volver_a_jugar.pack(pady=20)

        btn_estadisticas = tk.Button(self.ventana_juego, text="Estadisticas", command=self.estadisticas)
        btn_estadisticas.pack(pady=20)

        self.ventana_juego.mainloop()

    def actualizar_imagen(self):
        # Actualizar la imagen según los intentos restantes
        self.imagen.config(image=self.imagenes_intentos.get(self.intentos, self.imagenes_intentos[0]))

    def comprobar_letra(self):
        letra = self.mete_letra.get().lower()
        self.mete_letra.delete(0, tk.END)

        if self.intentos <= 0:
            #se agotan intentos
            return

        if letra in self.palabra_seleccionada:
            for i in range(len(self.palabra_seleccionada)):
                if self.palabra_seleccionada[i] == letra:
                    self.letras_adivinadas[i] = letra
            self.label_palabra.config(text=' '.join(self.letras_adivinadas))

            # Verificar si ya se adivinó toda la palabra
            if '_' not in self.letras_adivinadas:
                # El jugador ha ganado
                messagebox.showinfo("Has ganado", f"{self.nombre} Adivinaste la palabra: {self.palabra_seleccionada}")
                self.conn.actualizar_estadisticas(self.nombre, True)

                # Deshabilitar todos los controles excepto el botón "Volver a jugar"
                self.mete_letra.config(state=tk.DISABLED)
                for b in self.ventana_juego.winfo_children():
                    if isinstance(b, tk.Button) and b.cget("text") not in ["Estadisticas","Volver a jugar"]:
                        b.config(state=tk.DISABLED)

                return
        else:
            # Restar un intento solo si aún quedan intentos
            self.intentos -= 1
            self.label_intentos.config(text=f"Intentos restantes: {self.intentos}")

            self.actualizar_imagen()

            if self.intentos == 0:

                messagebox.showinfo("Perdiste", f"La palabra era: {self.palabra_seleccionada}")
                self.conn.actualizar_estadisticas(self.nombre, False)

                # Deshabilitar todos los controles excepto el botón "Volver a jugar"
                self.mete_letra.config(state=tk.DISABLED)

                for b in self.ventana_juego.winfo_children():
                    if isinstance(b, tk.Button) and b.cget("text") not in ["Estadisticas", "Volver a jugar"]:
                        b.config(state=tk.DISABLED)
                return

    def reiniciar_juego(self):
        # Restablecer intentos y palabra

        self.intentos = 6
        self.letras_adivinadas = []
        self.actualizar_imagen()


        palabras_frutas = ['manzana', 'plátano', 'piña', 'pomelo', 'limon']
        palabras_informatica = ['python', 'java', 'C#', 'kotlin', 'al']
        palabras_personas = ['pablo', 'martin', 'raul', 'rafa', 'niko']

        if self.tematica == 'Frutas':
            palabras = palabras_frutas
        elif self.tematica == 'Conceptos informáticos':
            palabras = palabras_informatica
        elif self.tematica == 'Nombres de personas':
            palabras = palabras_personas

        self.palabra_seleccionada = random.choice(palabras)
        self.letras_adivinadas = ['_'] * len(self.palabra_seleccionada)


        self.label_palabra.config(text='_ ' * len(self.palabra_seleccionada))
        self.label_intentos.config(text=f"Intentos restantes: {self.intentos}")

    def volver_a_jugar(self):
        # Restablecer intentos y palabra
        self.reiniciar_juego()


        self.mete_letra.config(state=tk.NORMAL)
        self.label_palabra.config(state=tk.NORMAL)
        self.label_intentos.config(state=tk.NORMAL)


        for b in self.ventana_juego.winfo_children():
            if isinstance(b, tk.Button):
                if b.cget("text") != "Volver a jugar":
                    b.config(state=tk.NORMAL)


    def estadisticas(self):
        # Crear ventana de estadísticas
        ventana_estadisticas = tk.Toplevel(self.ventana_juego)  # Ventana secundaria
        ventana_estadisticas.title("Estadísticas de Usuarios")

        usuarios = self.conn.obtener_estadisticas()


        #print(usuarios)

        if not usuarios:
            messagebox.showinfo("Sin estadísticas", "No hay usuarios registrados aún.")
            ventana_estadisticas.destroy()  # Cerrar la ventana si no hay registros
            return

        # Encabezado de la ventana
        encabezado = tk.Label(ventana_estadisticas, text="Estadísticas de los Jugadores", font=("Arial", 14, "bold"))
        encabezado.pack(pady=10)

        # Mostrar las estadísticas de cada usuario
        for usuario, victorias, derrotas in usuarios:
            texto_usuario = f"{usuario}: {victorias} victorias, {derrotas} derrotas"
            label_usuario = tk.Label(ventana_estadisticas, text=texto_usuario, font=("Arial", 12))
            label_usuario.pack()

        # Botón para cerrar la ventana de estadísticas
        btn_cerrar = tk.Button(ventana_estadisticas, text="Cerrar", command=ventana_estadisticas.destroy)
        btn_cerrar.pack(pady=20)


