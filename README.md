# Simulación de Estación Meteorológica MQTT (Grupo 2)

Este proyecto implementa una simulación de estaciones meteorológicas IoT utilizando el protocolo MQTT. El sistema genera datos sintéticos de sensores (Temperatura, Humedad, Viento) y los transmite al servidor público de la escuela, cumpliendo con la jerarquía de tópicos solicitada.

## Integrantes
 * Rishelvis Tavarez
 * Sebastián Bencosme
* **Grupo:** itt363-grupo2

## Estructura del Proyecto

El repositorio contiene los siguientes módulos:

* `simulador.py`: **Publicador**. Simula múltiples estaciones meteorológicas (por defecto "EST-NORTE" y "EST-SUR") que operan en hilos independientes, generando y enviando datos cada 5 segundos.
* `monitor.py`: **Suscriptor**. Se conecta al broker y escucha todos los mensajes bajo el tópico del grupo (`/itt363-grupo2/#`), mostrando los datos formateados en la consola en tiempo real.
* `requirements.txt`: Lista de dependencias necesarias para ejecutar el proyecto.

## Requisitos Previos

* **Conexión a la VPN de la PUCMM:** Es indispensable estar conectado a la red de la universidad (vía VPN o conexión local) para poder alcanzar el broker `mqtt.eict.ce.pucmm.edu.do`. Sin esta conexión, el script no podrá conectarse.
* Python 3.x
* Librería `paho-mqtt`

## Instalación

1.  Se recomienda utilizar un entorno virtual:
    python3 -m venv venv
    source venv/bin/activate  # En Linux/Mac
    

2.  Instalar las dependencias:
    pip install -r requirements.txt
    

## Guía de Uso

El sistema está diseñado para funcionar de manera autónoma sin configuración manual de credenciales.

### Paso 1: Iniciar el Monitor
Abra una terminal y ejecute el monitor. Este quedará en espera de datos.
python3 monitor.py

### Paso 2: Iniciar la Simulación
Abra una segunda terminal (manteniendo el monitor abierto) y ejecute el simulador.
python3 simulador.py

### Detalles Técnicos
## Jerarquía de Tópicos
    Se implementó la siguiente estructura para garantizar escalabilidad y orden: /itt363-grupo2/estacion/{ID_ESTACION}/sensores/{TIPO_SENSOR}

## Ejemplo de publicación:

/itt363-grupo2/estacion/EST-NORTE/sensores/temperatura

/itt363-grupo2/estacion/EST-SUR/sensores/viento

### Simulación Concurrente
El simulador.py utiliza la librería threading para instanciar cada estación como un proceso ligero independiente. Esto permite escalar la simulación a 'N' estaciones sin bloquear el hilo principal de ejecución.