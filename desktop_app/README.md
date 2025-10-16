# 🌱 SISTEMA REP - Aplicación de Escritorio

## 🎯 **REEMPLAZA LA INTERFAZ WEB**

Esta aplicación de escritorio para PC reemplaza completamente la interfaz web del sistema REP, proporcionando una experiencia nativa y conectada.

## ✅ **CONECTIVIDAD TOTAL**

### **🔗 Aplicaciones Conectadas:**
- 📱 **App Scanner Android** - Escanea QRs y registra retornos
- 📱 **App Sustentable Android** - Los clientes consultan sus puntos
- 💻 **Sistema Desktop PC** - Gestión completa del sistema

### **🔄 Flujo Completo Conectado:**
```
💻 PC genera QR → 📱 Scanner escanea → 📱 Cliente ve puntos
           ↓                ↓                    ↓
    Servidor REP ←→ Servidor REP ←→ Servidor REP
```

## 🚀 **EJECUCIÓN SIMPLE**

### **Método 1: Script Automático**
```
1. Hacer doble clic en: EJECUTAR_SISTEMA_REP.bat
2. El script instala dependencias automáticamente
3. Lanza la aplicación
```

### **Método 2: Manual**
```powershell
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python sistema_rep_desktop.py
```

## 📱 **FUNCIONALIDADES**

### **🎯 Generador QR**
- Genera QRs únicos CODELPA: y TERCERO:
- Configura marca, origen y cantidad
- Envía automáticamente al servidor
- QRs listos para escanear en apps móviles

### **📊 Dashboard REP**
- Estadísticas en tiempo real
- Reportes mensuales por lotes (YYYYMM)
- Exportación CSV para cumplimiento
- Visualización de datos conectados

### **👤 Consulta Cliente**
- Busca cualquier cliente por nombre
- Muestra puntos, retornos y historial
- Misma información que ve en App Sustentable
- Verificación de conectividad

### **⚙️ Configuración**
- Configura URL del servidor
- Prueba conexión en tiempo real
- Información del sistema completo

## 🌐 **CONFIGURACIÓN DE RED**

### **Servidor Centralizado:**
```
Servidor REP: http://192.168.5.53:5000
├── Desktop App (PC) - Gestión
├── Scanner App (Android) - Escaneo  
└── App Sustentable (Android) - Cliente
```

### **Requisitos de Red:**
- Todas las aplicaciones en la misma red WiFi
- PC con IP fija o conocida para el servidor
- Puerto 5000 abierto para comunicación

## 🔧 **SINCRONIZACIÓN AUTOMÁTICA**

### **Datos Compartidos:**
- ✅ QRs generados en PC → visibles en Scanner
- ✅ Retornos escaneados → visibles en PC y App Cliente
- ✅ Puntos acumulados → sincronizados en tiempo real
- ✅ Historial completo → accesible desde todas las apps

### **Ejemplo de Flujo:**
```
1. 💻 PC genera QR "CODELPA:ABC123"
2. 📱 Scanner lee QR → registra retorno → +150 puntos
3. 📱 App Sustentable muestra los 150 puntos nuevos
4. 💻 PC ve el retorno en estadísticas actualizadas
```

## 📋 **REQUISITOS TÉCNICOS**

### **Software:**
- Python 3.8 o superior
- Dependencias: requests, qrcode, Pillow
- Windows 10/11 (compatible con otros OS)

### **Hardware:**
- PC conectado a WiFi
- Mínimo 4GB RAM
- 100MB espacio en disco

## 🎉 **VENTAJAS DE LA APP DESKTOP**

### **vs Interfaz Web:**
- ✅ No necesita navegador
- ✅ Interfaz nativa más rápida
- ✅ Mejor experiencia de usuario
- ✅ Funciona sin depender de navegador
- ✅ Inicio automático con scripts

### **Conectividad Mejorada:**
- ✅ Prueba conexión automática
- ✅ Configuración de servidor flexible
- ✅ Estadísticas en tiempo real
- ✅ Sincronización inmediata

## 🏆 **SISTEMA COMPLETO FUNCIONANDO**

Con la aplicación desktop, el sistema REP está **100% COMPLETO**:

1. 💻 **Desktop App** - Gestión y generación QR
2. 📱 **Scanner App** - Escaneo y registro
3. 📱 **App Sustentable** - Consulta cliente
4. 🗄️ **Servidor REP** - Base de datos centralizada

## 🔄 **NOMBRE ACTUALIZADO**

- ❌ "Cliente REP" (anterior)
- ✅ "APP SUSTENTABLE" (nuevo)

**¡El sistema está listo para demostración completa!**