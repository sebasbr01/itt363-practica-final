# Librerías

# Librería para manejar el protocolo MQTT
import paho.mqtt.client as mqtt
# Conector oficial de MySQL para Python
import mysql.connector
# Para decodificar los mensajes en formato JSON
import json
# Para generar un identificador aleatorio del cliente MQTT
import random


# CONFIGURACIÓN MQTT
# Dirección del broker MQTT institucional
BROKER = "mqtt.eict.ce.pucmm.edu.do"

# Puerto estándar para MQTT sin TLS
PORT = 1883

# Credenciales del grupo
USER = "itt363-grupo2"
PASS = "knDH2P6N4w9g"

# Suscripción a todos los tópicos del grupo
TOPIC = f"/{USER}/#"

# CONFIGURACIÓN MYSQL

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",          # Servidor de base de datos
    user="root",               # Usuario MySQL
    password="LongAF_Infinity",# Contraseña MySQL, está constraseña debe adaptarse a cada usuario o base de datos. (Actualmente está configurada en MySQL 8.0)
    database="meteorologia"    # Base de datos utilizada (se puede usar de la base de datos mysql por defecto, ya que es neecesario crear la base de datos en MySQL Workbench con la sentencia: CREATE DATABASE IF NOT EXISTS meteorologia;)
)

# PORRR FIN, SOLUCIÓN AL PROBLEMA  - "Unread result found"
# Cursor buffered evita el error al permitir consumir completamente los resultados: Este error ocurre cuando se ejecuta una nueva instrucción SQL en la misma conexión (y a menudo en el mismo cursor) antes de que todos los resultados de la consulta anterior hayan sido completamente recuperados y procesados.

cursor = db.cursor(buffered=True)

#Evita errores de "resultado no leído": Sin un cursor con búfer, debes obtener todos los resultados de una consulta antes de ejecutar cualquier otra sentencia en la misma conexión. No hacerlo genera un error Interno (Resultado no leído encontrado). El cursor con búfer evita este problema porque la conexión ya no está "bloqueada" esperando que se lean los resultados.
#Evita el error "Unread Result": Sin un cursor con buffer, debes obtener todos los resultados de una consulta antes de ejecutar cualquier otra instrucción en la misma conexión. No hacerlo genera un error interno (Resultado no leído encontrado). El cursor con búfer evita este problema porque la conexión ya no está "bloqueada" esperando que se lean los resultados.



# CALLBACK: CONEXIÓN MQTT
##    Se ejecuta automáticamente cuando el cliente se conecta al broker MQTT.
def on_connect(client, userdata, flags, rc):
    print("Intentando conectar al broker MQTT...")
    if rc == 0:
        print("Monitor conectado al broker MQTT")
        client.subscribe(TOPIC)
        print(f"📡 Suscrito al tópico: {TOPIC}")
    else:
        print("Error de conexión MQTT. Código:", rc) # Esto fue agregrado porque debido al una corrupción de parte de IDE no corría los scripts de python, se logró resolver.




# CALLBACK: MENSAJE RECIBIDO
def on_message(client, userdata, msg):
    """
    Se ejecuta cada vez que se recibe un mensaje MQTT.
    Procesa el mensaje y lo almacena en la base de datos.
    """
    try:
        # DECODIFICACIÓN DEL PAYLOAD
        
        # El payload viene en JSON
        data = json.loads(msg.payload.decode())

        valor = data["valor"]
        fecha = data["fecha"]
        unidad = data["unidad"]

        # EXTRACCIÓN DE DATOS DEL TÓPICO
        # Ejemplo:
        # /itt363-grupo2/estacion/EST-NORTE/sensores/temperatura
        
        partes = msg.topic.split("/")
        estacion = partes[3]
        sensor = partes[5]

        # TABLA: ESTACION
        # Verifica si la estación ya existe
        cursor.execute(
            "SELECT id_estacion FROM estacion WHERE nombre = %s",
            (estacion,)
        )
        row = cursor.fetchone()

        if row:
            # Estación ya existe
            id_estacion = row[0]
        else:
            # Inserta nueva estación
            cursor.execute(
                "INSERT INTO estacion (nombre) VALUES (%s)",
                (estacion,)
            )
            db.commit()
            id_estacion = cursor.lastrowid

        # TABLA: SENSOR
        
        # Verifica si el sensor ya existe para esa estación
        
        cursor.execute(
            """
            SELECT id_sensor
            FROM sensor
            WHERE tipo = %s AND id_estacion = %s
            """,
            (sensor, id_estacion)
        )
        row = cursor.fetchone()

        if row:
            # Sensor ya existe
            id_sensor = row[0]
        else:
            # Inserta nuevo sensor
            cursor.execute(
                """
                INSERT INTO sensor (tipo, unidad, id_estacion)
                VALUES (%s, %s, %s)
                """,
                (sensor, unidad, id_estacion)
            )
            db.commit()
            id_sensor = cursor.lastrowid

        # TABLA: MEDICION
        
        # Inserta la medición recibida
        cursor.execute(
            """
            INSERT INTO medicion (valor, fecha, id_sensor)
            VALUES (%s, %s, %s)
            """,
            (valor, fecha, id_sensor)
        )
        db.commit()

        # Mensaje en consola para monitoreo
        print(f"[{estacion}] {sensor.upper()} | {valor}{unidad} | {fecha}")

    except Exception as e:
        # Manejo general de errores
        print("ERROR:", e)


# CONFIGURACIÓN DEL CLIENTE MQTT

client = mqtt.Client(
    client_id=f"MONITOR_{random.randint(1000,9999)}"
)

# Credenciales del broker
client.username_pw_set(USER, PASS)

# Asignación de callbacks
client.on_connect = on_connect
client.on_message = on_message

# Conexión al broker
client.connect(BROKER, PORT, 60)

# Loop infinito para escuchar mensajes
client.loop_forever()
print("funciona")