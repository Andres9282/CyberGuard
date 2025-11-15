# 📋 PASOS EXACTOS PARA COMPUTADORA 2

Sigue estos pasos **EN ORDEN** en tu segunda computadora.

---

## ✅ PASO 1: Verificar que tienes el proyecto

Abre una terminal y verifica:

```bash
cd CyberGuard
ls
```

Debes ver carpetas como: `agent/`, `backend/`, `ml/`, etc.

---

## ✅ PASO 2: Obtener la IP de la Computadora 1

**Necesitas saber la IP de la Computadora 1 para configurar la conexión.**

### En Windows:
```cmd
ipconfig
```
Busca "IPv4 Address" - anota ese número (ejemplo: 192.168.1.50)

### En Linux/WSL:
```bash
hostname -I
```
Anota la IP que aparece (ejemplo: 192.168.1.50)

**📝 ANOTA ESTA IP: _______________**

---

## ✅ PASO 3: Configurar backend/config.py

Abre el archivo `backend/config.py` y busca estas líneas:

```python
# Línea ~14-16: Cambia esto
BACKEND_URL = os.getenv(
    "CYBERGUARD_BACKEND_URL", 
    f"http://localhost:{BACKEND_PORT}"  # ← CAMBIA ESTO
)
```

**Cámbialo por:**

```python
BACKEND_URL = os.getenv(
    "CYBERGUARD_BACKEND_URL", 
    f"http://IP_COMPUTADORA_1:5001"  # ← Pega la IP que anotaste
)
```

**Ejemplo:**
```python
BACKEND_URL = os.getenv(
    "CYBERGUARD_BACKEND_URL", 
    f"http://192.168.1.50:5001"  # ← Tu IP real
)
```

**💾 Guarda el archivo (Ctrl+S)**

---

## ✅ PASO 4: Crear carpeta de ataque

### Si estás en Linux/WSL:
```bash
mkdir -p /home/andres/attack_test
cd /home/andres/attack_test
for i in {1..5}; do echo "Archivo de prueba $i" > test_$i.txt; done
ls
```

### Si estás en Windows:
```cmd
mkdir C:\attack_test
cd C:\attack_test
for /L %i in (1,1,5) do echo Archivo de prueba %i > test_%i.txt
dir
```

Debes ver 5 archivos: `test_1.txt`, `test_2.txt`, etc.

---

## ✅ PASO 5: Verificar que Python tiene las dependencias

```bash
cd CyberGuard
py -c "import flask, requests, psutil, watchdog; print('✅ Todas las dependencias instaladas')"
```

Si sale error, instala:
```bash
py -m pip install -r requirements.txt
```

**Nota:** En Windows usa `py` en lugar de `python`. Si prefieres usar `python`, activa el entorno virtual primero con `.\venv\Scripts\Activate.ps1`

---

## ✅ PASO 6: Iniciar el Monitor (Terminal 1)

Abre una **NUEVA TERMINAL** (no cierres esta):

```bash
cd CyberGuard
py agent/monitor.py
```

**Nota:** Si `py` no funciona, activa el entorno virtual primero:
```powershell
.\venv\Scripts\Activate.ps1
python agent/monitor.py
```

**Debes ver:**
```
🔵 CyberGuard Agent iniciado...
Vigilando: /home/andres/attack_test
```

**⚠️ NO CIERRES ESTA TERMINAL - Déjala corriendo**

---

## ✅ PASO 7: Iniciar Servidor de Ataque (Terminal 2)

Abre **OTRA TERMINAL NUEVA**:

```bash
cd CyberGuard
py agent/remote_attack_server.py
```

**Nota:** Si `py` no funciona, activa el entorno virtual primero:
```powershell
.\venv\Scripts\Activate.ps1
python agent/remote_attack_server.py
```

**Debes ver:**
```
🔴 Servidor de Ataque Remoto iniciado
   Host: 0.0.0.0
   Port: 5002
   Carpeta monitoreada: /home/andres/attack_test

   Para ejecutar un ataque desde otra computadora:
   POST http://<IP_ESTA_COMPUTADORA>:5002/attack
```

