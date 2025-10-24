"""
Script para verificar la configuración que Django está leyendo
"""

import os
import sys
from pathlib import Path

# Configurar el path de Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

print("="*60)
print("VERIFICACIÓN DE CONFIGURACIÓN DJANGO")
print("="*60)
print()

# 1. Verificar ubicación del .env
env_path = BASE_DIR / '.env'
print(f"📁 Directorio actual: {BASE_DIR}")
print(f"📄 Buscando .env en: {env_path}")
print(f"   ¿Existe? {env_path.exists()}")
print()

if env_path.exists():
    print("✅ Archivo .env encontrado")
    print()
    print("📋 Contenido del .env:")
    print("-" * 60)
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            # Ocultar contraseñas
            if 'PASSWORD' in line.upper() and '=' in line:
                parts = line.split('=', 1)
                if len(parts) == 2:
                    print(f"{i:2d}: {parts[0]}=*****")
                else:
                    print(f"{i:2d}: {line.rstrip()}")
            else:
                print(f"{i:2d}: {line.rstrip()}")
    print("-" * 60)
    print()
else:
    print("❌ Archivo .env NO encontrado")
    print()
    print("Solución:")
    print("   1. Asegúrate de que .env está en:")
    print(f"      {env_path}")
    print()
    print("   2. O copia .env.example a .env:")
    print("      copy .env.example .env")
    sys.exit(1)

# 2. Leer configuración con decouple
print("🔧 Leyendo configuración con python-decouple...")
print()

try:
    from decouple import config
    
    db_engine = config('DB_ENGINE', default='NO_ENCONTRADO')
    db_name = config('DB_NAME', default='NO_ENCONTRADO')
    db_user = config('DB_USER', default='NO_ENCONTRADO')
    db_password = config('DB_PASSWORD', default='NO_ENCONTRADO')
    db_host = config('DB_HOST', default='NO_ENCONTRADO')
    db_port = config('DB_PORT', default='NO_ENCONTRADO')
    
    print("Valores leídos por decouple:")
    print(f"   DB_ENGINE: {db_engine}")
    print(f"   DB_NAME: {db_name}")
    print(f"   DB_USER: {db_user}")
    print(f"   DB_PASSWORD: {'*' * len(str(db_password))} ({len(str(db_password))} caracteres)")
    print(f"   DB_HOST: {db_host}")
    print(f"   DB_PORT: {db_port}")
    print()
    
    # Verificar si algún valor está en "NO_ENCONTRADO"
    if 'NO_ENCONTRADO' in [db_engine, db_name, db_user, db_host, db_port]:
        print("⚠️  ADVERTENCIA: Algunos valores no se encontraron en .env")
        print("   Usando valores por defecto")
        print()
    
    if db_password == 'NO_ENCONTRADO':
        print("❌ ERROR: DB_PASSWORD no está definido en .env")
        print()
        print("Solución:")
        print("   Agrega esta línea a tu .env:")
        print("   DB_PASSWORD=Admin")
        sys.exit(1)
    
except Exception as e:
    print(f"❌ Error leyendo configuración: {e}")
    sys.exit(1)

# 3. Intentar cargar la configuración de Django
print("⚙️  Cargando configuración de Django...")
print()

try:
    import django
    django.setup()
    
    from django.conf import settings
    
    print("✅ Django configurado correctamente")
    print()
    print("Configuración de base de datos en Django:")
    db_config = settings.DATABASES['default']
    print(f"   ENGINE: {db_config.get('ENGINE', 'NO_DEFINIDO')}")
    print(f"   NAME: {db_config.get('NAME', 'NO_DEFINIDO')}")
    print(f"   USER: {db_config.get('USER', 'NO_DEFINIDO')}")
    password = db_config.get('PASSWORD', 'NO_DEFINIDO')
    print(f"   PASSWORD: {'*' * len(str(password))} ({len(str(password))} caracteres)")
    print(f"   HOST: {db_config.get('HOST', 'NO_DEFINIDO')}")
    print(f"   PORT: {db_config.get('PORT', 'NO_DEFINIDO')}")
    print()
    
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    import traceback
    print()
    print("Traceback completo:")
    print(traceback.format_exc())
    sys.exit(1)

# 4. Intentar conexión a la base de datos
print("🔄 Intentando conectar a PostgreSQL...")
print()

try:
    from django.db import connection
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("✅ ¡CONEXIÓN EXITOSA!")
        print()
        print(f"PostgreSQL version:")
        print(f"   {version[0][:80]}...")
        print()
        
        cursor.execute("SELECT current_database(), current_user;")
        db_info = cursor.fetchone()
        print(f"Base de datos: {db_info[0]}")
        print(f"Usuario: {db_info[1]}")
        
except Exception as e:
    print(f"❌ ERROR DE CONEXIÓN")
    print()
    print(f"Tipo de error: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    print()
    
    error_msg = str(e).lower()
    
    if 'password authentication failed' in error_msg:
        print("🔐 Problema de AUTENTICACIÓN")
        print()
        print("La contraseña es incorrecta.")
        print()
        print("Verifica:")
        print("   1. Tu .env dice: DB_PASSWORD=Admin")
        print("   2. Docker dice: POSTGRES_PASSWORD=Admin")
        print()
        print("Si son diferentes, cámbialos para que coincidan.")
        
    elif 'database' in error_msg and 'does not exist' in error_msg:
        print("🗄️  La BASE DE DATOS no existe")
        print()
        print("Solución:")
        print("   docker exec -it campos_maniobras_db psql -U postgres")
        print('   CREATE DATABASE "CAMPO_MAN_COGNITIVO";')
        
    elif 'could not connect' in error_msg:
        print("🔌 NO SE PUEDE CONECTAR al servidor")
        print()
        print("Verifica:")
        print("   1. Docker está corriendo: docker-compose ps")
        print("   2. Puerto mapeado: docker port campos_maniobras_db")
        
    else:
        print("❓ Error desconocido")
        print()
        import traceback
        print("Traceback completo:")
        print(traceback.format_exc())

print()
print("="*60)
