# 🎯 Tutorial: Simulación de Ataque Remoto - CyberGuard

Este tutorial te guía paso a paso para ejecutar un ataque desde la **Computadora 2** y que sea detectado y bloqueado en la **Computadora 1**.

## 📋 Requisitos Previos

- **Computadora 1** (Esta): Tiene el backend y dashboard
- **Computadora 2**: Tiene el agente y servidor de ataque
- Ambas computadoras en la misma red
- Python instalado en ambas
- Dependencias instaladas (`pip install -r requirements.txt`)

## 🔧 Paso 1: Configurar las IPs

### En Computadora 1 (Esta computadora):

1. Abre `backend/config.py`
2. Busca y actualiza estas líneas con la IP de la Computadora 2:

```python
# IP de la computadora donde está el agente (Computadora 2)
AGENT_IP = "192.168.1.XXX"  # ← Cambia por la IP real de la Computadora 2

# URL del backend para que el agente se conecte (IP de esta computadora)
BACKEND_URL = "http://TU_IP_COMPUTADORA_1:5001"  # ← Cambia por tu IP
```

### En Computadora 2:

1. Abre `backend/config.py` (o créalo si no existe)
2. Configura la URL del backend:

```python
# URL del backend (IP de la Computadora 1)
BACKEND_URL = "http://IP_COMPUTADORA_1:5001"  # ← IP de la Computadora 1
```

### 📝 Cómo saber tu IP:

**Windows:**
```cmd
ipconfig
```
Busca "IPv4 Address" en la sección de tu adaptador de red.

**Linux/WSL:**
```bash
hostname -I
# o
ip addr show
```

## 🚀 Paso 2: Preparar la Carpeta de Ataque

### En Computadora 2:

Crea la carpeta que será monitoreada y atacada:

**Linux/WSL:**
```bash
mkdir -p /home/andres/attack_test
# Crea algunos archivos de prueba
cd /home/andres/attack_test
for i in {1..5}; do echo "Archivo de prueba $i" > test_$i.txt; done
```

**Windows:**
```cmd
mkdir C:\attack_test
cd C:\attack_test
for /L %i in (1,1,5) do echo Archivo de prueba %i > test_%i.txt
```

## 🖥️ Paso 3: Iniciar Servicios en Computadora 1 (Esta)

Abre **DOS terminales** en la Computadora 1:

### Terminal 1 - Backend:
```bash
cd CyberGuard
python backend/server.py
```

Deberías ver:
```
🔵 CyberGuard Backend iniciado
   Host: 0.0.0.0
   Port: 5001
 * Running on http://0.0.0.0:5001
```

**¡NO CIERRES ESTA TERMINAL!**

## 🖥️ Paso 4: Iniciar Servicios en Computadora 2

Abre **DOS terminales** en la Computadora 2:

### Terminal 1 - Monitor (detecta ataques):
```bash
cd CyberGuard
python agent/monitor.py
```

Deberías ver:
```
🔵 CyberGuard Agent iniciado...
Vigilando: /home/andres/attack_test
```

**¡NO CIERRES ESTA TERMINAL!**

### Terminal 2 - Servidor de Ataque Remoto:
```bash
cd CyberGuard
python agent/remote_attack_server.py
```

Deberías ver:
```
🔴 Servidor de Ataque Remoto iniciado
   Host: 0.0.0.0
   Port: 5002
   Carpeta monitoreada: /home/andres/attack_test

   Para ejecutar un ataque desde otra computadora:
   POST http://<IP_ESTA_COMPUTADORA>:5002/attack
```

**¡NO CIERRES ESTA TERMINAL!**

## ✅ Paso 5: Verificar que Todo Está Conectado

### Desde Computadora 1:

Abre una **nueva terminal** y verifica la conexión:

```bash
# Verificar que el backend está funcionando
curl http://localhost:5001/

# Debería responder: "CyberGuard Backend OK"
```

### Desde Computadora 2:

Abre una **nueva terminal** y verifica:

```bash
# Verificar servidor de ataque
python attacker_client.py localhost --port 5002 --status

# Debería mostrar:
# ✅ Servidor de ataque disponible
#    Estado: running
#    Carpeta monitoreada: /home/andres/attack_test
```

## 🔥 Paso 6: Ejecutar el Ataque

Tienes **3 opciones** para ejecutar el ataque:

### Opción A: Desde Computadora 2 (Directo) ⭐ RECOMENDADO

En la Computadora 2, abre una nueva terminal:

```bash
cd CyberGuard

# Ejecutar ataque directo
python attacker_client.py localhost --port 5002 --files 10 --delay 0.1
```

### Opción B: Desde Computadora 1 (Remoto)

En la Computadora 1, abre una nueva terminal:

```bash
cd CyberGuard

# Usando curl
curl -X POST http://localhost:5001/trigger-attack \
  -H "Content-Type: application/json" \
  -d '{
    "agent_ip": "IP_COMPUTADORA_2",
    "agent_port": 5002,
    "num_files": 10,
    "delay": 0.1
  }'
```

