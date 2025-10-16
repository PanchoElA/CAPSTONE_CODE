#!/usr/bin/env python3
"""
🖼️ SISTEMA REP - GENERADOR QR CON IMÁGENES
Prueba la funcionalidad de generación de imágenes QR
"""

import qrcode
from PIL import Image
import os
from datetime import datetime

def test_qr_generation():
    """Prueba generar algunos QRs de ejemplo"""
    print("🖼️ PROBANDO GENERACIÓN DE IMÁGENES QR")
    print("=" * 50)
    
    # QRs de ejemplo
    qr_codes = [
        {"codigo": "CODELPA:ABC123DEF456", "marca": "SHERWIN", "origen": "MP"},
        {"codigo": "TERCERO:789GHI012JKL", "marca": "BENJAMIN_MOORE", "origen": "TIENDA"},
        {"codigo": "CODELPA:MNO345PQR678", "marca": "CODELPA_PRIME", "origen": "PLANTA"}
    ]
    
    # Crear carpeta para ejemplos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"QRs_EJEMPLO_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)
    
    print(f"📁 Creando QRs en carpeta: {folder_name}")
    
    for i, qr_data in enumerate(qr_codes, 1):
        print(f"\n🎯 Generando QR {i}/3:")
        print(f"   🆔 Código: {qr_data['codigo']}")
        print(f"   🏷️ Marca: {qr_data['marca']}")
        print(f"   📍 Origen: {qr_data['origen']}")
        
        try:
            # Generar QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=8,  # Tamaño más grande para mejor calidad
                border=4,
            )
            qr.add_data(qr_data['codigo'])
            qr.make(fit=True)
            
            # Crear imagen
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Redimensionar para uso
            qr_img_small = qr_img.resize((200, 200), Image.Resampling.LANCZOS)
            qr_img_large = qr_img.resize((400, 400), Image.Resampling.LANCZOS)
            
            # Guardar archivos
            filename_small = f"QR_{qr_data['codigo'].replace(':', '_')}_200x200.png"
            filename_large = f"QR_{qr_data['codigo'].replace(':', '_')}_400x400.png"
            
            qr_img_small.save(os.path.join(folder_name, filename_small))
            qr_img_large.save(os.path.join(folder_name, filename_large))
            
            print(f"   ✅ Guardado: {filename_small}")
            print(f"   ✅ Guardado: {filename_large}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Crear archivo de información
    info_file = os.path.join(folder_name, "INFO_QRs.txt")
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write("🖼️ CÓDIGOS QR GENERADOS - SISTEMA REP\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"📅 Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"📊 Total de QRs: {len(qr_codes)}\n\n")
        
        for i, qr_data in enumerate(qr_codes, 1):
            f.write(f"QR {i}:\n")
            f.write(f"  🆔 Código: {qr_data['codigo']}\n")
            f.write(f"  🏷️ Marca: {qr_data['marca']}\n")
            f.write(f"  📍 Origen: {qr_data['origen']}\n")
            f.write(f"  📱 Archivos: QR_{qr_data['codigo'].replace(':', '_')}_200x200.png\n")
            f.write(f"            QR_{qr_data['codigo'].replace(':', '_')}_400x400.png\n\n")
        
        f.write("💡 USO DE LOS ARCHIVOS:\n")
        f.write("  • 200x200: Para mostrar en aplicaciones\n")
        f.write("  • 400x400: Para imprimir etiquetas\n\n")
        f.write("📱 ESCANEO:\n")
        f.write("  • Use cualquier lector QR estándar\n")
        f.write("  • También funciona con la Scanner App del sistema\n")
    
    print(f"\n✅ GENERACIÓN COMPLETADA")
    print(f"📁 Archivos guardados en: {folder_name}")
    print(f"📋 Ver información en: {info_file}")
    
    return folder_name

def main():
    """Función principal"""
    print("🖼️ SISTEMA REP - PRUEBA DE GENERACIÓN QR")
    print("🕐", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    
    try:
        folder = test_qr_generation()
        
        print("\n" + "=" * 60)
        print("🎉 PRUEBA COMPLETADA EXITOSAMENTE")
        print(f"📁 Carpeta creada: {folder}")
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Revisar las imágenes QR generadas")
        print("   2. Probar escaneando con tu teléfono")
        print("   3. Usar la aplicación desktop para generar más")
        print("   4. Imprimir QRs para etiquetas físicas")
        
    except Exception as e:
        print(f"\n❌ ERROR EN LA PRUEBA: {str(e)}")

if __name__ == "__main__":
    main()