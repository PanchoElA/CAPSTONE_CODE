# 🌿 Sistema REP - Responsabilidad Extendida del Productor

## 📋 Descripción del Proyecto

Sistema completo de trazabilidad para baldes de pintura bajo el marco de **Responsabilidad Extendida del Productor (REP)** en Chile. El sistema permite el seguimiento completo del ciclo de vida de envases de pintura, diferenciando entre baldes de CODELPA (para reúso) y baldes de terceros (para valorización).

## 🏗️ Arquitectura del Sistema

El proyecto consta de **4 aplicaciones principales**:

### 📱 1. Scanner App (Android)
- **Ubicación**: `android_app/`
- **Función**: Escaneo de QRs REP para otorgar puntos
- **Tecnología**: Kotlin, OkHttp, ZXing
- **Puntos**: CODELPA (150 pts), TERCERO (100 pts)

### 📲 2. App Sustentable (Android)  
- **Ubicación**: `client_app/`
- **Función**: Consulta de historial y datos de retornos
- **Tecnología**: Kotlin, Retrofit, RecyclerView
- **Características**: Visualización de retornos por cliente

### 🖥️ 3. Desktop App (Generador QR)
- **Ubicación**: `desktop_app/`
- **Función**: Generación y gestión de QRs REP
- **Tecnología**: Python, Tkinter, PIL, QRCode
- **Características**: Generación batch, imágenes QR, dashboard

### 🌐 4. Servidor REP
- **Ubicación**: `android_app/server/`
- **Función**: Backend central con API REST
- **Tecnología**: Flask, SQLite
- **Endpoints**: Generación QR, retornos, reportería

## 🎯 Características Principales

### ✅ Trazabilidad Completa
- **QR únicos** con formato `CODELPA:XXXXXXXXXXXX` o `TERCERO:XXXXXXXXXXXX`
- **Validación estricta** - solo QRs generados por el sistema desktop
- **Base de datos** con todos los campos requeridos por normativa REP

### 🔒 Seguridad
- **Validación hexadecimal** de 12 caracteres
- **Rechazo automático** de QRs no autorizados
- **Prevención de duplicados** y reutilización

### 📊 Reportería Regulatoria
- **Lotes mensuales** en formato YYYYMM
- **Destinos diferenciados**: REUSO_CODELPA vs VALORIZACION_INPROPLAS  
- **Exportación CSV** para reportes oficiales
- **Dashboard** en tiempo real

### 🌐 Conectividad
- **WiFi multiplataforma** entre todas las aplicaciones
- **Sincronización automática** servidor-aplicaciones
- **Fallback servers** para redundancia

## 🚀 Instalación y Uso

### 1. Iniciar Sistema Completo
```bash
# Ejecutar desde directorio principal
.\INICIAR_SISTEMA_COMPLETO.bat
```

### 2. Solo Servidor REP
```bash
cd android_app\server
.\INICIAR_SERVIDOR_REP.bat
```

### 3. Solo Desktop App
```bash
cd desktop_app
.\EJECUTAR_SISTEMA_REP.bat
```

### 4. Compilar Apps Android

**Scanner App:**
```bash
cd android_app
./gradlew assembleDebug
```

**App Sustentable:**
```bash
cd client_app  
./gradlew assembleDebug
```

## 📋 Requisitos del Sistema

### 🖥️ PC (Servidor + Desktop)
- **Python 3.7+**
- **Librerías**: Flask, Pillow, qrcode, tkinter
- **Windows 10/11**
- **Red WiFi**

### 📱 Android (Apps)
- **Android 7.0+ (API 24)**  
- **Cámara** para escaneo QR
- **WiFi** misma red que el servidor

### 🌐 Red
- **Router WiFi** para conectar PC y dispositivos móviles
- **Puerto 5000** abierto en firewall de Windows

## 🗃️ Base de Datos

### Tabla `qr_generated`
```sql
- qr_id (TEXT PRIMARY KEY)
- marca_envase (TEXT)  
- origen (TEXT)
- fecha_generacion (TIMESTAMP)
- usado (BOOLEAN DEFAULT FALSE)
- lote_reporte (TEXT)
```

### Tabla `retornos_rep`
```sql
- id (INTEGER PRIMARY KEY)
- qr_id (TEXT REFERENCES qr_generated)
- fecha_retorno (TIMESTAMP)
- estado_retorno (TEXT)
- peso_envase_kg (REAL)
- destino (TEXT)
- tienda_retorno (TEXT)  
- evidencia (TEXT)
- cliente_profile (TEXT)
- puntos_otorgados (INTEGER)
```

## 📈 Flujo del Sistema

```
1. 🖥️ Desktop App → Genera QR REP único
2. 📱 Scanner App → Escanea QR y otorga puntos  
3. 🌐 Servidor → Procesa retorno y actualiza BD
4. 📲 App Sustentable → Consulta historial cliente
5. 📊 Dashboard → Reportes y estadísticas
6. 📄 Exportación → CSV para autoridades
```

## 🏭 Cumplimiento Normativo REP

### ✅ Diferenciación de Destinos
- **CODELPA** estado BUENO/REPARABLE → **REUSO_CODELPA** (150 pts)
- **CODELPA** estado MALO → **VALORIZACION_INPROPLAS** (100 pts)  
- **TERCEROS** cualquier estado → **VALORIZACION_INPROPLAS** (100 pts)

### 📋 Campos Obligatorios REP
- ✅ `qr_id` - Identificador único del envase
- ✅ `marca_envase` - CODELPA o marca tercero
- ✅ `origen` - Punto de generación
- ✅ `fecha_retorno` - Timestamp del retorno
- ✅ `estado_retorno` - BUENO/MALO/REPARABLE
- ✅ `peso_envase_kg` - Peso del envase
- ✅ `destino` - REUSO_CODELPA/VALORIZACION_INPROPLAS
- ✅ `tienda_retorno` - Punto de retorno
- ✅ `evidencia` - Documentación del retorno
- ✅ `lote_reporte` - Batch mensual YYYYMM

## 🛠️ Diagnósticos y Troubleshooting

### 🔧 Herramientas de Diagnóstico
- `diagnostico_conectividad.py` - Verificar red y servidor
- `test_validacion_final.py` - Probar QRs y endpoints
- `diagnostico_escaneo.py` - Debug scanner app

### ⚠️ Problemas Comunes

**"rep_network_error"**
- ✅ Verificar servidor ejecutándose
- ✅ Comprobar mismo WiFi
- ✅ Firewall puerto 5000

**QRs no reconocidos**  
- ✅ Solo QRs generados por desktop app
- ✅ Formato: `TIPO:XXXXXXXXXXXX`
- ✅ 12 caracteres hexadecimales exactos

## 👥 Autores

- **Franco Travisany** - Desarrollo completo del sistema
- **Universidad Adolfo Ibáñez** - Proyecto CAPSTONE

## 📄 Licencia

Este proyecto es parte de un trabajo de titulación académico.

## 🌟 Estado del Proyecto

- ✅ **Sistema completo funcional**
- ✅ **4 aplicaciones integradas**  
- ✅ **Validación estricta de seguridad**
- ✅ **Reportería REP compliant**
- ✅ **Conectividad multiplataforma**

---

**🎯 Sistema REP completo para cumplimiento normativo de Responsabilidad Extendida del Productor en Chile** 🇨🇱