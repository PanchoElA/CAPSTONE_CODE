#!/usr/bin/env python3
"""
🔧 DIAGNÓSTICO CONECTIVIDAD REP
Diagnostica problemas de red entre Scanner App y servidor
"""

import requests
import socket
import subprocess
import time
import json
from datetime import datetime

def check_network_basics():
    """Verifica conectividad básica de red"""
    print("🌐 VERIFICANDO CONECTIVIDAD BÁSICA:")
    print("=" * 50)
    
    # Verificar conectividad local
    try:
        # Verificar que el servidor local responde
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ Servidor local (localhost:5000) - ACCESIBLE")
    except Exception as e:
        print(f"❌ Servidor local (localhost:5000) - ERROR: {str(e)}")
    
    # Verificar IP específica
    try:
        response = requests.get("http://192.168.5.53:5000", timeout=5)
        print("✅ Servidor IP (192.168.5.53:5000) - ACCESIBLE")
    except Exception as e:
        print(f"❌ Servidor IP (192.168.5.53:5000) - ERROR: {str(e)}")

def check_port_connectivity():
    """Verifica que el puerto 5000 esté abierto"""
    print(f"\n🔌 VERIFICANDO PUERTO 5000:")
    print("=" * 50)
    
    hosts = ["localhost", "192.168.5.53"]
    
    for host in hosts:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((host, 5000))
            sock.close()
            
            if result == 0:
                print(f"✅ Puerto 5000 abierto en {host}")
            else:
                print(f"❌ Puerto 5000 cerrado en {host}")
        except Exception as e:
            print(f"❌ Error verificando {host}:5000 - {str(e)}")

def check_firewall():
    """Verifica configuración del firewall"""
    print(f"\n🛡️ VERIFICANDO FIREWALL:")
    print("=" * 50)
    
    try:
        # Verificar reglas de firewall para puerto 5000
        result = subprocess.run(
            ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"],
            capture_output=True, text=True, timeout=10
        )
        
        if "5000" in result.stdout:
            print("✅ Reglas de firewall encontradas para puerto 5000")
        else:
            print("⚠️ No se encontraron reglas específicas para puerto 5000")
            
    except Exception as e:
        print(f"❌ Error verificando firewall: {str(e)}")
    
    # Sugerir comando para abrir puerto
    print("\n💡 Para abrir puerto 5000 en firewall:")
    print('netsh advfirewall firewall add rule name="REP Server" dir=in action=allow protocol=TCP localport=5000')

def check_server_endpoints(server_url):
    """Verifica que los endpoints del servidor funcionen"""
    print(f"\n📡 VERIFICANDO ENDPOINTS DEL SERVIDOR:")
    print("=" * 50)
    
    endpoints = [
        ("/", "GET", None, "Página principal"),
        ("/stats", "GET", None, "Estadísticas"),
        ("/retorno_rep", "POST", {
            "qr_id": "TEST:123456789ABC",
            "estado_retorno": "BUENO",
            "cliente_profile": "TEST_CONNECTIVITY"
        }, "Endpoint REP")
    ]
    
    for endpoint, method, data, description in endpoints:
        try:
            url = f"{server_url}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, json=data, timeout=10)
            
            print(f"✅ {description} ({endpoint}) - Código: {response.status_code}")
            
        except requests.exceptions.ConnectRefused:
            print(f"❌ {description} - CONEXIÓN RECHAZADA")
        except requests.exceptions.Timeout:
            print(f"⏰ {description} - TIMEOUT")
        except Exception as e:
            print(f"❌ {description} - ERROR: {str(e)}")

def test_android_simulation(server_url):
    """Simula una petición como la haría Android"""
    print(f"\n📱 SIMULANDO PETICIÓN ANDROID:")
    print("=" * 50)
    
    try:
        # Simular exactamente lo que envía Android
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'okhttp/4.x (Android simulation)'
        }
        
        payload = {
            "qr_id": "CODELPA:6C231EF1C127",  # QR real de la BD
            "estado_retorno": "BUENO",
            "tienda_retorno": "MUNDO_PINTURA_CENTRAL",
            "cliente_profile": "ANDROID_TEST",
            "evidencia": "SIMULACION_ANDROID"
        }
        
        print(f"📤 Enviando a: {server_url}/retorno_rep")
        print(f"📝 Headers: {headers}")
        print(f"📦 Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{server_url}/retorno_rep",
            json=payload,
            headers=headers,
            timeout=15
        )
        
        print(f"\n📊 RESPUESTA:")
        print(f"   Código: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.text:
            try:
                result = response.json()
                print(f"   JSON: {json.dumps(result, indent=2)}")
            except:
                print(f"   Texto: {response.text}")
        
        if response.status_code == 200:
            print("✅ SIMULACIÓN ANDROID EXITOSA")
        else:
            print("❌ SIMULACIÓN ANDROID FALLÓ")
            
    except Exception as e:
        print(f"❌ Error en simulación Android: {str(e)}")

def check_wifi_connectivity():
    """Verifica configuración de WiFi"""
    print(f"\n📶 VERIFICANDO CONECTIVIDAD WIFI:")
    print("=" * 50)
    
    try:
        # Obtener configuración de red
        result = subprocess.run(
            ["ipconfig"], capture_output=True, text=True, timeout=10
        )
        
        if "192.168.5." in result.stdout:
            print("✅ PC está en red 192.168.5.x")
        else:
            print("⚠️ PC podría no estar en la misma red que Android")
            
        # Mostrar IPs activas
        lines = result.stdout.split('\n')
        for line in lines:
            if "IPv4" in line:
                ip = line.split(':')[-1].strip()
                print(f"   📍 IP del PC: {ip}")
                
    except Exception as e:
        print(f"❌ Error verificando WiFi: {str(e)}")

def main():
    """Función principal"""
    print("🔧 DIAGNÓSTICO CONECTIVIDAD REP - SISTEMA")
    print("🕐", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    
    # Verificar conectividad básica
    check_network_basics()
    
    # Verificar puerto
    check_port_connectivity()
    
    # Verificar firewall
    check_firewall()
    
    # Verificar WiFi
    check_wifi_connectivity()
    
    # Determinar servidor a usar
    server_url = None
    for url in ["http://192.168.5.53:5000", "http://localhost:5000"]:
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                server_url = url
                break
        except:
            continue
    
    if server_url:
        print(f"\n🎯 USANDO SERVIDOR: {server_url}")
        
        # Verificar endpoints
        check_server_endpoints(server_url)
        
        # Simular Android
        test_android_simulation(server_url)
    else:
        print("\n❌ NO SE ENCONTRÓ SERVIDOR FUNCIONANDO")
    
    # Resumen y recomendaciones
    print("\n" + "=" * 60)
    print("🏁 RESUMEN Y RECOMENDACIONES:")
    print("=" * 60)
    
    print("💡 PARA SOLUCIONAR 'rep_network_error':")
    print("   1. Verificar que el servidor REP esté ejecutándose")
    print("   2. Confirmar que Android y PC están en misma WiFi")
    print("   3. Abrir puerto 5000 en firewall si está bloqueado")
    print("   4. Verificar IP 192.168.5.53 sea accesible desde Android")
    print("   5. Actualizar configuración en Scanner App si es necesario")
    
    print("\n🔧 COMANDOS ÚTILES:")
    print("   • Iniciar servidor: .\\INICIAR_SISTEMA_COMPLETO.bat")
    print("   • Verificar firewall: netsh advfirewall firewall show rule name=all")
    print("   • Ver configuración red: ipconfig")

if __name__ == "__main__":
    main()