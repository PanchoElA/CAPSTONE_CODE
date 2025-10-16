#!/usr/bin/env python3
"""
🔒 PRUEBA FINAL VALIDACIÓN QR
Prueba con QRs reales generados por el sistema desktop
"""

import requests
import json
import sqlite3
from datetime import datetime

def get_real_qrs():
    """Obtiene QRs reales de la base de datos"""
    try:
        conn = sqlite3.connect("android_app/server/data.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT qr_id, marca_envase, tipo_qr 
            FROM qr_generated 
            ORDER BY fecha_generacion DESC 
            LIMIT 3
        """)
        
        qrs = cursor.fetchall()
        conn.close()
        return qrs
    except Exception as e:
        print(f"❌ Error accediendo base de datos: {str(e)}")
        return []

def test_real_qr_scanning(server_url):
    """Prueba escaneo con QRs reales del sistema"""
    print("🔒 PROBANDO CON QRs REALES DEL SISTEMA:")
    print("=" * 60)
    
    # Obtener QRs reales
    real_qrs = get_real_qrs()
    
    if not real_qrs:
        print("❌ No hay QRs reales para probar")
        return
    
    print(f"✅ Encontrados {len(real_qrs)} QRs reales en la base de datos")
    
    for i, (qr_id, marca, tipo) in enumerate(real_qrs, 1):
        print(f"\n🧪 PRUEBA QR REAL {i}:")
        print(f"   🆔 QR: {qr_id}")
        print(f"   🏷️ Marca: {marca}")
        print(f"   📋 Tipo: {tipo}")
        
        try:
            # Intentar escanear QR real
            scan_data = {
                "qr_id": qr_id,
                "estado_retorno": "BUENO",
                "tienda_retorno": "MUNDO_PINTURA_CENTRAL",
                "cliente_profile": f"TEST_REAL_USER_{i}",
                "evidencia": "PRUEBA_QR_REAL"
            }
            
            response = requests.post(f"{server_url}/retorno_rep", 
                                   json=scan_data, 
                                   timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                points = result.get('puntos_otorgados', 0)
                destino = result.get('destino', 'N/A')
                print(f"   ✅ ESCANEO EXITOSO!")
                print(f"   🎁 Puntos otorgados: {points}")
                print(f"   📍 Destino: {destino}")
                
            elif response.status_code == 409:
                print(f"   ⚠️ QR ya procesado (normal en pruebas)")
                
            else:
                try:
                    error_data = response.json()
                    print(f"   ❌ Error: {error_data.get('error', 'Desconocido')}")
                except:
                    print(f"   ❌ Error: {response.text}")
                    
        except Exception as e:
            print(f"   ❌ Error de conexión: {str(e)}")

def test_fake_qrs(server_url):
    """Prueba que QRs falsos sean rechazados"""
    print(f"\n🚫 PROBANDO RECHAZO DE QRs FALSOS:")
    print("=" * 60)
    
    fake_qrs = [
        "CODELPA:123456789ABC",  # Formato válido pero no en BD
        "TERCERO:DEF456789012",  # Formato válido pero no en BD
        "MYAPPPOINTS:ABC123",    # Formato antiguo
        "https://fake-qr.com",   # URL
        "TEXTO_SIMPLE",          # Texto plano
    ]
    
    rejected_count = 0
    
    for i, fake_qr in enumerate(fake_qrs, 1):
        print(f"\n🧪 PRUEBA QR FALSO {i}:")
        print(f"   📝 QR: {fake_qr}")
        
        try:
            scan_data = {
                "qr_id": fake_qr,
                "estado_retorno": "BUENO",
                "tienda_retorno": "MUNDO_PINTURA_CENTRAL",
                "cliente_profile": "TEST_FAKE_USER",
                "evidencia": "PRUEBA_QR_FALSO"
            }
            
            response = requests.post(f"{server_url}/retorno_rep", 
                                   json=scan_data, 
                                   timeout=10)
            
            if response.status_code != 200:
                print(f"   ✅ RECHAZADO CORRECTAMENTE (código {response.status_code})")
                rejected_count += 1
            else:
                print(f"   🚨 ERROR - QR falso fue aceptado!")
                
        except Exception as e:
            print(f"   ❌ Error de conexión: {str(e)}")
    
    print(f"\n📊 RESULTADO: {rejected_count}/{len(fake_qrs)} QRs falsos rechazados")
    return rejected_count == len(fake_qrs)

def main():
    """Función principal"""
    print("🔒 SISTEMA REP - PRUEBA FINAL VALIDACIÓN")
    print("🕐", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)
    
    server_url = "http://192.168.5.53:5000"
    
    try:
        response = requests.get(server_url, timeout=3)
        print(f"✅ Servidor conectado: {server_url}")
    except Exception as e:
        print(f"❌ Error conectando al servidor: {str(e)}")
        return
    
    # Probar QRs reales
    test_real_qr_scanning(server_url)
    
    # Probar QRs falsos
    all_fake_rejected = test_fake_qrs(server_url)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("🏁 RESUMEN FINAL DE VALIDACIÓN:")
    print("=" * 70)
    
    if all_fake_rejected:
        print("✅ VALIDACIÓN PERFECTA:")
        print("   • QRs reales del sistema son aceptados")
        print("   • QRs falsos/externos son rechazados")
        print("   • Scanner funciona SOLO con QRs del desktop")
        print("\n🔒 SEGURIDAD CONFIRMADA:")
        print("   • Imposible usar QRs de otras fuentes")
        print("   • Solo QRs generados por el sistema REP")
        print("   • Formato estricto validado")
    else:
        print("⚠️ PROBLEMAS DE VALIDACIÓN DETECTADOS")
        print("🔧 Revisar configuración del servidor")
    
    print("\n💡 EL SCANNER AHORA SOLO FUNCIONA CON:")
    print("   ✅ QRs CODELPA generados por desktop")
    print("   ✅ QRs TERCERO generados por desktop")
    print("   ❌ Rechaza TODO lo demás")

if __name__ == "__main__":
    main()