from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# --- CONFIGURACIÓN MYSQL ---
DB_HOST = "127.0.0.1"
DB_USER = "itt363-grupo2"
DB_PASS = "12345678"
DB_NAME = "estacion_meteorologica"

def obtener_conexion():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, port=3306
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/lecturas')
def api_lecturas():
    """API de Paginación Keyset (Basado en el artículo de jOOQ)"""
    last_id = request.args.get('last_id', type=int)
    first_id = request.args.get('first_id', type=int)
    limit = 10
    
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    
    # Lógica de Paginación Keyset (Sin usar OFFSET para mayor eficiencia)
    if last_id: # Botón Siguiente (buscar más viejos)
        cursor.execute("SELECT * FROM lecturas WHERE id < %s ORDER BY id DESC LIMIT %s", (last_id, limit))
        datos = cursor.fetchall()
    elif first_id: # Botón Anterior (buscar más nuevos)
        cursor.execute("SELECT * FROM lecturas WHERE id > %s ORDER BY id ASC LIMIT %s", (first_id, limit))
        datos = cursor.fetchall()
        datos.reverse() # Invertimos para mantener el orden visual descendente
    else: # Primera carga
        cursor.execute("SELECT * FROM lecturas ORDER BY id DESC LIMIT %s", (limit,))
        datos = cursor.fetchall()
        
    # Calcular total de páginas (solo como referencia visual)
    cursor.execute("SELECT COUNT(*) as total FROM lecturas")
    total_rows = cursor.fetchone()['total']
    total_pages = (total_rows + limit - 1) // limit if total_rows > 0 else 1
    
    cursor.close()
    conexion.close()
    
    return jsonify({'datos': datos, 'total_pages': total_pages})

if __name__ == '__main__':
    print("--- INICIANDO SERVIDOR WEB (PUERTO 8080) ---")
    app.run(host='0.0.0.0', port=8080)