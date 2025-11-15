# 📋 PASOS EXACTOS PARA COMPUTADORA 1 (ESTA)

Sigue estos pasos **EN ORDEN** en esta computadora.

---

## ✅ PASO 1: Obtener tu IP local

Abre PowerShell o CMD:

```cmd
ipconfig
```

Busca "IPv4 Address" en tu adaptador de red activo.

**📝 ANOTA TU IP: _______________**

**Ejemplo:** 192.168.1.50

---

## ✅ PASO 2: Configurar backend/config.py

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
    f"http://TU_IP:5001"  # ← Pega TU IP (la que anotaste arriba)
)
```

**Ejemplo:**
```python
BACKEND_URL = os.getenv(
    "CYBERGUARD_BACKEND_URL", 
    f"http://192.168.1.50:5001"  # ← Tu IP real
)
```

**También configura la IP del agente (Computadora 2):**

Busca la línea ~34:
```python
AGENT_IP = os.getenv("CYBERGUARD_AGENT_IP", "localhost")
```

**Cámbiala por la IP de la Computadora 2:**
```python
AGENT_IP = os.getenv("CYBERGUARD_AGENT_IP", "192.168.1.XXX")  # ← IP de Computadora 2
```

**💾 Guarda el archivo (Ctrl+S)**

---

## ✅ PASO 3: Verificar que Python tiene las dependencias

Abre una terminal en la carpeta del proyecto:

```bash
cd CyberGuard
py -c "import flask, requests; print('✅ Dependencias OK')"
```

Si sale error:
```bash
py -m pip install -r requirements.txt
```

**Nota:** En Windows usa `py` en lugar de `python`. Si prefieres usar `python`, activa el entorno virtual primero con `.\venv\Scripts\Activate.ps1`

---

## ✅ PASO 4: Iniciar el Backend

Abre una terminal:

```bash
cd CyberGuard
python3 -m backend.server

```

**Nota:** Si `py` no funciona, activa el entorno virtual primero:
```powershell
.\venv\Scripts\Activate.ps1
python backend/server.py
```

**Debes ver:**
```
🔵 CyberGuard Backend iniciado
   Host: 0.0.0.0
   Port: 5001
 * Running on http://0.0.0.0:5001
```

**⚠️ NO CIERRES ESTA TERMINAL - Déjala corriendo**

---

## ✅ PASO 5: Verificar que el Backend responde

Abre **OTRA TERMINAL NUEVA**:

```bash
curl http://localhost:5001/
```

**Debes ver:**
```
CyberGuard Backend OK
```

Si no tienes `curl`, usa Python:
```python
import requests
response = requests.get("http://localhost:5001/")
print(response.text)
```

---

## ✅ PASO 6: Esperar a que Computadora 2 esté lista

**Ahora ve a la Computadora 2 y sigue los pasos en `PASOS_COMPUTADORA_2.md`**

Espera a que en la Computadora 2:
- ✅ El monitor esté corriendo
- ✅ El servidor de ataque esté corriendo

---

## ✅ PASO 7: Verificar conexión con Computadora 2

En una nueva terminal:

```bash
# Reemplaza IP_COMPUTADORA_2 con la IP real
ping IP_COMPUTADORA_2
```

Debe responder. Si no, verifica que ambas estén en la misma red.

---

## ✅ PASO 8: Observar cuando llegue el ataque

Cuando se ejecute el ataque en la Computadora 2, en la terminal del Backend (Paso 4) deberías ver:

```
127.0.0.1 - - [2024-XX-XX XX:XX:XX] "POST /event HTTP/1.1" 200 -
```

Esto significa que el agente detectó el ataque y lo reportó.

---

## ✅ PASO 9: Ver casos detectados

En una nueva terminal:

```bash
curl http://localhost:5001/cases
```

O con Python:
```python
import requests
response = requests.get("http://localhost:5001/cases")
print(response.json())
```

Deberías ver los casos de ataques detectados.

---

## ✅ VERIFICACIÓN FINAL

**En esta computadora debe estar corriendo:**
- ✅ Backend en puerto 5001
- ✅ Terminal del backend abierta y mostrando logs

**Cuando Computadora 2 ejecute un ataque:**
- ✅ Deberías ver logs en la terminal del backend
- ✅ Los casos se guardan en la base de datos
- ✅ Puedes verlos con `curl http://localhost:5001/cases`

**¡TODO LISTO!** 🎉

---

## 🐛 Si algo no funciona:

### Error: "Address already in use"

Algo más está usando el puerto 5001. Cierra otros programas o cambia el puerto en `backend/config.py`

### Error: "No module named 'flask'"

```bash
pip install flask requests
```

### El backend no recibe eventos

1. Verifica que la IP en Computadora 2 sea correcta
2. Verifica que el firewall permita conexiones en puerto 5001
3. Prueba: `ping IP_COMPUTADORA_2`

---

## 📞 Resumen:

- ✅ **Terminal 1**: `python backend/server.py` (corriendo)
- ✅ **Terminal 2**: Para verificar y ejecutar comandos

**¡Listo! Ahora espera a que Computadora 2 esté configurada!** 🚀

