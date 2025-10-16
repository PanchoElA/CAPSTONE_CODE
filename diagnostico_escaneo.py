#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO QR ESCANEADOS
Verifica la conexión entre QRs generados y el sistema de escaneo
"""

import requests
import json
import sqlite3
import os
from datetime import datetime

def check_server_connection():
    """Verifica conexión con servidor"""
    servers = [
        "http://192.168.5.53:5000",
        "http://localhost:5000",
        "http://127.0.0.1:5000"
    ]
    
    print("🔍 VERIFICANDO CONEXIÓN SERVIDOR:")
    print("=" * 50)
    
    for server in servers:
        try:
            response = requests.get(f"{server}/", timeout=3)
            print(f"✅ {server} - CONECTADO")
            return server
        except Exception as e:
            print(f"❌ {server} - {str(e)}")
    
    return None

def check_database_qrs(server_url):
    """Verifica QRs en la base de datos"""
    print(f"\n📊 VERIFICANDO QRs EN BASE DE DATOS:")
    print("=" * 50)
    
    try:
        # Verificar que existe la base de datos
        db_path = "android_app/server/data.db"  # Nombre correcto de la base de datos
        if not os.path.exists(db_path):
            print(f"❌ Base de datos no encontrada: {db_path}")
            return []
        
        # Conectar y consultar QRs generados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT qr_id, marca_envase, origen, tipo_qr, fecha_generacion
            FROM qr_generated 
            ORDER BY fecha_generacion DESC 
            LIMIT 10
        """)
        
        qrs = cursor.fetchall()
        conn.close()
        
        if qrs:
            print(f"✅ {len(qrs)} QRs encontrados en la base de datos:")
            for i, qr in enumerate(qrs, 1):
                qr_id, marca, origen, tipo, fecha = qr
                fecha_str = datetime.fromtimestamp(fecha/1000).strftime("%Y-%m-%d %H:%M:%S")
                print(f"   {i}. {qr_id} - {marca} ({origen}) [{tipo}] - {fecha_str}")
            return qrs
        else:
            print("❌ No se encontraron QRs en la base de datos")
            return []
            
    except Exception as e:
        print(f"❌ Error accediendo a la base de datos: {str(e)}")
        return []

def test_qr_scan_simulation(server_url, qr_id):
    """Simula el escaneo de un QR"""
    print(f"\n🔄 SIMULANDO ESCANEO QR: {qr_id}")
    print("=" * 50)
    
    try:
        # Datos del escaneo simulado
        scan_data = {
            "qr_id": qr_id,
            "estado_retorno": "BUENO",
            "tienda_retorno": "MUNDO_PINTURA_CENTRAL",
            "cliente_profile": "TEST_USER",
            "evidencia": "SIMULACION_DIAGNOSTICO"
        }
        
        print(f"📤 Enviando datos de escaneo:")
        print(f"   🆔 QR: {qr_id}")
        print(f"   👤 Cliente: TEST_USER")
        print(f"   📍 Tienda: MUNDO_PINTURA_CENTRAL")
        print(f"   ✅ Estado: BUENO")
        
        response = requests.post(f"{server_url}/retorno_rep", 
                               json=scan_data, 
                               timeout=10)
        
        print(f"\n📊 RESULTADO DEL ESCANEO:")
        print(f"   Código de respuesta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Escaneo exitoso!")
            print(f"   🎁 Puntos otorgados: {result.get('puntos_otorgados', 0)}")
            print(f"   📍 Destino: {result.get('destino', 'N/A')}")
            print(f"   🆔 Retorno ID: {result.get('retorno_id', 'N/A')}")
            return True
        else:
            try:
                error_data = response.json()
                print(f"   ❌ Error: {error_data.get('error', 'Desconocido')}")
            except:
                print(f"   ❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en simulación: {str(e)}")
        return False

def check_client_points(server_url, cliente):
    """Verifica puntos del cliente"""
    print(f"\n💰 VERIFICANDO PUNTOS CLIENTE: {cliente}")
    print("=" * 50)
    
    try:
        response = requests.get(f"{server_url}/cliente_retornos/{cliente}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Cliente encontrado!")
            print(f"   🎁 Puntos totales: {data.get('puntos_total', 0)}")
            print(f"   📊 Retornos realizados: {data.get('retornos_total', 0)}")
            print(f"   ⚖️ Peso total reciclado: {data.get('peso_total_kg', 0)}kg")
            return data
        else:
            print(f"   ❌ Cliente no encontrado o sin retornos")
            return None
            
    except Exception as e:
        print(f"   ❌ Error consultando cliente: {str(e)}")
        return None

def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO ESCANEO QR - SISTEMA REP")
    print("🕐", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    
    # 1. Verificar conexión servidor
    server_url = check_server_connection()
    if not server_url:
        print("\n❌ NO SE PUEDE CONTINUAR SIN SERVIDOR")
        return
    
    # 2. Verificar QRs en base de datos
    qrs = check_database_qrs(server_url)
    if not qrs:
        print("\n❌ NO HAY QRs PARA PROBAR")
        return
    
    # 3. Probar escaneo con el primer QR
    qr_to_test = qrs[0][0]  # Primer QR ID
    scan_success = test_qr_scan_simulation(server_url, qr_to_test)
    
    # 4. Verificar puntos del cliente de prueba
    if scan_success:
        check_client_points(server_url, "TEST_USER")
    
    print("\n" + "=" * 60)
    print("🔚 DIAGNÓSTICO COMPLETADO")
    
    if scan_success:
        print("\n✅ SISTEMA FUNCIONANDO CORRECTAMENTE")
        print("💡 Los QRs generados pueden ser escaneados y otorgan puntos")
        print("🔄 Verifica que la Scanner App esté usando el mismo servidor")
    else:
        print("\n❌ PROBLEMA DETECTADO")
        print("💡 Verifica:")
        print("   1. Servidor iniciado correctamente")
        print("   2. Base de datos tiene QRs válidos") 
        print("   3. Endpoint /retorno_rep funciona")
        print("   4. Scanner App apunta al servidor correcto")

if __name__ == "__main__":
    main()