# Cliente REP - Aplicación Android

Aplicación móvil para que los clientes consulten sus puntos REP y historial de retornos de baldes.

## Funcionalidades

- **Consulta de perfil**: Los usuarios pueden buscar su perfil por nombre
- **Dashboard de puntos**: Visualización de puntos acumulados, retornos realizados y peso total
- **Historial de retornos**: Lista de los retornos recientes y historial completo
- **Actualización automática**: Pull-to-refresh para sincronizar datos
- **Memoria de usuario**: Recuerda el último nombre buscado

## Estructura de la Aplicación

### Actividades
- `MainActivity.kt`: Pantalla principal con búsqueda y dashboard
- `HistorialActivity.kt`: Historial completo de retornos

### Componentes
- `Models.kt`: Clases de datos para la comunicación con el servidor
- `ApiClient.kt`: Cliente HTTP para comunicación con el servidor REP
- `RetornosAdapter.kt`: Adaptador para mostrar la lista de retornos

### Layouts
- `activity_main.xml`: Dashboard principal con estadísticas y retornos recientes
- `activity_historial.xml`: Lista completa de retornos
- `item_retorno.xml`: Item individual en la lista de retornos

## Configuración

### Servidor
Por defecto, la app apunta a `http://192.168.5.53:5000`. 

Para cambiar la URL del servidor, modifica la constante en `ApiClient.kt` o implementa un sistema de configuración.

### Requisitos
- Android 7.0 (API level 24) o superior
- Conexión a internet
- Acceso al servidor REP

## Instalación

1. Compila el proyecto con Android Studio
2. Instala el APK en el dispositivo Android
3. Asegúrate de que el dispositivo tenga acceso al servidor REP

## Uso

1. Abre la aplicación
2. Ingresa tu nombre completo en el campo de búsqueda
3. Presiona "Buscar" para cargar tu información
4. Consulta tus puntos, retornos y peso total en el dashboard
5. Ve el historial reciente o presiona "Ver Todo" para el historial completo
6. Usa "Pull to refresh" para actualizar la información

## API Integration

La aplicación se comunica con el servidor REP a través de estos endpoints:

- `GET /cliente_retornos/<nombre>`: Obtiene resumen del cliente con retornos recientes
- `GET /retornos_completos/<nombre>`: Obtiene historial completo de retornos

## Características Técnicas

- **Networking**: OkHttp para comunicación HTTP
- **JSON**: Gson para parsing de respuestas
- **UI**: Material Design Components
- **Concurrencia**: Kotlin Coroutines para operaciones asíncronas
- **Storage**: SharedPreferences para configuración local

## Estados de la Aplicación

- **Búsqueda**: Input de nombre y botón de búsqueda
- **Cargando**: Indicador de progreso durante consultas
- **Dashboard**: Estadísticas y lista de retornos recientes
- **Historial**: Lista completa de todos los retornos
- **Error**: Mensajes informativos para errores de conexión o cliente no encontrado

## Próximas Mejoras

- Sistema de configuración para URL del servidor
- Notificaciones push para nuevos puntos
- Caché local para uso offline
- Autenticación de usuario
- Filtros y búsqueda en el historial