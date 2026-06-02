import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Habilitamos CORS para permitir que el frontend alojado en Vercel se comunique con este backend
CORS(app) 

DATABASE = 'database.db'

def get_db_connection():
    """Establece una conexión limpia con la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE)
    # Permite acceder a las columnas por su nombre en lugar de por índices numéricos
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """Crea las tablas de forma automática e inserta datos de prueba si están vacías."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Crear tabla de usuarios según la especificación del examen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL
        )
    ''')
    
    # 2. Crear tabla de productos según la especificación del examen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL,
            stock INTEGER,
            categoria TEXT
        )
    ''')
    
    # Insertar un usuario administrador por defecto si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (username, password, nombre) VALUES (?, ?, ?)", 
                       ('admin', '1234', 'Administrador del Sistema'))
        
    # Insertar algunos productos de hardware informático de prueba si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO productos (codigo, nombre, descripcion, precio, stock, categoria) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('P001', 'Tarjeta Gráfica GTX 1650', 'Memoria GDDR6 de 4GB, ideal para setups de entrada.', 650.00, 5, 'Hardware'))
        
        cursor.execute('''
            INSERT INTO productos (codigo, nombre, descripcion, precio, stock, categoria) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('P002', 'Fuente de Poder GameMax VP-500W', 'Potencia de 500W reales con certificación 80 Plus Bronze.', 180.00, 12, 'Componentes'))
        
        cursor.execute('''
            INSERT INTO productos (codigo, nombre, descripcion, precio, stock, categoria) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('P003', 'Memoria RAM 16GB DDR4', 'Módulo de alta velocidad a 3200MHz para optimización del sistema.', 240.00, 20, 'Memorias'))
        
    conn.commit()
    conn.close()

@app.route("/")
def home():
    """Ruta raíz para verificar que el servicio responda correctamente en Render."""
    return jsonify({
        "estado": "Exito",
        "mensaje": "¡El backend en Render está funcionando perfectamente!"
    })

@app.route("/api/buscar_producto", methods=["POST"])
def buscar_producto():
    """API en formato JSON para buscar un producto por su código único."""
    data = request.get_json()
    
    # Validación de seguridad del JSON entrante
    if not data or 'codigo' not in data:
        return jsonify({"encontrado": False, "mensaje": "Código no proporcionado en la petición"}), 400
        
    codigo_buscado = data['codigo'].strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Consulta SQL parametrizada para evitar inyecciones SQL
    cursor.execute("SELECT nombre, descripcion, precio, stock, categoria FROM productos WHERE codigo = ?", (codigo_buscado,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        # Construcción de la respuesta con los campos requeridos
        producto_data = {
            "nombre": row["nombre"],
            "descripcion": row["descripcion"],
            "precio": row["precio"],
            "stock": row["stock"],
            "categoria": row["categoria"]
        }
        return jsonify({
            "encontrado": True,
            "producto": producto_data
        }), 200
    else:
        return jsonify({
            "encontrado": False,
            "mensaje": "Producto no encontrado en el inventario"
        }), 404

init_db()

if __name__ == "__main__":
    # Inicializa de manera segura la base de datos local antes de levantar el servidor
    
    # El examen indica que Render utilizará preferentemente el puerto 10000
    app.run(debug=True, port=10000)