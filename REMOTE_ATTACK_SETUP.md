# Configuración de Ataque Remoto - CyberGuard

Este documento explica cómo configurar y ejecutar simulaciones de ataque desde una segunda computadora.

## Arquitectura

El sistema está compuesto por:

1. **Computadora 1 (Servidor)**: 
   - Backend (`backend/server.py`) - Puerto 5001
   - Recibe eventos del agente y puede disparar ataques remotos

2. **Computadora 2 (Cliente/Agente)**:
   - Monitor (`agent/monitor.py`) - Monitorea carpetas y detecta ataques
   - Servidor de Ataque Remoto (`agent/remote_attack_server.py`) - Puerto 5002
   - Recibe comandos de ataque y los ejecuta localmente

## Configuración

### 1. Configurar Variables de Entorno (Opcional)

Puedes configurar las siguientes variables de entorno o modificar `backend/config.py`:

```bash
# En Computadora 1 (Servidor)
export CYBERGUARD_BACKEND_HOST="0.0.0.0"
export CYBERGUARD_BACKEND_PORT="5001"

# En Computadora 2 (Agente)
export CYBERGUARD_AGENT_HOST="0.0.0.0"
export CYBERGUARD_AGENT_PORT="5002"
export CYBERGUARD_WATCH_FOLDER="/home/andres/attack_test"  # Linux/WSL
# o
export CYBERGUARD_WATCH_FOLDER="C:\\attack_test"  # Windows
export CYBERGUARD_BACKEND_URL="http://<IP_COMPUTADORA_1>:5001/event"
```

### 2. Modificar config.py (Alternativa)

Edita `backend/config.py` y actualiza las IPs según tu red:

```python
# IP de la computadora donde está el agente
AGENT_IP = "192.168.1.100"  # Cambiar por la IP real

# URL del backend para que el agente se conecte
BACKEND_URL = "http://192.168.1.50:5001"  # Cambiar por la IP del servidor
```

## Uso

### Paso 1: Iniciar el Backend (Computadora 1)

```bash
cd CyberGuard
python backend/server.py
```

Deberías ver:
```
🔵 CyberGuard Backend iniciado
   Host: 0.0.0.0
   Port: 5001
```

### Paso 2: Iniciar el Monitor y Servidor de Ataque (Computadora 2)

En la computadora 2, ejecuta dos procesos:

**Terminal 1 - Monitor:**
```bash
cd CyberGuard
python agent/monitor.py
```

**Terminal 2 - Servidor de Ataque Remoto:**
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
```

### Paso 3: Ejecutar Ataque desde Computadora 2 (Directo)

Desde la computadora 2, puedes ejecutar el ataque directamente:

```bash
# Verificar estado del servidor
python attacker_client.py <IP_COMPUTADORA_2> --port 5002 --status

# Ejecutar ataque
python attacker_client.py <IP_COMPUTADORA_2> --port 5002 --files 10 --delay 0.1
```

### Paso 4: Ejecutar Ataque desde Computadora 1 (Remoto)

Desde la computadora 1, puedes disparar un ataque remoto:

**Opción A: Usando curl**
```bash
curl -X POST http://localhost:5001/trigger-attack \
  -H "Content-Type: application/json" \
  -d '{
    "agent_ip": "<IP_COMPUTADORA_2>",
    "agent_port": 5002,
    "num_files": 10,
    "delay": 0.1
  }'
```

**Opción B: Usando Python**
```python
import requests

response = requests.post(
    "http://localhost:5001/trigger-attack",
    json={
        "agent_ip": "<IP_COMPUTADORA_2>",
        "agent_port": 5002,
        "num_files": 10,
        "delay": 0.1
    }
)
print(response.json())
```

**Opción C: Desde otra computadora (tercera)**
```bash
python attacker_client.py <IP_COMPUTADORA_2> --port 5002 --files 15
```

## Flujo de Ataque

1. **Cliente ejecuta ataque** → `attacker_client.py` o `POST /trigger-attack`
2. **Servidor de ataque recibe comando** → `agent/remote_attack_server.py` en puerto 5002
3. **Script de ataque se ejecuta** → `agent/ransomware_test.py` modifica archivos
4. **Monitor detecta cambios** → `agent/monitor.py` detecta modificaciones
5. **Detección de anomalía** → ML detecta comportamiento sospechoso
6. **Evento enviado al backend** → `backend/server.py` recibe alerta
7. **Caso creado en BD** → Se guarda evidencia del ataque

## Parámetros del Ataque

- `num_files`: Número de archivos a modificar (default: 10)
- `delay`: Retraso entre modificaciones en segundos (default: 0.1)
- `target_folder`: Carpeta objetivo (opcional, usa la configurada por defecto)

## Solución de Problemas

### Error: "No se pudo conectar al agente"

1. Verifica que el servidor de ataque esté ejecutándose en la computadora 2:
   ```bash
   python agent/remote_attack_server.py
   ```

2. Verifica la conectividad de red:
   ```bash
   ping <IP_COMPUTADORA_2>
   ```

3. Verifica que el firewall permita conexiones en el puerto 5002

### Error: "Carpeta no existe"

1. Crea la carpeta objetivo:
   ```bash
   mkdir -p /home/andres/attack_test  # Linux/WSL
   # o
   mkdir C:\attack_test  # Windows
   ```

2. O especifica otra carpeta en el comando de ataque:
   ```bash
   python attacker_client.py <IP> --folder /ruta/alternativa
   ```

### El monitor no detecta cambios

1. Verifica que el monitor esté ejecutándose
2. Verifica que la carpeta monitoreada sea la misma que la del ataque
3. Verifica permisos de lectura/escritura en la carpeta

## Notas de Seguridad

⚠️ **ADVERTENCIA**: Este sistema es solo para pruebas y simulaciones en entornos controlados. No usar en producción sin las medidas de seguridad apropiadas.

- Los endpoints de ataque no tienen autenticación por defecto
- Considera agregar autenticación para entornos de producción
- Limita el acceso a los puertos 5001 y 5002 mediante firewall

