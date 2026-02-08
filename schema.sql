-- Eliminación previa para evitar conflictos, en caso de que crearla manualmente cree conflictos
DROP DATABASE IF EXISTS meteorologia;

-- Creación de la base de datos
CREATE DATABASE meteorologia;
USE meteorologia;


-- TABLA: estacion: Representa una estación meteorológica física

CREATE TABLE estacion (
    id_estacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE
);

-- TABLA: sensor: Representa sensores asociados a una estación

CREATE TABLE sensor (
    id_sensor INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    unidad VARCHAR(10),
    id_estacion INT NOT NULL,
    FOREIGN KEY (id_estacion)
    REFERENCES estacion(id_estacion)
);


-- TABLA: medicion: Almacena las mediciones históricas

CREATE TABLE medicion (
    id_medicion INT AUTO_INCREMENT PRIMARY KEY,
    valor DECIMAL(10,2) NOT NULL,
    fecha DATETIME NOT NULL,
    id_sensor INT NOT NULL,
    FOREIGN KEY (id_sensor)
        REFERENCES sensor(id_sensor)
);
