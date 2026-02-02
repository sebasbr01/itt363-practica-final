import paho.mqtt.client as mqtt
import time
import random
import threading

# --- CONFIGURACIÓN GRUPO 2 ---
BROKER = "mqtt.eict.ce.pucmm.edu.do"
PORT = 1883
USER = "itt363-grupo2"
PASS = "knDH2P6N4w9g"

# Compatibilidad Paho v2 (Para evitar el Warning)
try:
    from paho.mqtt.enums import CallbackAPIVersion
    VERSION_API = CallbackAPIVersion.VERSION2
except ImportError:
    VERSION_API = None 

class EstacionMeteorologica(threading.Thread):
    def __init__(self, estacion_id):
        threading.Thread.__init__(self)
        self.estacion_id = estacion_id
        
        client_id_sim = f"Sim_{USER}_{estacion_id}"
        
        if VERSION_API:
            self.client = mqtt.Client(client_id=client_id_sim, callback_api_version=VERSION_API)
        else:
            self.client = mqtt.Client(client_id=client_id_sim)
            
        self.client.username_pw_set(USER, PASS)
        self.connected = False

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print(f"[{self.estacion_id}]  Conectado.")
            self.connected = True
        else:
            print(f"[{self.estacion_id}]  Error: {rc}")

    def run(self):
        self.client.on_connect = self.on_connect
        try:
            self.client.connect(BROKER, PORT, 60)
            self.client.loop_start()

            while True:
                if self.connected:
                    temp = round(random.uniform(22.0, 34.0), 2)
                    hum = round(random.uniform(60.0, 95.0), 2)
                    viento = round(random.uniform(5.0, 30.0), 2)

                    base_topic = f"/{USER}/estacion/{self.estacion_id}/sensores"
                    
                    self.client.publish(f"{base_topic}/temperatura", temp)
                    self.client.publish(f"{base_topic}/humedad", hum)
                    self.client.publish(f"{base_topic}/viento", viento)

                    print(f" [{self.estacion_id}] Enviado T:{temp}°C | H:{hum}%")
                
                time.sleep(5) 

        except Exception as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            self.client.disconnect()

if __name__ == "__main__":
    print(f"--- INICIANDO SIMULADOR (PUBLICADOR) ---")
    EstacionMeteorologica("EST-NORTE").start()
    EstacionMeteorologica("EST-SUR").start()