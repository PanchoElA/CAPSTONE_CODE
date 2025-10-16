# 🔧 SOLUCIÓN ERRORES DE CONEXIÓN - Sistema REP

## ❌ **PROBLEMA IDENTIFICADO**

```
Error de conexión: HTTPConnectionPool(host='192.168.5.53', port=5000): 
Max retries exceeded with url /
```

## ✅ **SOLUCIONES PASO A PASO**

### **🚀 Solución 1: Iniciar Servidor Automáticamente**

```powershell
# Ejecutar desde directorio principal
.\INICIAR_SISTEMA_COMPLETO.bat
```

Esto hace:
- ✅ Inicia servidor REP automáticamente
- ✅ Abre puerto 5000 en firewall
- ✅ Lanza aplicación desktop
- ✅ Configura todo automáticamente

### **🔥 Solución 2: Iniciar Solo Servidor**

```powershell
cd android_app\server
.\INICIAR_SERVIDOR_REP.bat
```

### **🌐 Solución 3: Verificar Conectividad**

1. **Abrir Desktop App**
2. **Ir a pestaña "⚙️ Configuración"**  
3. **Probar URLs en este orden:**
   - `http://192.168.5.53:5000`
   - `http://localhost:5000`  
   - `http://127.0.0.1:5000`

### **🔒 Solución 4: Configurar Firewall Manualmente**

```powershell
# Ejecutar como Administrador
netsh advfirewall firewall add rule name="Python REP Server" dir=in action=allow protocol=TCP localport=5000
```

### **📱 Solución 5: Apps Android**

**Actualizar URL en apps móviles:**

```kotlin
// En ApiClient.kt (tanto Scanner como App Sustentable)
private val BASE_URL = "http://TU_IP_REAL:5000"
```

**Obtener IP real:**
```powershell
ipconfig | findstr "IPv4"
```

## 🔍 **DIAGNÓSTICO DE PROBLEMAS**

### **Error 1: "No connection could be made"**
- ❌ **Causa**: Servidor no está ejecutándose
- ✅ **Solución**: Ejecutar `INICIAR_SERVIDOR_REP.bat`

### **Error 2: "Connection refused"**
- ❌ **Causa**: Firewall bloquea puerto 5000
- ✅ **Solución**: Ejecutar como administrador o usar localhost

### **Error 3: "Target machine actively refused"**
- ❌ **Causa**: IP incorrecta o servidor caído
- ✅ **Solución**: Verificar IP con `ipconfig` y reiniciar servidor

### **Error 4: Apps Android no conectan**
- ❌ **Causa**: Diferentes redes WiFi
- ✅ **Solución**: Conectar todas las devices a misma WiFi

## 🎯 **VERIFICACIÓN RÁPIDA**

### **1. Servidor Funcionando:**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/" -UseBasicParsing
```

### **2. Red Funcionando:**
```powershell
Invoke-WebRequest -Uri "http://192.168.5.53:5000/" -UseBasicParsing
```

### **3. Desktop App Conectada:**
- Abrir app → pestaña Configuración → "🔌 Probar Conexión"

## 🚀 **INICIO RECOMENDADO**

### **Orden Correcto:**
```
1. Ejecutar: INICIAR_SISTEMA_COMPLETO.bat
2. Esperar ventanas del servidor y desktop
3. Verificar conexión en desktop app
4. Compilar e instalar apps Android
5. Probar flujo completo
```

### **URLs por Aplicación:**

| Aplicación | URL Recomendada |
|------------|----------------|
| Desktop App | Autodetección (localhost primero) |
| Scanner App | `http://192.168.5.53:5000` |
| App Sustentable | `http://192.168.5.53:5000` |

## 📱 **CONFIGURACIÓN APPS ANDROID**

### **Si cambias IP del servidor:**

1. **Scanner App**: Editar `PointsManager.kt`
2. **App Sustentable**: Editar `ApiClient.kt`
3. **Recompilar ambas apps**

```kotlin
// Cambiar en ambas apps
private val BASE_URL = "http://TU_IP_NUEVA:5000"
```

## 🎉 **VERIFICACIÓN EXITOSA**

**Cuando todo funcione verás:**
- ✅ Servidor: "Running on http://192.168.5.53:5000"
- ✅ Desktop: "🔌 Conectado al servidor REP"
- ✅ Apps Android: Pueden consultar datos sin errores

## 🆘 **SI NADA FUNCIONA**

### **Plan B - Solo Localhost:**
1. Cambiar todas las URLs a `localhost:5000`
2. Usar solo en el PC (sin apps Android)
3. Funcionalidad completa en desktop app

### **Plan C - IP Manual:**
1. Obtener IP real: `ipconfig`
2. Actualizar todas las configuraciones
3. Abrir puerto manualmente en Windows Defender

**¡El sistema está diseñado para funcionar! Solo necesita la configuración inicial correcta.** 🚀