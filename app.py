from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# --- CONFIGURACIÓN MYSQL ---
DB_HOST = "192.168.100.152"
DB_USER = "itt363-grupo2"
DB_PASS = "12345678"
DB_NAME = "estacion_meteorologica"

def obtener_datos():
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=3306
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT estacion, sensor, valor, unidad, fecha FROM lecturas ORDER BY id DESC LIMIT 50")
        datos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return datos
    except mysql.connector.Error as err:
        print(f"Error de base de datos: {err}")
        return []

@app.route('/')
def index():
    datos_sensores = obtener_datos()
    return render_template('index.html', lecturas=datos_sensores)

if __name__ == '__main__':
    print("--- INICIANDO SERVIDOR WEB ---")
    print("Abre navegador en: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)