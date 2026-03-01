import paho.mqtt.client as mqtt
import mysql.connector
import random
import json

# --- CONFIGURACIÓN MQTT ---
BROKER = "mqtt.eict.ce.pucmm.edu.do"
PORT = 1883
USER_MQTT = "itt363-grupo2"
PASS_MQTT = "knDH2P6N4w9g"
TOPIC_ROOT = f"/{USER_MQTT}/#"  # <--- Faltaba esta línea

# --- CONFIGURACIÓN MYSQL ---
DB_HOST = "192.168.100.152"
DB_USER = "itt363-grupo2"
DB_PASS = "12345678"
DB_NAME = "estacion_meteorologica"

try:
    from paho.mqtt.enums import CallbackAPIVersion
    VERSION_API = CallbackAPIVersion.VERSION2
except ImportError:
    VERSION_API = None

def guardar_en_mysql(estacion, sensor, valor, unidad, fecha):
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=3306
        )
        cursor = conexion.cursor()
        sql = "INSERT INTO lecturas (estacion, sensor, valor, unidad, fecha) VALUES (%s, %s, %s, %s, %s)"
        valores = (estacion, sensor, valor, unidad, fecha)
        
        cursor.execute(sql, valores)
        conexion.commit()
        
        cursor.close()
        conexion.close()
        return True
    except mysql.connector.Error as err:
        print(f" Error de MySQL: {err}")
        return False

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f" MONITOR CONECTADO AL BROKER ({USER_MQTT})")
        client.subscribe(TOPIC_ROOT)
    else:
        print(f" Error de conexión MQTT: {rc}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        topic = msg.topic
        
        try:
            data = json.loads(payload_str)
            valor = data.get("valor")
            fecha = data.get("fecha")
            unidad = data.get("unidad", "")
        except json.JSONDecodeError:
            return 
        
        partes = topic.split("/")
        if len(partes) >= 6:
            estacion = partes[3]
            sensor = partes[5]
            
            if guardar_en_mysql(estacion, sensor, valor, unidad, fecha):
                texto_sensor = sensor.upper().ljust(12)
                texto_valor = f"{valor}{unidad}".ljust(10)
                print(f" Guardado DB: [{estacion}] {texto_sensor} | {texto_valor} | {fecha}")
            
    except Exception as e:
        print(f"Error general: {e}")

aleatorio = random.randint(1000, 9999)
client_id_monitor = f"Monitor_{USER_MQTT}_{aleatorio}"

if VERSION_API:
    client = mqtt.Client(client_id=client_id_monitor, callback_api_version=VERSION_API)
else:
    client = mqtt.Client(client_id=client_id_monitor)

# <--- Aquí estaba el otro error (decía PASS en vez de PASS_MQTT arriba)
client.username_pw_set(USER_MQTT, PASS_MQTT)
client.on_connect = on_connect
client.on_message = on_message

try:
    print(f"Conectando al broker MQTT en {BROKER}...")
    client.connect(BROKER, PORT, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("\nMonitor detenido.")