O usando Python:
```python
import requests

response = requests.post(
    "http://localhost:5001/trigger-attack",
    json={
        "agent_ip": "IP_COMPUTADORA_2",  # Cambiar por IP real
        "agent_port": 5002,
        "num_files": 10,
        "delay": 0.1
    }
)
print(response.json())
```

### Opción C: Desde una Tercera Computadora

```bash
python attacker_client.py IP_COMPUTADORA_2 --port 5002 --files 10
```

## 👀 Paso 7: Observar la Detección y Bloqueo

### En Computadora 2 - Terminal del Monitor:

Deberías ver algo como:

```
⚠️ Cambio detectado: /home/andres/attack_test/test_1.txt
Features extraídos: [45.2, 60.1, 25, 15]
🔥 ATAQUE DETECTADO: posible ransomware
  🔒 test_1.txt → test_1.encrypted
  🔒 test_2.txt → test_2.locked
  ...
✅ Enviado a backend → {"status": "ok", "case_id": 1, ...}
```

### En Computadora 1 - Terminal del Backend:

Deberías ver:

```
🔴 Reenviando comando de ataque a IP_COMPUTADORA_2:5002
127.0.0.1 - - [2024-01-XX XX:XX:XX] "POST /trigger-attack HTTP/1.1" 200 -
127.0.0.1 - - [2024-01-XX XX:XX:XX] "POST /event HTTP/1.1" 200 -
```

### Verificar en la Base de Datos:

En Computadora 1:

```bash
# Ver casos detectados
curl http://localhost:5001/cases

# Ver detalles de un caso específico
curl http://localhost:5001/cases/1
```

## 🎬 Flujo Completo del Ataque

```
1. Tú ejecutas: attacker_client.py
   ↓
2. Cliente envía comando → Computadora 2:5002/attack
   ↓
3. Servidor de ataque recibe comando
   ↓
4. Se ejecuta ransomware_test.py
   ↓
5. Archivos se modifican (test.txt → test.encrypted)
   ↓
6. Monitor detecta cambios en la carpeta
   ↓
7. ML analiza features y detecta anomalía
   ↓
8. Monitor detiene proceso sospechoso
   ↓
9. Monitor envía alerta → Computadora 1:5001/event
   ↓
10. Backend guarda caso en base de datos
   ↓
11. ✅ Ataque bloqueado y registrado
```

## 🔍 Solución de Problemas

### ❌ "No se pudo conectar al agente"

**Problema:** No puedes conectar a la Computadora 2

**Solución:**
1. Verifica que el servidor de ataque esté corriendo en Computadora 2
2. Verifica la IP: `ping IP_COMPUTADORA_2`
3. Verifica firewall: Asegúrate que el puerto 5002 esté abierto
4. En Windows: Abre el puerto en el Firewall de Windows

### ❌ "El monitor no detecta cambios"

**Problema:** El monitor no reacciona al ataque

**Solución:**
1. Verifica que la carpeta monitoreada sea la misma que la del ataque
2. Verifica permisos: `ls -la /home/andres/attack_test`
3. Verifica que el monitor esté corriendo
4. Prueba crear un archivo manualmente: `touch /home/andres/attack_test/test.txt`

### ❌ "Error enviando al backend"

**Problema:** El agente no puede enviar eventos al backend

**Solución:**
1. Verifica que el backend esté corriendo en Computadora 1
2. Verifica la URL en `backend/config.py`: `BACKEND_URL`
3. Prueba la conexión: `curl http://IP_COMPUTADORA_1:5001/`
4. Verifica firewall en Computadora 1 (puerto 5001)

### ❌ "Carpeta no existe"

**Problema:** La carpeta de ataque no existe

**Solución:**
```bash
# Linux/WSL
mkdir -p /home/andres/attack_test

# Windows
mkdir C:\attack_test
```

## 📊 Ver Resultados

### Ver casos detectados:

```bash
# Desde Computadora 1
curl http://localhost:5001/cases | python -m json.tool
```

### Ver dashboard (si está configurado):

Abre el navegador en Computadora 1:
```
http://localhost:5000
# o el puerto que uses para el dashboard
```

## 🎯 Resumen Rápido

**Computadora 1 (Esta):**
```bash
# Terminal 1
python backend/server.py
```

**Computadora 2:**
```bash
# Terminal 1
python agent/monitor.py

# Terminal 2
python agent/remote_attack_server.py

# Terminal 3 (para ejecutar ataque)
python attacker_client.py localhost --port 5002 --files 10
```

## ✅ Checklist Final

- [ ] IPs configuradas en `backend/config.py` en ambas computadoras
- [ ] Carpeta de ataque creada en Computadora 2
- [ ] Backend corriendo en Computadora 1 (puerto 5001)
- [ ] Monitor corriendo en Computadora 2
- [ ] Servidor de ataque corriendo en Computadora 2 (puerto 5002)
- [ ] Conexión verificada entre ambas computadoras
- [ ] Ataque ejecutado exitosamente
- [ ] Detección observada en el monitor
- [ ] Caso guardado en el backend

¡Listo! Ahora puedes ejecutar ataques remotos y ver cómo el sistema los detecta y bloquea. 🎉

