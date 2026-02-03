import paho.mqtt.client as mqtt
import random
import json

# --- CONFIGURACIÓN GRUPO 2 ---
BROKER = "mqtt.eict.ce.pucmm.edu.do"
PORT = 1883
USER = "itt363-grupo2"
PASS = "knDH2P6N4w9g"
TOPIC_ROOT = f"/{USER}/#"

try:
    from paho.mqtt.enums import CallbackAPIVersion
    VERSION_API = CallbackAPIVersion.VERSION2
except ImportError:
    VERSION_API = None

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"MONITOR CONECTADO ({USER})")
        print(f"Escuchando en: {TOPIC_ROOT}")
        client.subscribe(TOPIC_ROOT)
    else:
        print(f"Error de conexión: {rc}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        topic = msg.topic
        
        # Intentamos parsear como JSON
        try:
            data = json.loads(payload_str)
            valor = data.get("valor")
            fecha = data.get("fecha")
            unidad = data.get("unidad", "")
            es_json = True
        except json.JSONDecodeError:
            # Si no es JSON (por si acaso), lo tratamos como texto plano
            valor = payload_str
            fecha = "Sin fecha"
            unidad = ""
            es_json = False
        
        # Parseo del Tópico
        partes = topic.split("/")
        if len(partes) >= 6:
            estacion = partes[3]
            sensor = partes[5]
            
            # Formato de salida profesional
            # [ESTACION] SENSOR | VALOR | FECHA
            texto_sensor = sensor.upper().ljust(12)
            texto_valor = f"{valor}{unidad}".ljust(10)
            
            print(f"[{estacion}] {texto_sensor} | {texto_valor} | {fecha}")
        else:
            print(f"{topic}: {payload_str}")
            
    except Exception as e:
        print(f"Error procesando mensaje: {e}")

# Generar ID aleatorio
aleatorio = random.randint(1000, 9999)
client_id_monitor = f"Monitor_{USER}_{aleatorio}"

if VERSION_API:
    client = mqtt.Client(client_id=client_id_monitor, callback_api_version=VERSION_API)
else:
    client = mqtt.Client(client_id=client_id_monitor)

client.username_pw_set(USER, PASS)
client.on_connect = on_connect
client.on_message = on_message

try:
    print(f"Conectando al broker...")
    client.connect(BROKER, PORT, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("\nMonitor detenido.")