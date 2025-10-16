#!/usr/bin/env python3
"""
🔧 DIAGNÓSTICO DE GENERACIÓN QR
Prueba la conexión y generación de QRs paso a paso
"""

import requests
import json
import time

def test_server_connection():
    """Prueba la conexión con el servidor"""
    servers = [
        "http://192.168.5.53:5000",
        "http://localhost:5000",
        "http://127.0.0.1:5000"
    ]
    
    print("🔍 PROBANDO CONEXIÓN CON SERVIDORES:")
    print("=" * 50)
    
    for server in servers:
        try:
            response = requests.get(f"{server}/", timeout=3)
            print(f"✅ {server} - CONECTADO (Código: {response.status_code})")
            return server
        except requests.exceptions.ConnectRefused:
            print(f"❌ {server} - CONEXIÓN RECHAZADA")
        except requests.exceptions.Timeout:
            print(f"⏰ {server} - TIMEOUT")
        except Exception as e:
            print(f"❌ {server} - ERROR: {str(e)}")
    
    print("\n❌ NINGÚN SERVIDOR DISPONIBLE")
    return None

def test_stats_endpoint(server_url):
    """Prueba el endpoint de estadísticas"""
    print(f"\n📊 PROBANDO ENDPOINT /stats en {server_url}:")
    print("=" * 50)
    
    try:
        response = requests.get(f"{server_url}/stats", timeout=5)
        print(f"✅ Código de respuesta: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Datos recibidos: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Error en respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en /stats: {str(e)}")

def test_qr_generation(server_url):
    """Prueba la generación de un QR"""
    print(f"\n🎯 PROBANDO GENERACIÓN QR en {server_url}:")
    print("=" * 50)
    
    # Datos de prueba
    test_data = {
        "tipo_qr": "CODELPA",
        "marca_envase": "SHERWIN",
        "origen": "MP",
        "peso_envase_kg": 1.5,
        "lote_produccion": f"LOTE_TEST_{int(time.time())}"
    }
    
    print(f"📤 Enviando datos: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(f"{server_url}/generate_qr", 
                               json=test_data, 
                               timeout=10)
        
        print(f"✅ Código de respuesta: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"🎉 QR GENERADO EXITOSAMENTE:")
            print(f"   🆔 ID: {result.get('qr_id')}")
            print(f"   🏷️ Marca: {result.get('marca_envase')}")
            print(f"   📍 Origen: {result.get('origen')}")
            print(f"   ⚖️ Peso: {result.get('peso_envase_kg')}kg")
            return True
        else:
            print(f"❌ Error en generación:")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', 'Desconocido')}")
            except:
                print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en /generate_qr: {str(e)}")
        return False

def test_multiple_qrs(server_url, cantidad=3):
    """Prueba generar múltiples QRs"""
    print(f"\n🔄 PROBANDO GENERACIÓN MÚLTIPLE ({cantidad} QRs):")
    print("=" * 50)
    
    exitos = 0
    errores = 0
    
    for i in range(cantidad):
        test_data = {
            "tipo_qr": "CODELPA" if i % 2 == 0 else "TERCERO",
            "marca_envase": f"MARCA_TEST_{i+1}",
            "origen": "MP",
            "peso_envase_kg": 1.5,
            "lote_produccion": f"LOTE_MULTI_{int(time.time())}_{i}"
        }
        
        try:
            response = requests.post(f"{server_url}/generate_qr", 
                                   json=test_data, 
                                   timeout=10)
            
            if response.status_code in [200, 201]:
                result = response.json()
                qr_id = result.get('qr_id', 'ERROR')
                print(f"✅ QR {i+1}: {qr_id}")
                exitos += 1
            else:
                print(f"❌ QR {i+1}: Error {response.status_code}")
                errores += 1
                
        except Exception as e:
            print(f"❌ QR {i+1}: {str(e)}")
            errores += 1
    
    print(f"\n📊 RESULTADOS: {exitos} éxitos, {errores} errores")
    return exitos, errores

def main():
    """Ejecuta todas las pruebas"""
    print("🔧 SISTEMA REP - DIAGNÓSTICO DE QR")
    print("🕐", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    
    # 1. Probar conexión
    server_url = test_server_connection()
    if not server_url:
        print("\n❌ NO SE PUEDE CONTINUAR SIN SERVIDOR")
        return
    
    # 2. Probar endpoint stats
    test_stats_endpoint(server_url)
    
    # 3. Probar generación individual
    if test_qr_generation(server_url):
        # 4. Probar generación múltiple
        test_multiple_qrs(server_url, 3)
    
    print("\n" + "=" * 60)
    print("🔚 DIAGNÓSTICO COMPLETADO")
    print("\n💡 Si hay errores:")
    print("   1. Verificar que el servidor esté ejecutándose")
    print("   2. Ejecutar: INICIAR_SERVIDOR_REP.bat")
    print("   3. Verificar firewall y puerto 5000")
    print("   4. Probar en la aplicación desktop nuevamente")

if __name__ == "__main__":
    main()