**⚠️ NO CIERRES ESTA TERMINAL - Déjala corriendo**

---

## ✅ PASO 8: Verificar que todo está funcionando

Abre **OTRA TERMINAL NUEVA** (tercera terminal):

```bash
cd CyberGuard
py attacker_client.py localhost --port 5002 --status
```

**Nota:** Si `py` no funciona, activa el entorno virtual primero:
```powershell
.\venv\Scripts\Activate.ps1
python attacker_client.py localhost --port 5002 --status
```

**Debes ver:**
```
✅ Servidor de ataque disponible
   Estado: running
   Carpeta monitoreada: /home/andres/attack_test
   Carpeta existe: True
```

Si ves esto, **¡TODO ESTÁ LISTO!** ✅

---

## 🔥 PASO 9: Ejecutar el Ataque

En la misma terminal del Paso 8 (o abre una nueva):

```bash
cd CyberGuard
py attacker_client.py localhost --port 5002 --files 10 --delay 0.1
```

**Nota:** Si `py` no funciona, activa el entorno virtual primero:
```powershell
.\venv\Scripts\Activate.ps1
python attacker_client.py localhost --port 5002 --files 10 --delay 0.1
```

**Debes ver:**
```
🔴 Ejecutando ataque remoto...
   Objetivo: localhost:5002
   Archivos: 10
   Delay: 0.1s

✅ Ataque iniciado exitosamente
   Ataque iniciado
   Carpeta objetivo: /home/andres/attack_test
```

---

## 👀 PASO 10: Observar la Detección

### En Terminal 1 (Monitor):

Deberías ver algo como:

```
⚠️ Cambio detectado: /home/andres/attack_test/test_1.txt
Features extraídos: [45.2, 60.1, 25, 15]
🔥 ATAQUE DETECTADO: posible ransomware
  🔒 test_1.txt → test_1.encrypted
  🔒 test_2.txt → test_2.locked
✅ Enviado a backend → {"status": "ok", "case_id": 1, ...}
```

### En Terminal 2 (Servidor de Ataque):

Deberías ver:

```
🔥 ATAQUE REMOTO RECIBIDO
   Carpeta objetivo: /home/andres/attack_test
   Archivos: 10
   Delay: 0.1s
🔥 Iniciando simulación de ataque ransomware...
📁 Carpeta objetivo: /home/andres/attack_test
📄 Archivos a modificar: 10
  🔒 test_1.txt → test_1.encrypted
  🔒 test_2.txt → test_2.locked
  ...
✅ Ataque simulado completado: 10 archivos modificados
```

---

## ✅ VERIFICACIÓN FINAL

Si ves:
- ✅ Monitor detectando cambios
- ✅ Mensaje "ATAQUE DETECTADO"
- ✅ Archivos modificados (test_1.txt → test_1.encrypted)
- ✅ Mensaje "Enviado a backend"

**¡TODO FUNCIONA CORRECTAMENTE!** 🎉

---

## 🐛 Si algo no funciona:

### Error: "No se pudo conectar al backend"

1. Verifica que la Computadora 1 tenga el backend corriendo
2. Verifica la IP en `backend/config.py`
3. Prueba: `ping IP_COMPUTADORA_1`

### Error: "Carpeta no existe"

```bash
# Linux/WSL
mkdir -p /home/andres/attack_test

# Windows
mkdir C:\attack_test
```

### Error: "Puerto 5002 en uso"

Cierra otros programas que usen el puerto 5002, o cambia el puerto en `backend/config.py`

---

## 📞 Resumen de lo que debe estar corriendo:

- ✅ **Terminal 1**: `python agent/monitor.py` (corriendo)
- ✅ **Terminal 2**: `python agent/remote_attack_server.py` (corriendo)
- ✅ **Terminal 3**: Para ejecutar comandos (ataques, verificaciones)

**¡Listo! Ahora puedes ejecutar ataques y ver cómo se detectan!** 🚀

