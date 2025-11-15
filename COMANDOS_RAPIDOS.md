# 🚀 Comandos Rápidos - CyberGuard

## 📍 Antes de Empezar

### Obtener tu IP:
```bash
# Windows
ipconfig

# Linux/WSL
hostname -I
```

### Verificar configuración:
```bash
python verificar_configuracion.py
```

---

## 🖥️ COMPUTADORA 1 (Esta - Servidor)

### Iniciar Backend:
```bash
python backend/server.py
```

### Verificar que está corriendo:
```bash
curl http://localhost:5001/
```

### Ver casos detectados:
```bash
curl http://localhost:5001/cases
```

---

## 🖥️ COMPUTADORA 2 (Cliente - Agente)

### Preparar carpeta de ataque:
```bash
# Linux/WSL
mkdir -p /home/andres/attack_test
cd /home/andres/attack_test
for i in {1..5}; do echo "Test $i" > test_$i.txt; done

# Windows
mkdir C:\attack_test
cd C:\attack_test
for /L %i in (1,1,5) do echo Test %i > test_%i.txt
```

### Iniciar Monitor (Terminal 1):
```bash
python agent/monitor.py
```

### Iniciar Servidor de Ataque (Terminal 2):
```bash
python agent/remote_attack_server.py
```

### Verificar servidor de ataque:
```bash
python attacker_client.py localhost --port 5002 --status
```

### Ejecutar ataque:
```bash
python attacker_client.py localhost --port 5002 --files 10 --delay 0.1
```

---

## 🔥 Ejecutar Ataque Remoto

### Opción 1: Desde Computadora 2 (Directo)
```bash
python attacker_client.py localhost --port 5002 --files 10
```

### Opción 2: Desde Computadora 1 (vía Backend)
```bash
curl -X POST http://localhost:5001/trigger-attack \
  -H "Content-Type: application/json" \
  -d '{"agent_ip": "IP_COMPUTADORA_2", "agent_port": 5002, "num_files": 10}'
```

### Opción 3: Desde otra computadora
```bash
python attacker_client.py IP_COMPUTADORA_2 --port 5002 --files 10
```

---

## 🔍 Verificar Estado

### Verificar Backend:
```bash
curl http://localhost:5001/
```

### Verificar Servidor de Ataque:
```bash
curl http://localhost:5002/status
```

### Ver casos en base de datos:
```bash
curl http://localhost:5001/cases | python -m json.tool
```

---

## ⚙️ Configuración

### Editar IPs en `backend/config.py`:

**Computadora 1:**
```python
AGENT_IP = "192.168.1.XXX"  # IP de Computadora 2
BACKEND_URL = "http://TU_IP:5001"  # Tu IP
```

**Computadora 2:**
```python
BACKEND_URL = "http://IP_COMPUTADORA_1:5001"  # IP de Computadora 1
```

---

## 🐛 Solución Rápida de Problemas

### Backend no responde:
```bash
# Verificar que esté corriendo
netstat -an | findstr 5001  # Windows
netstat -an | grep 5001     # Linux
```

### Servidor de ataque no responde:
```bash
# Verificar que esté corriendo
netstat -an | findstr 5002  # Windows
netstat -an | grep 5002     # Linux
```

### No se puede conectar:
```bash
# Verificar conectividad
ping IP_COMPUTADORA_2  # Desde Computadora 1
ping IP_COMPUTADORA_1  # Desde Computadora 2
```

---

## 📚 Documentación Completa

- **Tutorial detallado:** `TUTORIAL_ATAQUE_REMOTO.md`
- **Inicio rápido:** `INICIO_RAPIDO.txt`
- **Setup remoto:** `REMOTE_ATTACK_SETUP.md`

