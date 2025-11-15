#!/usr/bin/env python
# Script de prueba para verificar que el servidor funciona
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from app_integrated import app
    print("✅ App importada correctamente")
    
    # Verificar rutas
    with app.test_client() as client:
        print("\n🔍 Probando rutas...")
        
        # Probar ruta principal
        response = client.get('/')
        print(f"   GET / -> {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Página principal carga correctamente")
        else:
            print(f"   ❌ Error: {response.status_code}")
        
        # Probar API status
        response = client.get('/api/status')
        print(f"   GET /api/status -> {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Status: {data.get('status', 'N/A')}")
        else:
            print(f"   ❌ Error: {response.status_code}")
        
        # Probar API cases
        response = client.get('/api/cases')
        print(f"   GET /api/cases -> {response.status_code}")
        if response.status_code == 200:
            data = response.get_json()
            cases_count = len(data) if isinstance(data, list) else 0
            print(f"   ✅ Casos encontrados: {cases_count}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    
    print("\n✅ Todas las pruebas completadas")
    print("\n💡 Para iniciar el servidor, ejecuta:")
    print("   python dashboard/app_integrated.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

