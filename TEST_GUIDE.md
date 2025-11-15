# 🧪 Guía de Pruebas - CyberGuard Backend

## 📋 Paso 1: Iniciar el Servidor

Abre una terminal y ejecuta:

```bash
cd backend
python server_local.py
```

Deberías ver algo como:
```
✅ Tablas creadas correctamente

📋 Rutas registradas:
   ['GET', 'HEAD', 'OPTIONS'] /
   ['GET', 'HEAD', 'OPTIONS'] /status
   ['GET', 'HEAD', 'OPTIONS'] /cases
   ['GET', 'HEAD', 'OPTIONS'] /cases/<int:case_id>
   ['GET', 'HEAD', 'OPTIONS'] /report/<int:case_id>
   ['POST', 'OPTIONS'] /event
   ...

🚀 Iniciando servidor en http://127.0.0.1:5001
```

**¡El servidor está corriendo!** Déjalo abierto.

---

## 📋 Paso 2: Probar Endpoints Básicos

### 2.1 Verificar que el servidor responde

Abre tu navegador y ve a:
```
http://127.0.0.1:5001/status
```

Deberías ver:
```json
{
  "status": "backend listo 🔥",
  "message": "Todo funcionando VAMOSSSSSSSSSSS 💪",
  "ok": true
}
```

### 2.2 Ver todas las rutas disponibles

```
http://127.0.0.1:5001/debug/routes
```

---

## 📋 Paso 3: Crear Datos de Prueba

### Opción A: Usar el endpoint de test-data (MÁS FÁCIL)

Abre otra terminal (o usa Postman/Thunder Client) y envía un POST:

**Con PowerShell:**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5001/debug/test-data" -Method POST
```

**Con curl (si lo tienes):**
```bash
curl -X POST http://127.0.0.1:5001/debug/test-data
```

**Con Postman/Thunder Client:**
- Método: `POST`
- URL: `http://127.0.0.1:5001/debug/test-data`
- No necesitas body

Deberías recibir:
```json
{
  "status": "ok",
  "message": "Datos de prueba creados exitosamente",
  "case_id": 1
}
```

### Opción B: Enviar un evento manual (MÁS REALISTA)

**Con PowerShell:**
```powershell
$body = @{
    timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")
    severity = "high"
    folder = "C:\test\monitored_folder"
    actions = @("process_killed", "files_quarantined")
    process = @{
        name = "malware.exe"
    }
    network = @{
        attacker_ip = "192.168.1.100"
    }
    events = @(
        @{
            event_type = "file_encryption"
            details = @{
                files_affected = 15
            }
        }
    )
    artifacts = @(
        @{
            file_path = "C:\test\file1.txt"
            hash = "abc123def456"
            operation = "encrypted"
        }
    )
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri "http://127.0.0.1:5001/event" -Method POST -Body $body -ContentType "application/json"
```

**Con curl:**
```bash
curl -X POST http://127.0.0.1:5001/event \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-01-15T10:30:00",
    "severity": "high",
    "folder": "C:\\test\\monitored_folder",
    "actions": ["process_killed", "files_quarantined"],
    "process": {
      "name": "malware.exe"
    },
    "network": {
      "attacker_ip": "192.168.1.100"
    },
    "events": [
      {
        "event_type": "file_encryption",
        "details": {"files_affected": 15}
      }
    ],
    "artifacts": [
      {
        "file_path": "C:\\test\\file1.txt",
        "hash": "abc123def456",
        "operation": "encrypted"
      }
    ]
  }'
```

---

## 📋 Paso 4: Verificar que los Datos se Guardaron

### 4.1 Ver todos los casos

Abre en el navegador:
```
http://127.0.0.1:5001/cases
```

Deberías ver un JSON con todos los casos guardados.

### 4.2 Ver detalles de un caso específico

```
http://127.0.0.1:5001/cases/1
```

Reemplaza `1` con el `case_id` que recibiste.

---

## 📋 Paso 5: Ver el Reporte HTML

Abre en el navegador:
```
http://127.0.0.1:5001/report/1
```

Deberías ver un reporte HTML completo con:
- ✅ Información general del caso
- ✅ Eventos registrados
- ✅ Artefactos capturados
- ✅ Carpeta afectada
- ✅ Acciones tomadas

---

## 📋 Paso 6: Probar con el Agente Real (Opcional)

Si tu compañero tiene el agente funcionando:

1. Asegúrate que el agente apunte a: `http://127.0.0.1:5001/event`
2. Ejecuta el agente
3. El agente debería enviar eventos automáticamente cuando detecte algo
4. Verifica en `/cases` que se crearon nuevos casos

---

## ✅ Checklist de Pruebas

- [ ] Servidor inicia correctamente
- [ ] `/status` responde OK
- [ ] `/debug/routes` muestra todas las rutas
- [ ] `/debug/test-data` crea un caso de prueba
- [ ] `/cases` muestra los casos guardados
- [ ] `/cases/1` muestra detalles del caso
- [ ] `/report/1` genera el reporte HTML correctamente
- [ ] `/event` acepta eventos POST correctamente

---

## 🐛 Si algo falla

1. **Revisa la consola del servidor** - Ahí verás los errores
2. **Verifica que la base de datos existe** en `C:\CyberGuardData\database.db`
3. **Revisa que el puerto 5001 no esté ocupado**
4. **Verifica que tienes Flask instalado**: `pip install flask flask-cors`

---

## 📝 Notas

- El servidor corre en modo `debug=True`, así que se recarga automáticamente cuando cambias código
- La base de datos se crea automáticamente en `C:\CyberGuardData\database.db`
- Los datos de prueba se pueden crear múltiples veces (cada vez crea un nuevo caso)

