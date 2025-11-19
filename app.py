from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
from collections import defaultdict
import json

app = Flask(__name__)
CORS(app)

DB_NAME = "cookies_pedidos.db"
SABORES_VALIDOS = [
    "Pistacho", "Rocher", "Sweet", "Velvet", "Kinder", "Rasta",
    "Cadbury", "Milka", "Blackblock", "Coco", "Doublechocolate",
]

def get_db():
    """Obtiene conexión a la base de datos"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos si no existe"""
    if not os.path.exists(DB_NAME):
        conn = get_db()
        cursor = conn.cursor()
        
        # Crear tablas
        cursor.execute('''
            CREATE TABLE pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dia TEXT NOT NULL,
                nombre TEXT NOT NULL,
                precio_pedido REAL NOT NULL,
                precio_envio REAL DEFAULT 0.0,
                direccion TEXT,
                horario TEXT,
                pago INTEGER DEFAULT 0,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE pedido_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                sabor TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos (id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('CREATE INDEX idx_pedido_id ON pedido_items (pedido_id)')
        conn.commit()
        conn.close()
    else:
        # Verificar y actualizar columna pago si no existe
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(pedidos)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'pago' not in columns:
            cursor.execute('ALTER TABLE pedidos ADD COLUMN pago INTEGER DEFAULT 0')
            conn.commit()
        conn.close()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    """Obtiene todos los pedidos"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM pedidos ORDER BY dia, fecha_registro")
        pedidos_db = cursor.fetchall()
        
        pedidos_completos = []
        for pedido_row in pedidos_db:
            pedido_dict = dict(pedido_row)
            cursor.execute("SELECT sabor, cantidad FROM pedido_items WHERE pedido_id = ?", 
                         (pedido_dict['id'],))
            items_db = cursor.fetchall()
            pedido_dict['items'] = [dict(item) for item in items_db]
            pedidos_completos.append(pedido_dict)
        
        conn.close()
        return jsonify({"success": True, "pedidos": pedidos_completos})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/pedidos', methods=['POST'])
def crear_pedido():
    """Crea un nuevo pedido"""
    try:
        data = request.json
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("BEGIN TRANSACTION")
        
        sql_pedido = """
            INSERT INTO pedidos (dia, nombre, precio_pedido, precio_envio, direccion, horario)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql_pedido, (
            data['dia'],
            data['nombre'],
            data['precio_pedido'],
            data.get('precio_envio', 0),
            data.get('direccion', ''),
            data.get('horario', '')
        ))
        
        pedido_id = cursor.lastrowid
        
        sql_item = "INSERT INTO pedido_items (pedido_id, sabor, cantidad) VALUES (?, ?, ?)"
        for item in data['items']:
            cursor.execute(sql_item, (pedido_id, item['sabor'], item['cantidad']))
        
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "pedido_id": pedido_id})
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/pedidos/<int:pedido_id>', methods=['GET'])
def get_pedido(pedido_id):
    """Obtiene un pedido específico"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,))
        pedido_row = cursor.fetchone()
        
        if not pedido_row:
            conn.close()
            return jsonify({"success": False, "error": "Pedido no encontrado"}), 404
        
        pedido_dict = dict(pedido_row)
        cursor.execute("SELECT sabor, cantidad FROM pedido_items WHERE pedido_id = ?", (pedido_id,))
        items_db = cursor.fetchall()
        pedido_dict['items'] = [dict(item) for item in items_db]
        
        conn.close()
        return jsonify({"success": True, "pedido": pedido_dict})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/pedidos/<int:pedido_id>', methods=['PUT'])
def actualizar_pedido(pedido_id):
    """Actualiza un pedido existente"""
    try:
        data = request.json
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("BEGIN TRANSACTION")
        
        sql_update = """
            UPDATE pedidos
            SET dia = ?, nombre = ?, precio_pedido = ?, precio_envio = ?,
                direccion = ?, horario = ?, pago = ?
            WHERE id = ?
        """
        cursor.execute(sql_update, (
            data['dia'],
            data['nombre'],
            data['precio_pedido'],
            data.get('precio_envio', 0),
            data.get('direccion', ''),
            data.get('horario', ''),
            data.get('pago', 0),
            pedido_id
        ))
        
        cursor.execute("DELETE FROM pedido_items WHERE pedido_id = ?", (pedido_id,))
        
        sql_item = "INSERT INTO pedido_items (pedido_id, sabor, cantidad) VALUES (?, ?, ?)"
        for item in data['items']:
            cursor.execute(sql_item, (pedido_id, item['sabor'], item['cantidad']))
        
        conn.commit()
        conn.close()
        
        return jsonify({"success": True})
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/pedidos/<int:pedido_id>', methods=['DELETE'])
def eliminar_pedido(pedido_id):
    """Elimina un pedido"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
        conn.commit()
        
        eliminado = cursor.rowcount > 0
        conn.close()
        
        if eliminado:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Pedido no encontrado"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/pedidos/<int:pedido_id>/toggle-pago', methods=['POST'])
def toggle_pago(pedido_id):
    """Cambia el estado de pago de un pedido"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT pago FROM pedidos WHERE id = ?", (pedido_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return jsonify({"success": False, "error": "Pedido no encontrado"}), 404
        
        nuevo_estado = 1 if result['pago'] == 0 else 0
        cursor.execute("UPDATE pedidos SET pago = ? WHERE id = ?", (nuevo_estado, pedido_id))
        conn.commit()
        conn.close()
        
        return jsonify({"success": True, "nuevo_estado": nuevo_estado})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    """Obtiene estadísticas generales"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM pedidos")
        pedidos = cursor.fetchall()
        
        # Resumen de producción
        produccion = defaultdict(int)
        produccion_por_dia = defaultdict(lambda: defaultdict(int))
        total_recaudado = 0
        pedidos_pagados = 0
        pedidos_pendientes = 0
        
        for pedido_row in pedidos:
            pedido = dict(pedido_row)
            total_recaudado += pedido['precio_pedido'] + pedido.get('precio_envio', 0)
            
            if pedido.get('pago', 0) == 1:
                pedidos_pagados += 1
            else:
                pedidos_pendientes += 1
            
            cursor.execute("SELECT sabor, cantidad FROM pedido_items WHERE pedido_id = ?", 
                         (pedido['id'],))
            items = cursor.fetchall()
            
            dia = pedido['dia']
            for item in items:
                sabor = item['sabor']
                cantidad = item['cantidad']
                produccion[sabor] += cantidad
                produccion_por_dia[dia][sabor] += cantidad
        
        conn.close()
        
        # Convertir defaultdict a dict normal para JSON
        produccion_por_dia_dict = {dia: dict(sabores) for dia, sabores in produccion_por_dia.items()}
        
        return jsonify({
            "success": True,
            "estadisticas": {
                "produccion_total": dict(produccion),
                "produccion_por_dia": produccion_por_dia_dict,
                "total_recaudado": round(total_recaudado, 2),
                "total_pedidos": len(pedidos),
                "pedidos_pagados": pedidos_pagados,
                "pedidos_pendientes": pedidos_pendientes,
                "total_cookies": sum(produccion.values())
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/sabores', methods=['GET'])
def get_sabores():
    """Obtiene la lista de sabores válidos"""
    return jsonify({"success": True, "sabores": SABORES_VALIDOS})

if __name__ == '__main__':
    init_db()
    import webbrowser
    from threading import Timer
    
    def open_browser():
        webbrowser.open('http://127.0.0.1:5000')
    
    Timer(1, open_browser).start()
    app.run(debug=True, port=5000, use_reloader=False)