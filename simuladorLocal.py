import paho.mqtt.client as mqtt
import time
import random
import json
from datetime import datetime

# --- CONFIGURACIÓN MQTT (PÚBLICO) ---
BROKER = "mqtt.eict.ce.pucmm.edu.do"
PORT = 1883
USER_MQTT = "itt363-grupo2"
PASS_MQTT = "knDH2P6N4w9g"

# Estaciones y sensores a simular
ESTACIONES = ["EST-NORTE", "EST-SUR"]
SENSORES = {
    "temperatura": {"min": 20.0, "max": 35.0, "unidad": "C"},
    "humedad": {"min": 40.0, "max": 95.0, "unidad": "%"},
    "viento": {"min": 0.0, "max": 40.0, "unidad": "km/h"}
}

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(" Simulador conectado al Broker MQTT exitosamente.")
    else:
        print(f" Error al conectar, código: {rc}")

# Inicializamos el cliente MQTT
client = mqtt.Client(client_id="simulador_local_sebas", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(USER_MQTT, PASS_MQTT)
client.on_connect = on_connect

print("--- INICIANDO SIMULADOR LOCAL ---")
client.connect(BROKER, PORT, 60)
client.loop_start() # Inicia el hilo de red en segundo plano

try:
    while True:
        for estacion in ESTACIONES:
            for sensor, specs in SENSORES.items():
                # Generar valor aleatorio
                valor = round(random.uniform(specs["min"], specs["max"]), 2)
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Empaquetar en JSON
                payload = {
                    "valor": valor,
                    "unidad": specs["unidad"],
                    "fecha": fecha_actual
                }
                
                # Construir el tópico exacto que espera la página web
                # Formato: /itt363-grupo2/estacion/EST-NORTE/sensor/temperatura
                topic = f"/{USER_MQTT}/estacion/{estacion}/sensor/{sensor}"
                
                # Publicar
                payload_json = json.dumps(payload)
                client.publish(topic, payload_json)
                print(f"📡 Enviado: {topic} -> {payload_json}")
                
                time.sleep(1) # Pequeña pausa entre sensores
        
        print(" Esperando 5 segundos para el próximo ciclo...\n")
        time.sleep(5)

except KeyboardInterrupt:
    print("\n Simulador detenido por el usuario.")
    client.loop_stop()
    client.disconnect()