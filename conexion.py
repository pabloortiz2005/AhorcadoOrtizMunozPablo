# conexion.py

import mysql.connector

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
        except mysql.connector.Error as err:
            print(f"Error de conexión: {err}")
            return False
        return True

    def verificar_jugador(self, nombre):
        if not self.conn:
            return False

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Jugador WHERE nombre = %s", (nombre,))
        jugador = cursor.fetchone()
        return jugador is not None

    def actualizar_estadisticas(self, nombre, victoria):
        if not self.conn:
            return

        cursor = self.conn.cursor()
        if victoria:
            cursor.execute("UPDATE Jugador SET victorias = victorias + 1 WHERE nombre = %s", (nombre,))
        else:
            cursor.execute("UPDATE Jugador SET derrotas = derrotas + 1 WHERE nombre = %s", (nombre,))
        self.conn.commit()

    def cerrar(self):
        if self.conn:
            self.conn.close()
