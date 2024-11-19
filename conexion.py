import mysql.connector
from mysql.connector import Error  # Importación correcta de Error

class Conexion:
    def __init__(self):
        self.conn = None

    def conectar(self):
        try:

            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="Ahorcado"
            )
            if self.conn.is_connected():
                print("Conexión exitosa")
                return True
        except mysql.connector.Error as err:
            print(f"Error de conexión: {err}")
            return False

    def verificar_jugador(self, nombre):
        if not self.conn:
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Jugador WHERE nombre = %s", (nombre,))
            jugador = cursor.fetchone()
            cursor.close()
            return jugador is not None
        except mysql.connector.Error as err:
            print(f"Error al verificar jugador: {err}")
            return False

    def actualizar_estadisticas(self, nombre, victoria):
        if not self.conn:
            return

        try:
            cursor = self.conn.cursor()
            if victoria:
                cursor.execute("UPDATE Jugador SET victorias = victorias + 1 WHERE nombre = %s", (nombre,))
            else:
                cursor.execute("UPDATE Jugador SET derrotas = derrotas + 1 WHERE nombre = %s", (nombre,))
            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error al actualizar estadísticas: {err}")

    def obtener_estadisticas(self):
        if not self.conn or not self.conn.is_connected():
            print("La conexión no está activa.")
            return []
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT nombre, victorias, derrotas FROM Jugador")
            usuarios = cursor.fetchall()
            print(f"Usuarios recuperados: {usuarios}")
            return usuarios
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return []

    def insertar_jugador(self, nombre):
        if not self.conn:
            print("No hay conexión con la base de datos.")
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Jugador (nombre, victorias, derrotas) VALUES (%s, 0, 0)", (nombre,))
            self.conn.commit()
            cursor.close()
            print(f"Jugador {nombre} insertado correctamente.")
            return True
        except mysql.connector.Error as err:
            print(f"Error al insertar jugador: {err}")
            return False

    def cerrar(self):
        if self.conn:
            self.conn.close()
            print("Conexión cerrada")
