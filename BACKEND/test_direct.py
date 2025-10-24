"""
Prueba de conexión DIRECTA a PostgreSQL sin usar .env
Para descartar problemas con decouple
"""

import psycopg2

print("="*60)
print("PRUEBA DE CONEXIÓN DIRECTA (sin .env)")
print("="*60)
print()

# Valores hardcodeados basados en tu docker-compose.yml
DB_CONFIG = {
    'database': 'CAMPO_MAN_COGNITIVO',
    'user': 'postgres',
    'password': 'Admin',
    'host': 'localhost',
    'port': '5432'
}

print("📋 Configuración de conexión:")
print(f"   Database: {DB_CONFIG['database']}")
print(f"   User: {DB_CONFIG['user']}")
print(f"   Password: {'*' * len(DB_CONFIG['password'])}")
print(f"   Host: {DB_CONFIG['host']}")
print(f"   Port: {DB_CONFIG['port']}")
print()

print("🔄 Intentando conectar...")
print()

try:
    connection = psycopg2.connect(**DB_CONFIG)
    
    print("✅ ¡CONEXIÓN EXITOSA!")
    print()
    
    cursor = connection.cursor()
    
    # Información de la conexión
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"📊 PostgreSQL: {version[0][:80]}...")
    print()
    
    cursor.execute("SELECT current_database(), current_user;")
    info = cursor.fetchone()
    print(f"🗄️  Base de datos: {info[0]}")
    print(f"👤 Usuario: {info[1]}")
    print()
    
    cursor.close()
    connection.close()
    
    print("="*60)
    print("✅ LA CONEXIÓN FUNCIONA")
    print("="*60)
    print()
    print("Esto significa que:")
    print("   ✅ PostgreSQL está funcionando correctamente")
    print("   ✅ Las credenciales son correctas")
    print("   ✅ La base de datos existe")
    print()
    print("❓ El problema debe estar en:")
    print("   1. El archivo .env no existe o está en el lugar equivocado")
    print("   2. El archivo .env tiene formato incorrecto")
    print("   3. Python-decouple no está leyendo correctamente el .env")
    print()
    print("🔧 SOLUCIÓN:")
    print("   Ejecuta: python check_config.py")
    print("   Ese script te dirá exactamente qué está leyendo Django")
    
except psycopg2.OperationalError as e:
    print("❌ ERROR DE CONEXIÓN")
    print()
    print(f"Mensaje: {e}")
    print()
    
    error_msg = str(e).lower()
    
    if 'authentication failed' in error_msg:
        print("🔐 PROBLEMA: Contraseña incorrecta")
        print()
        print("La contraseña 'Admin' no es correcta.")
        print()
        print("Verifica tu .env de Docker:")
        print("   POSTGRES_PASSWORD=???")
        
    elif 'database' in error_msg and 'does not exist' in error_msg:
        print("🗄️  PROBLEMA: Base de datos no existe")
        print()
        print("Créala con:")
        print("   docker exec -it campos_maniobras_db psql -U postgres")
        print('   CREATE DATABASE "CAMPO_MAN_COGNITIVO";')
        
    elif 'could not connect' in error_msg:
        print("🔌 PROBLEMA: No se puede conectar")
        print()
        print("Verifica:")
        print("   docker-compose ps")
        print("   docker port campos_maniobras_db")
    
    print()
    print("="*60)

except Exception as e:
    print(f"❌ ERROR INESPERADO: {e}")
    import traceback
    print()
    print(traceback.format_exc())
