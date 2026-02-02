import paho.mqtt.client as mqtt
import random # Importamos random para el ID unico

# --- CONFIGURACIÓN GRUPO 2 ---
BROKER = "mqtt.eict.ce.pucmm.edu.do"
PORT = 1883
USER = "itt363-grupo2"
PASS = "knDH2P6N4w9g"
TOPIC_ROOT = f"/{USER}/#"

# Ajuste Compatibilidad Paho v2
try:
    from paho.mqtt.enums import CallbackAPIVersion
    VERSION_API = CallbackAPIVersion.VERSION2
except ImportError:
    VERSION_API = None

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f" MONITOR CONECTADO ({USER})")
        print(f" Escuchando en: {TOPIC_ROOT}")
        client.subscribe(TOPIC_ROOT)
    else:
        print(f" Error de conexión: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        topic = msg.topic
        
        # Parseo: /itt363-grupo2/estacion/ID/sensores/TIPO
        partes = topic.split("/")
        
        if len(partes) >= 6:
            estacion = partes[3]
            sensor = partes[5]
            # Usamos ljust para que quede alineado bonito en columnas
            print(f" [{estacion}] {sensor.upper().ljust(12)}: {payload}")
        else:
            print(f" {topic}: {payload}")
            
    except Exception as e:
        print(f"Error procesando mensaje: {e}")

# --- GENERAR ID ÚNICO ---
# Esto evita el conflicto si se te quedó otro proceso abierto
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
    print(f"Conectando al broker como {client_id_monitor}...")
    client.connect(BROKER, PORT, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("\nMonitor detenido.")