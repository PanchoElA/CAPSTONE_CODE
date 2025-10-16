#!/usr/bin/env python3
"""
🔒 VALIDACIÓN ESTRICTA QR - SISTEMA REP
Prueba que el scanner SOLO acepta QRs del sistema desktop
"""

import requests
import json
from datetime import datetime

def test_qr_validation(server_url):
    """Prueba diferentes tipos de QR para validar filtrado"""
    print("🔒 PROBANDO VALIDACIÓN ESTRICTA DE QRs:")
    print("=" * 60)
    
    # QRs de prueba - algunos válidos, otros que deben ser rechazados
    test_qrs = [
        {
            "qr": "CODELPA:ABC123456789",
            "description": "QR CODELPA válido (12 caracteres hex)",
            "should_accept": True
        },
        {
            "qr": "TERCERO:DEF123456789", 
            "description": "QR TERCERO válido (12 caracteres hex)",
            "should_accept": True
        },
        {
            "qr": "CODELPA:ABC12345",
            "description": "QR CODELPA inválido (muy corto)",
            "should_accept": False
        },
        {
            "qr": "CODELPA:ABC123456789EXTRA",
            "description": "QR CODELPA inválido (muy largo)",
            "should_accept": False
        },
        {
            "qr": "CODELPA:ABC123GHI456",
            "description": "QR CODELPA inválido (contiene letras no-hex)",
            "should_accept": False
        },
        {
            "qr": "MYAPPPOINTS:ABC123",
            "description": "QR formato antiguo (debe rechazar)",
            "should_accept": False
        },
        {
            "qr": "https://example.com/qr?id=123",
            "description": "QR URL (debe rechazar)",
            "should_accept": False
        },
        {
            "qr": "SIMPLE_TEXT_QR",
            "description": "QR texto simple (debe rechazar)",
            "should_accept": False
        },
        {
            "qr": "codelpa:abc123456789",
            "description": "QR CODELPA minúsculas (debe aceptar y normalizar)",
            "should_accept": True
        },
        {
            "qr": "OTRA_MARCA:123456789ABC",
            "description": "QR marca no reconocida (debe rechazar)",
            "should_accept": False
        }
    ]
    
    results = {"accepted": 0, "rejected": 0, "errors": 0}
    
    for i, test in enumerate(test_qrs, 1):
        qr_code = test["qr"]
        description = test["description"]
        should_accept = test["should_accept"]
        
        print(f"\n🧪 PRUEBA {i}/10:")
        print(f"   📝 QR: {qr_code}")
        print(f"   📋 Descripción: {description}")
        print(f"   🎯 Expectativa: {'✅ ACEPTAR' if should_accept else '❌ RECHAZAR'}")
        
        try:
            # Simular escaneo
            scan_data = {
                "qr_id": qr_code,
                "estado_retorno": "BUENO",
                "tienda_retorno": "MUNDO_PINTURA_CENTRAL",
                "cliente_profile": "TEST_VALIDATION_USER",
                "evidencia": "PRUEBA_VALIDACION"
            }
            
            response = requests.post(f"{server_url}/retorno_rep", 
                                   json=scan_data, 
                                   timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                points = result.get('puntos_otorgados', 0)
                if points > 0:
                    print(f"   ✅ RESULTADO: ACEPTADO ({points} puntos)")
                    if should_accept:
                        print(f"   🎉 CORRECTO - Se esperaba aceptación")
                        results["accepted"] += 1
                    else:
                        print(f"   🚨 ERROR - Se esperaba rechazo pero fue aceptado")
                        results["errors"] += 1
                else:
                    print(f"   ❌ RESULTADO: RECHAZADO (0 puntos)")
                    if not should_accept:
                        print(f"   🎉 CORRECTO - Se esperaba rechazo")
                        results["rejected"] += 1
                    else:
                        print(f"   🚨 ERROR - Se esperaba aceptación pero fue rechazado")
                        results["errors"] += 1
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', 'Error desconocido')
                except:
                    error_msg = response.text
                
                print(f"   ❌ RESULTADO: ERROR DEL SERVIDOR ({response.status_code})")
                print(f"   📝 Error: {error_msg}")
                
                if not should_accept:
                    print(f"   🎉 CORRECTO - QR inválido rechazado por servidor")
                    results["rejected"] += 1
                else:
                    print(f"   🚨 ERROR - QR válido rechazado incorrectamente")
                    results["errors"] += 1
                    
        except Exception as e:
            print(f"   ❌ RESULTADO: ERROR DE CONEXIÓN")
            print(f"   📝 Error: {str(e)}")
            results["errors"] += 1
    
    return results

def main():
    """Función principal"""
    print("🔒 SISTEMA REP - VALIDACIÓN ESTRICTA QR")
    print("🕐", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)
    
    # Verificar servidor
    server_url = "http://192.168.5.53:5000"
    try:
        response = requests.get(server_url, timeout=3)
        print(f"✅ Servidor conectado: {server_url}")
    except Exception as e:
        print(f"❌ Error conectando al servidor: {str(e)}")
        return
    
    # Ejecutar pruebas
    results = test_qr_validation(server_url)
    
    # Mostrar resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE VALIDACIÓN:")
    print("=" * 70)
    print(f"✅ QRs Aceptados Correctamente: {results['accepted']}")
    print(f"❌ QRs Rechazados Correctamente: {results['rejected']}")
    print(f"🚨 Errores de Validación: {results['errors']}")
    
    total_correct = results['accepted'] + results['rejected']
    total_tests = sum(results.values())
    
    if results['errors'] == 0:
        print(f"\n🎉 VALIDACIÓN PERFECTA: {total_correct}/{total_tests} pruebas correctas")
        print("✅ El scanner SOLO acepta QRs del sistema REP desktop")
        print("✅ Todos los QRs inválidos son rechazados correctamente")
    else:
        print(f"\n⚠️ PROBLEMAS DETECTADOS: {results['errors']} errores de validación")
        print("🔧 Revisar lógica de validación en PointsManager.kt")
    
    print("\n💡 FORMATOS VÁLIDOS ÚNICAMENTE:")
    print("   ✅ CODELPA:[12 caracteres hexadecimales]")
    print("   ✅ TERCERO:[12 caracteres hexadecimales]")
    print("   ❌ Cualquier otro formato será rechazado")

if __name__ == "__main__":
    main()