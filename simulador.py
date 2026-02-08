# Librerías

import paho.mqtt.client as mqtt 
import time
import random
import threading
import json
from datetime import datetime


# CONFIGURACIÓN MQTT

BROKER = "mqtt.eict.ce.pucmm.edu.do" #dirección del broker
PORT = 1883 #puerto abierto par ael broker PUCMM
USER = "itt363-grupo2" #usuario del broker PUCMM
PASS = "knDH2P6N4w9g"  #Contraseña del broker PUCMM


# Compatibilidad con versiones nuevas de Paho MQTT
try:
    from paho.mqtt.enums import CallbackAPIVersion
    VERSION_API = CallbackAPIVersion.VERSION2
except ImportError:
    VERSION_API = None 


# CLASE ESTACIÓN METEOROLÓGICA

class EstacionMeteorologica(threading.Thread):
    """
    Simula una estación meteorológica independiente.
    Cada estación corre en su propio hilo.
    """

    def __init__(self, estacion_id):
        threading.Thread.__init__(self)
        self.estacion_id = estacion_id
        
        # ID único del cliente MQTT
        client_id_sim = f"Sim_{USER}_{estacion_id}"
        
        # Inicialización del cliente MQTT
        if VERSION_API:
            self.client = mqtt.Client(
                client_id=client_id_sim,
                callback_api_version=VERSION_API
            )
        else:
            self.client = mqtt.Client(client_id=client_id_sim)
            
        self.client.username_pw_set(USER, PASS)
        self.connected = False

    def on_connect(self, client, userdata, flags, rc, properties=None):
        """
        Se ejecuta al conectarse al broker.
        """
        if rc == 0:
            print(f"[{self.estacion_id}] Conectado.")
            self.connected = True
        else:
            print(f"[{self.estacion_id}] Error: {rc}")

    def run(self):
        """
        Lógica principal del hilo.
        Genera y publica datos periódicamente.
        """
        self.client.on_connect = self.on_connect
        try:
            self.client.connect(BROKER, PORT, 60)
            self.client.loop_start()

            while True:
                if self.connected:
                    # GENERACIÓN DE DATOS
                    
                    temp = round(random.uniform(22.0, 34.0), 2)
                    hum = round(random.uniform(60.0, 95.0), 2)
                    viento = round(random.uniform(5.0, 30.0), 2)

                    # Timestamp actual
                    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Tópico base de la estación
                    base_topic = f"/{USER}/estacion/{self.estacion_id}/sensores"
                    
                    # Payloads en formato JSON
                    payload_temp = json.dumps({"valor": temp, "fecha": ahora, "unidad": "C"})
                    payload_hum = json.dumps({"valor": hum, "fecha": ahora, "unidad": "%"})
                    payload_viento = json.dumps({"valor": viento, "fecha": ahora, "unidad": "km/h"})

                    # Publicación MQTT
                    self.client.publish(f"{base_topic}/temperatura", payload_temp)
                    self.client.publish(f"{base_topic}/humedad", payload_hum)
                    self.client.publish(f"{base_topic}/viento", payload_viento)

                    print(f"[{self.estacion_id}] Enviado a las {ahora}")
                
                time.sleep(5)

        except Exception as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            self.client.disconnect()


# EJECUCIÓN DEL SIMULADOR


if __name__ == "__main__":
    print("--- INICIANDO SIMULADOR CON TIMESTAMP ---")
    EstacionMeteorologica("EST-NORTE").start()  #Est-1
    EstacionMeteorologica("EST-SUR").start()    #Est-2
