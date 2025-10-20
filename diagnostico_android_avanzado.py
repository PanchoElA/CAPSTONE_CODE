#!/usr/bin/env python3
"""
Diagnóstico específico para Scanner App con permisos corregidos
Determinar por qué persiste rep_network_error después de recompilación
"""

import requests
import json
from datetime import datetime

def test_from_android_perspective():
    """Simular exactamente lo que hace el Scanner App"""
    server_url = "http://192.168.5.53:5000"
    
    print("🔍 DIAGNÓSTICO SCANNER APP - PERSPECTIVA ANDROID")
    print("=" * 60)
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Test básico de conectividad (lo que Chrome hace exitosamente)
    print("\n1️⃣ TEST CONECTIVIDAD BÁSICA (Chrome funciona):")
    try:
        response = requests.get(f"{server_url}/", timeout=5)
        print(f"   ✅ GET / → Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error básico: {e}")
        return False
    
    # 2. Test endpoint específico de sincronización
    print("\n2️⃣ TEST ENDPOINT SINCRONIZACIÓN:")
    try:
        response = requests.get(f"{server_url}/cliente_retornos/default", timeout=10)
        print(f"   📊 GET /cliente_retornos/default → Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            points = data.get('profile', {}).get('points', 0)
            print(f"   ⭐ Puntos en servidor: {points}")
        else:
            print(f"   ⚠️ Response: {response.text[:100]}")
    except Exception as e:
        print(f"   ❌ Error sincronización: {e}")
    
    # 3. Test POST retorno_rep (lo que falla en Scanner App)
    print("\n3️⃣ TEST RETORNO_REP (LO QUE HACE SCANNER APP):")
    
    # Generar QR nuevo
    qr_payload = {
        "tipo_qr": "CODELPA",
        "marca_envase": "Codelpa", 
        "origen": "ANDROID_DIAGNOSTIC",
        "peso_envase_kg": 1.0
    }
    
    try:
        qr_response = requests.post(f"{server_url}/generate_qr", json=qr_payload, timeout=10)
        if qr_response.status_code in [200, 201]:
            test_qr = qr_response.json()["qr_id"]
            print(f"   📱 QR generado: {test_qr}")
            
            # Simular EXACTAMENTE el payload del Scanner App
            scan_payload = {
                "qr_id": test_qr,
                "estado_retorno": "BUENO", 
                "tienda_retorno": "MUNDO_PINTURA_CENTRAL",
                "cliente_profile": "default",
                "evidencia": "INSPECCION_VISUAL"
            }
            
            # Test con diferentes configuraciones de headers
            headers_tests = [
                {"Content-Type": "application/json"},
                {"Content-Type": "application/json", "User-Agent": "Android-App"},
                {"Content-Type": "application/json; charset=utf-8"},
                {}  # Sin headers
            ]
            
            for i, headers in enumerate(headers_tests, 1):
                try:
                    print(f"\n   🧪 Test {i} - Headers: {headers}")
                    scan_response = requests.post(
                        f"{server_url}/retorno_rep",
                        json=scan_payload,
                        headers=headers,
                        timeout=30
                    )
                    
                    print(f"      📤 Status: {scan_response.status_code}")
                    
                    if scan_response.status_code == 200:
                        result = scan_response.json()
                        puntos = result.get('puntos_otorgados', 0)
                        print(f"      ✅ ÉXITO: {puntos} puntos otorgados")
                        print(f"      🎯 Scanner App DEBERÍA funcionar con estos headers")
                        return True
                    elif scan_response.status_code == 409:
                        print(f"      ⚠️ QR ya usado (normal)")
                        break
                    else:
                        print(f"      ❌ Error: {scan_response.text[:100]}")
                        
                except Exception as e:
                    print(f"      ❌ Error request: {e}")
                    
        else:
            print(f"   ❌ No se pudo generar QR test: {qr_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error general: {e}")
    
    return False

def analyze_possible_causes():
    """Analizar causas posibles del problema persistente"""
    print("\n4️⃣ ANÁLISIS CAUSAS POSIBLES:")
    print("=" * 40)
    
    causes = [
        ("🔧 APK no recompilado correctamente", [
            "• Caché de Android no limpiado",
            "• APK anterior aún instalado",
            "• Recompilación parcial sin permisos"
        ]),
        ("🌐 Problema de configuración de red", [
            "• URL hardcodeada incorrecta en app",
            "• Timeout muy corto en OkHttp",
            "• User-Agent bloqueado por servidor"
        ]),
        ("📱 Problema específico de Android", [
            "• Firewall de Android bloqueando app",
            "• Configuración de WiFi con restricciones",
            "• Permisos no aplicados correctamente"
        ]),
        ("🔍 Problema de código", [
            "• Error en PointsManager.kt no detectado",
            "• Exception silenciosa en try/catch",
            "• URL SERVER_URL incorrecta"
        ])
    ]
    
    for cause, details in causes:
        print(f"\n{cause}:")
        for detail in details:
            print(f"   {detail}")

def provide_immediate_solutions():
    """Proporcionar soluciones inmediatas"""
    print("\n5️⃣ SOLUCIONES INMEDIATAS:")
    print("=" * 40)
    
    print("\n🎯 OPCIÓN A: Verificación de URL en Scanner App")
    print("   1. Abrir Scanner App")
    print("   2. Ir a Configuración/Settings")
    print("   3. Verificar URL: http://192.168.5.53:5000")
    print("   4. Asegurar que NO tiene barra final (/)")
    
    print("\n🎯 OPCIÓN B: Limpiar datos de la App")
    print("   1. Android: Configuración → Apps → QRPoints")
    print("   2. Almacenamiento → Borrar datos")
    print("   3. Reinstalar APK recompilado")
    print("   4. Configurar URL desde cero")
    
    print("\n🎯 OPCIÓN C: Verificar PointsManager.kt")
    print("   1. Confirmar SERVER_URL = 'http://192.168.5.53:5000'")
    print("   2. Sin espacios, sin barra final")
    print("   3. Timeout mínimo 30 segundos")
    
    print("\n🎯 OPCIÓN D: Test desde dispositivo Android")
    print("   1. Abrir Chrome en Android")
    print("   2. Ir a: http://192.168.5.53:5000")
    print("   3. Si funciona → problema en Scanner App")
    print("   4. Si no funciona → problema de red Android")

def main():
    """Función principal"""
    print("📱 DIAGNÓSTICO: Scanner App con permisos corregidos")
    print("   Problema: rep_network_error persiste después de recompilación")
    print()
    
    server_working = test_from_android_perspective()
    
    analyze_possible_causes()
    provide_immediate_solutions()
    
    print(f"\n" + "=" * 60)
    print("📋 CONCLUSIÓN:")
    if server_working:
        print("✅ Servidor funciona → Problema en Scanner App")
        print("🔧 Revisar URL, configuración y logs de Android")
    else:
        print("⚠️ Hay problemas de conectividad específicos")
        print("🔧 Verificar configuración de red y permisos")
    print("=" * 60)

if __name__ == "__main__":
    main()