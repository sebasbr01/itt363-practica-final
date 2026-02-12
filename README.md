## Implementación de conexión base de datos

## Simulación de Estación Meteorológica MQTT con Persistencia en MySQL (Grupo 2)

Este proyecto implementa una simulación de estaciones meteorológicas IoT utilizando el protocolo MQTT. El sistema genera datos sintéticos de sensores (Temperatura, Humedad, Viento) y los transmite al servidor MQTT de la escuela. Además, la información recibida es persistida en una base de datos relacional MySQL mediante un cliente subscriptor desarrollado en Python.

El sistema completo cumple con la jerarquía de tópicos solicitada y permite el almacenamiento histórico de las mediciones para su posterior análisis.

## Grupo 2 - Proyecto Integrador

Grupo: itt363-grupo2_pasalucha

## Descripción General del Sistema

    El sistema está compuesto por:

    Un simulador MQTT (simulador.py), que genera datos meteorológicos sintéticos.

    Un cliente subscriptor MQTT (monitor.py), que recibe los mensajes y los persiste en una base de datos MySQL.

    Una base de datos relacional MySQL, que almacena estaciones, sensores y mediciones.

    Un modelo entidad–relación normalizado, que garantiza integridad referencial.

## Estructura del Proyecto

    El repositorio contiene los siguientes módulos:

    simulador.py: Publicador MQTT. Simula múltiples estaciones meteorológicas (por defecto "EST-NORTE" y "EST-SUR") que operan en hilos independientes, generando y enviando datos cada 5 segundos.

    monitor.py: Subscriptor MQTT con persistencia. Se conecta al broker, recibe los mensajes y almacena la información en una base de datos MySQL.

    schema.sql: Script SQL para la creación de la base de datos y sus tablas.

    requirements.txt: Lista de dependencias necesarias para ejecutar el proyecto.

    README.md: Documentación del proyecto.

## Requisitos Previos


    Conexión a la VPN de la PUCMM: Es indispensable estar conectado a la red de la universidad (vía VPN o conexión local) para poder alcanzar el broker mqtt.eict.ce.pucmm.edu.do. Sin esta conexión, el script no podrá conectarse.
    Python 3.x

    MySQL Community Server (puede que se necesario crear la base de datos X con anterioridad)

    Librerías Python:

    paho-mqtt

    mysql-connector-python

## Instalación y Configuración
1. Instalación de MySQL

    Descargar MySQL Community Server desde (elegir la segunda/última opción):
    https://dev.mysql.com/downloads/installer/ 

    Durante la instalación:

    Seleccionar MySQL Server

    Configurar usuario y contraseña

    Puerto por defecto: 3306

    Verificar la instalación:

    mysql --version

## 2. Creación del entorno virtual

    Desde la carpeta del proyecto:

    python -m venv venv


    Activar el entorno:

    Windows (PowerShell):

    venv\Scripts\activate


## 3. Instalación de dependencias
    pip install -r requirements.txt


    O manualmente:

    pip install paho-mqtt mysql-connector-python

## 4. Creación de la base de datos

Ejecutar el archivo schema.sql desde VS Code (SQLTools) -Una vez añadida la conexión a la base de datos con MySQL Community Server a tráves de SQLTools se puede usar la opción de correr desde la conexión activa directamente- o desde la consola MySQL:

    CREATE DATABASE IF NOT EXISTS meteorologia;
    USE meteorologia;

    CREATE TABLE IF NOT EXISTS estacion (
        id_estacion INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS sensor (
        id_sensor INT AUTO_INCREMENT PRIMARY KEY,
        tipo VARCHAR(50),
        unidad VARCHAR(10),
        id_estacion INT,
        FOREIGN KEY (id_estacion) REFERENCES estacion(id_estacion)
    );

    CREATE TABLE IF NOT EXISTS medicion (
        id_medicion INT AUTO_INCREMENT PRIMARY KEY,
        valor DECIMAL(10,2),
        fecha DATETIME,
        id_sensor INT,
        FOREIGN KEY (id_sensor) REFERENCES sensor(id_sensor)
    );

## Guía de Uso
Paso 1: Iniciar el Monitor (Subscriptor + Persistencia)
python monitor.py


    Este script:

    Se conecta al broker MQTT.

    Se suscribe al tópico /itt363-grupo2/#.

    Recibe los mensajes.

    Procesa los datos.

    Inserta automáticamente la información en MySQL.

Paso 2: Iniciar la Simulación (Publicador)

    En una segunda terminal:

    python simulador.py


## Este script:

    Simula estaciones meteorológicas.

    Genera valores aleatorios.

    Publica los datos cada 5 segundos.

## Detalles Técnicos
Jerarquía de Tópicos

Se implementó la siguiente estructura para garantizar escalabilidad y orden:

    /itt363-grupo2/estacion/{ID_ESTACION}/sensores/{TIPO_SENSOR}

Ejemplos:
    /itt363-grupo2/estacion/EST-NORTE/sensores/temperatura
    /itt363-grupo2/estacion/EST-SUR/sensores/viento

## Simulación Concurrente

El archivo simulador.py utiliza la librería threading para ejecutar cada estación como un hilo independiente. Esto permite simular múltiples estaciones de forma concurrente sin bloquear la ejecución principal.

## Persistencia de Datos

La persistencia se implementa dentro del archivo monitor.py, específicamente en la función:

def on_message(client, userdata, msg):


Dentro de esta función se realizan las siguientes operaciones:

    Recepción del mensaje MQTT

    Interpretación del tópico

    Conexión a MySQL

    Inserción de la estación si no existe

    Inserción del sensor si no existe

    Inserción de la medición

    Confirmación de la transacción con commit()

Esto garantiza el almacenamiento permanente de los datos recibidos.

## Verificación del Funcionamiento

Ejecutar en MySQL:

SELECT * FROM estacion;
SELECT * FROM sensor;
SELECT * FROM medicion;


##  Consulta completa de verificación:

SELECT 
    e.nombre AS estacion,
    s.tipo AS sensor,
    m.valor,
    s.unidad,
    m.fecha
FROM medicion m
JOIN sensor s ON m.id_sensor = s.id_sensor
JOIN estacion e ON s.id_estacion = e.id_estacion
ORDER BY m.fecha DESC;

##  Resultados Esperados

    Recepción correcta de mensajes MQTT

    Persistencia automática en MySQL

    Integridad referencial garantizada

    No duplicación de estaciones ni sensores

    Registro histórico de mediciones