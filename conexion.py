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
        if not self.conn:
            return []

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT nombre, victorias, derrotas FROM Jugador")
            resultados = cursor.fetchall()
            cursor.close()

            # Depurar los resultados obtenidos
            print(f"Resultados obtenidos de la base de datos: {resultados}")

            return resultados
        except mysql.connector.Error as err:
            print(f"Error al obtener estadísticas: {err}")
            return []

    def insertar_jugador(self, nombre):
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Jugador (nombre, victorias, derrotas) VALUES (%s, 0, 0)", (nombre,))
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error al insertar jugador: {err}")
            return False
    def cerrar(self):
        if self.conn:
            self.conn.close()
            print("Conexión cerrada")
