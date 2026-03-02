import paho.mqtt.client as mqtt
import mysql.connector
import json

# --- CONFIGURACIÓN MQTT (PÚBLICO) ---
BROKER = "mqtt.eict.ce.pucmm.edu.do"
PORT = 1883
USER_MQTT = "itt363-grupo2"
PASS_MQTT = "knDH2P6N4w9g"
TOPIC_ROOT = f"/{USER_MQTT}/#"

# --- CONFIGURACIÓN MYSQL (REMOTA HACIA TU SERVIDOR) ---
# Aquí apuntamos a la IP del servidor de la PUCMM
DB_HOST = "192.168.100.152"
DB_USER = "itt363-grupo2"
DB_PASS = "12345678"
DB_NAME = "estacion_meteorologica"

def guardar_en_bd(estacion, sensor, valor, unidad, fecha):
    try:
        # Abrimos conexión por cada mensaje para evitar que se caiga si hay inactividad
        conexion = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, port=3306
        )
        cursor = conexion.cursor()
        sql = "INSERT INTO lecturas (estacion, sensor, valor, unidad, fecha) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (estacion, sensor, valor, unidad, fecha))
        conexion.commit()
        print(f" Guardado en MySQL Remoto: {estacion} - {sensor}: {valor}{unidad}")
        cursor.close()
        conexion.close()
    except mysql.connector.Error as err:
        print(f" Error guardando en BD: {err}")

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(" Monitor Local conectado al Broker MQTT.")
        client.subscribe(TOPIC_ROOT)
        print(f" Escuchando en el tópico: {TOPIC_ROOT}")
    else:
        print(f" Error de conexión MQTT: {rc}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        topic = msg.topic
        data = json.loads(payload_str)
        
        # Desarmamos el tópico para sacar los nombres
        partes = topic.split("/")
        if len(partes) >= 6:
            estacion = partes[3]
            sensor = partes[5]
            
            # Mandamos a guardar
            guardar_en_bd(estacion, sensor, data['valor'], data['unidad'], data['fecha'])
    except Exception as e:
        print(f" Error procesando mensaje: {e}")

# Inicializamos el cliente MQTT
client = mqtt.Client(client_id="monitor_local_sebas", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(USER_MQTT, PASS_MQTT)
client.on_connect = on_connect
client.on_message = on_message

print("--- INICIANDO MONITOR LOCAL ---")
try:
    client.connect(BROKER, PORT, 60)
    client.loop_forever() # Se queda escuchando infinitamente
except KeyboardInterrupt:
    print("\n Monitor detenido por el usuario.")
    client.disconnect()