# 🔧 Solución: Error "python no reconocido"

## ✅ Solución Rápida

En Windows, tienes **2 opciones**:

---

## Opción 1: Usar `py` en lugar de `python` ⭐ RECOMENDADO

En lugar de:
```bash
python backend/server.py
```

Usa:
```bash
py backend/server.py
```

---

## Opción 2: Activar el Entorno Virtual

1. Activa el entorno virtual primero:
```powershell
.\venv\Scripts\Activate.ps1
```

2. Luego usa `python` normalmente:
```bash
python backend/server.py
```

---

## 📋 Comandos Corregidos para Este Proyecto

### Iniciar Backend:
```bash
py backend/server.py
```

### Iniciar Monitor (en Computadora 2):
```bash
py agent/monitor.py
```

### Iniciar Servidor de Ataque (en Computadora 2):
```bash
py agent/remote_attack_server.py
```

### Ejecutar Cliente de Ataque:
```bash
py attacker_client.py localhost --port 5002 --files 10
```

---

## ✅ Verificar que Funciona

Prueba:
```bash
py --version
```

Deberías ver: `Python 3.11.9` (o similar)

---

## 💡 Nota

Si prefieres usar `python` siempre, puedes:
1. Activar el entorno virtual cada vez que abras una terminal
2. O agregar Python al PATH del sistema (más complejo)

**La forma más fácil es usar `py` en lugar de `python`** ✅

