DROP SCHEMA IF EXISTS `certificacion_constanza` ;

-- -----------------------------------------------------
-- Schema esquema_t
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `certificacion_constanza` DEFAULT CHARACTER SET utf8mb3 ;
USE `certificacion_constanza`  ;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(70) NOT NULL,
    apellido VARCHAR(70) NOT NULL,
    email VARCHAR(45) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- Crear tabla de películas
CREATE TABLE IF NOT EXISTS peliculas (
    id INT NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(100) NOT NULL UNIQUE,
    sinopsis TEXT NOT NULL,
    director VARCHAR(100) NOT NULL,
    fecha_estreno DATE NOT NULL,
    usuario_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- Crear tabla de comentarios
CREATE TABLE IF NOT EXISTS comentarios (
    id INT NOT NULL AUTO_INCREMENT,
    contenido TEXT NOT NULL,
    pelicula_id INT NOT NULL,
    usuario_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) 
|| ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;