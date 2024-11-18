-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS Ahorcado;
USE Ahorcado;

-- Crear la tabla Jugador
CREATE TABLE IF NOT EXISTS Jugador (
    id_jugador INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    victorias INT DEFAULT 0,
    derrotas INT DEFAULT 0 
);

-- Crear la tabla Partida
CREATE TABLE IF NOT EXISTS Partida (
    id_partida INT AUTO_INCREMENT PRIMARY KEY,
    id_jugador INT NOT NULL,
    palabra VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_jugador) REFERENCES Jugador(id_jugador)
);

-- jugadores de ejemplo
INSERT INTO Jugador (nombre) 
VALUES 
('Raul martin'),
('Martin');

-- partidas de ejemplo
INSERT INTO Partida (id_jugador, palabra)
VALUES
(1, 'python'),
(1, 'java'),
(2, 'javascript'),
(2, 'csharp');