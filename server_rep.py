#!/usr/bin/env python3
"""
SERVIDOR REP OPTIMIZADO
Versión limpia para Scanner App y Desktop App
"""

from flask import Flask, request, jsonify, render_template_string
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Configuración
DATABASE = 'rep_database.db'

def init_database():
    """Inicializa la base de datos"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qr_scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            qr_code TEXT NOT NULL,
            user_name TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Página principal con estadísticas"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Obtener estadísticas básicas
    cursor.execute('SELECT COUNT(*) FROM qr_scans')
    total_scans = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT user_name) FROM qr_scans')
    total_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT qr_code, user_name, timestamp FROM qr_scans ORDER BY timestamp DESC LIMIT 10')
    recent_scans = cursor.fetchall()
    
    conn.close()
    
    # Template HTML simple
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sistema REP</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            .header { color: #2E7D32; text-align: center; margin-bottom: 30px; }
            .stats { display: flex; justify-content: space-around; margin: 20px 0; }
            .stat-box { background: #E8F5E8; padding: 20px; border-radius: 8px; text-align: center; }
            .stat-number { font-size: 2em; font-weight: bold; color: #2E7D32; }
            .recent-scans { margin-top: 30px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #2E7D32; color: white; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌱 Sistema REP</h1>
                <p>Servidor funcionando correctamente</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{{ total_scans }}</div>
                    <div>QRs Escaneados</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ total_users }}</div>
                    <div>Usuarios Activos</div>
                </div>
            </div>
            
            <div class="recent-scans">
                <h3>📱 Escaneos Recientes</h3>
                <table>
                    <tr>
                        <th>Código QR</th>
                        <th>Usuario</th>
                        <th>Fecha</th>
                    </tr>
                    {% for scan in recent_scans %}
                    <tr>
                        <td>{{ scan[0] }}</td>
                        <td>{{ scan[1] }}</td>
                        <td>{{ scan[2] }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(html, 
                                total_scans=total_scans, 
                                total_users=total_users, 
                                recent_scans=recent_scans)

@app.route('/scan', methods=['POST'])
def process_scan():
    """Endpoint principal para recibir datos de QR escaneados"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        qr_code = data.get('qr_code')
        user_name = data.get('user_name')
        
        if not qr_code or not user_name:
            return jsonify({"error": "Missing qr_code or user_name"}), 400
        
        # Guardar en base de datos
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO qr_scans (qr_code, user_name, ip_address)
            VALUES (?, ?, ?)
        ''', (qr_code, user_name, request.remote_addr))
        
        scan_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ QR escaneado - ID: {scan_id}, Usuario: {user_name}, QR: {qr_code}")
        
        return jsonify({
            "status": "success",
            "message": "QR code procesado exitosamente",
            "scan_id": scan_id,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/stats')
def stats():
    """API de estadísticas"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM qr_scans')
    total_scans = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT user_name) FROM qr_scans')
    total_users = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        "total_scans": total_scans,
        "total_users": total_users,
        "server_status": "running"
    })

@app.route('/users')
def users():
    """Lista de usuarios con sus escaneos"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_name, COUNT(*) as scan_count, MAX(timestamp) as last_scan
        FROM qr_scans 
        GROUP BY user_name 
        ORDER BY scan_count DESC
    ''')
    
    users = []
    for row in cursor.fetchall():
        users.append({
            "name": row[0],
            "scan_count": row[1],
            "last_scan": row[2]
        })
    
    conn.close()
    return jsonify(users)

@app.route('/user/<user_name>')
def user_detail(user_name):
    """Detalles de un usuario específico"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT qr_code, timestamp FROM qr_scans 
        WHERE user_name = ? 
        ORDER BY timestamp DESC
    ''', (user_name,))
    
    scans = []
    for row in cursor.fetchall():
        scans.append({
            "qr_code": row[0],
            "timestamp": row[1]
        })
    
    conn.close()
    
    return jsonify({
        "user_name": user_name,
        "total_scans": len(scans),
        "scans": scans
    })

if __name__ == '__main__':
    print("🚀 Iniciando Servidor REP...")
    init_database()
    print("✅ Base de datos inicializada")
    print("🌐 Servidor disponible en: http://192.168.5.53:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)