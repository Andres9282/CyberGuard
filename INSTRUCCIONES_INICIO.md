# 🚀 INSTRUCCIONES PARA INICIAR EL DASHBOARD

## ⚡ INICIO RÁPIDO

### Opción 1: Usar el script de inicio (Windows)
```powershell
.\iniciar_dashboard.bat
```

### Opción 2: Inicio manual
```powershell
cd dashboard
python app_integrated.py
```

## 📋 PASOS DETALLADOS

### 1. Abre PowerShell en el directorio del proyecto
```powershell
cd C:\Users\danie\OneDrive\Desktop\CyberGuard
```

### 2. Inicia el Dashboard
```powershell
python dashboard/app_integrated.py
```

### 3. Verás un mensaje como este:
```
============================================================
🚀 CYBERGUARD SV - SISTEMA REAL
============================================================

📊 DASHBOARD DISPONIBLE EN:
   Local:    http://localhost:5001
   Red:      http://192.168.1.XXX:5001

📡 ENDPOINT DE EVENTOS:
   http://192.168.1.XXX:5001/event

💾 Base de datos: database/cyberguard.db
📝 Los casos mostrados son REALES de la base de datos

============================================================
✅ Servidor iniciando...
   Presiona Ctrl+C para detener
============================================================
```

### 4. Abre tu navegador
Ve a: **http://localhost:5001**

## 🔍 VERIFICAR QUE FUNCIONA

### Prueba 1: Endpoint de prueba
Abre en el navegador:
```
http://localhost:5001/api/test
```

Deberías ver:
```json
{
  "status": "ok",
  "message": "Servidor funcionando correctamente",
  "timestamp": "2024-..."
}
```

### Prueba 2: Estado del sistema
Abre en el navegador:
```
http://localhost:5001/api/status
```

Deberías ver el estado del sistema en JSON.

### Prueba 3: Consola del navegador
1. Abre el dashboard: http://localhost:5001
2. Presiona **F12** para abrir las herramientas de desarrollador
3. Ve a la pestaña **Console**
4. Deberías ver mensajes como:
   - 🚀 Inicializando CyberGuard Dashboard...
   - ✅ Dashboard inicializado correctamente
   - 🔄 Cargando estado del sistema...
   - ✅ Estado del sistema: {...}
   - 🔄 Cargando casos...
   - ✅ Casos cargados: 0

## 🌐 ACCESO DESDE OTRA COMPUTADORA

Si quieres acceder desde otra computadora en la misma red:

1. **Obtén la IP de tu computadora** (se muestra al iniciar el servidor)
2. **Desde la otra computadora**, abre:
   ```
   http://TU_IP:5001
   ```
   Ejemplo: `http://192.168.1.100:5001`

## ⚠️ SOLUCIÓN DE PROBLEMAS

### El dashboard no carga
1. Verifica que el servidor esté corriendo (deberías ver mensajes en la terminal)
2. Abre la consola del navegador (F12) y revisa errores
3. Prueba el endpoint de prueba: http://localhost:5001/api/test

### Error de conexión
1. Verifica que no haya otro proceso usando el puerto 5001
2. Verifica que el firewall no esté bloqueando el puerto
3. Asegúrate de estar usando la URL correcta: http://localhost:5001

### No se muestran casos
- Es normal si no has ejecutado ningún ataque aún
- Los casos aparecerán automáticamente cuando el monitor detecte un ataque
- El dashboard se actualiza cada 3 segundos automáticamente

## 📡 CONFIGURACIÓN DEL MONITOR

El monitor en la PC2 debe estar configurado para enviar eventos a:
```
http://TU_IP_PC1:5001/event
```

Donde `TU_IP_PC1` es la IP que se muestra al iniciar el dashboard.

## ✅ TODO LISTO

Una vez que veas el dashboard cargando correctamente:
- ✅ Frontend conectado
- ✅ Backend funcionando
- ✅ Base de datos lista
- ✅ Endpoints disponibles

¡El sistema está listo para recibir ataques y mostrarlos en tiempo real!

