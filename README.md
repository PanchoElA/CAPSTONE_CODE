# Sistema REP Optimizado

## 🌱 Descripción
Sistema simplificado de Responsabilidad Extendida del Productor (REP) compuesto por:
- **Scanner App Android**: Escanea QR + envía datos al servidor
- **Desktop App**: Visualiza datos del servidor  
- **Servidor REP**: Recibe y almacena datos de escaneos

## 📁 Estructura del Proyecto
```
├── server_rep.py              # Servidor Flask optimizado
├── desktop_app/
│   └── desktop_app.py         # Aplicación de escritorio simple
├── APP_SCAN/                  # Scanner App Android
│   ├── app/src/main/java/     # Código Kotlin
│   └── build.gradle           # Configuración Android
└── INICIAR_SISTEMA.bat        # Script de inicio
```

## 🚀 Uso Rápido

### 1. Iniciar Sistema
```bash
# Doble click en:
INICIAR_SISTEMA.bat
```

### 2. Scanner App Android
- Compilar APK con Android Studio
- Instalar en dispositivo Android
- Configurar URL: `http://192.168.5.53:5000`
- Escanear códigos QR

### 3. Ver Datos
- Desktop App muestra escaneos en tiempo real
- Servidor web: `http://192.168.5.53:5000`

## 🛠️ Tecnologías
- **Servidor**: Python Flask + SQLite
- **Android**: Kotlin + CameraX + OkHttp  
- **Desktop**: Python Tkinter
- **API**: REST JSON simple

## ⚡ Funcionalidad
1. **Scanner App**: Escanea QR → Envía a servidor
2. **Servidor**: Recibe datos → Guarda en base de datos
3. **Desktop App**: Consulta servidor → Muestra datos

**¡Sistema listo y optimizado!** 🎯