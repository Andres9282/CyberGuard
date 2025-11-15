# 🚀 Cómo Iniciar el Dashboard

## Paso 1: Verificar que estás en el directorio correcto

```powershell
cd C:\Users\danie\OneDrive\Desktop\CyberGuard
```

## Paso 2: Iniciar el Dashboard

```powershell
python dashboard/app_integrated.py
```

**O si usas el entorno virtual:**

```powershell
.\venv\Scripts\Activate.ps1
python dashboard/app_integrated.py
```

## Paso 3: Abrir en el navegador

Una vez que veas este mensaje:
```
🚀 CyberGuard SV - Sistema REAL
📊 Dashboard: http://localhost:5001
```

Abre tu navegador y ve a:
```
http://localhost:5001
```

## ⚠️ Si no muestra nada:

1. **Abre la consola del navegador** (F12) y revisa si hay errores
2. **Verifica que el servidor esté corriendo** - deberías ver mensajes en la terminal
3. **Revisa la URL** - debe ser `http://localhost:5001` (no 5000)
4. **Verifica que no haya otro proceso usando el puerto 5001**

## 🔍 Verificar que funciona:

Abre otra terminal y prueba:
```powershell
curl http://localhost:5001/api/status
```

O en el navegador ve a:
```
http://localhost:5001/api/status
```

Deberías ver un JSON con el estado del sistema.

## 📝 Notas:

- El dashboard corre en el puerto **5001** por defecto
- Si quieres usar otro puerto, establece la variable de entorno: `$env:PORT=5000`
- El dashboard se actualiza automáticamente cada 3 segundos

