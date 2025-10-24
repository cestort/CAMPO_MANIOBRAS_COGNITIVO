"""
Script de prueba de conexión a PostgreSQL
Ejecuta este script para verificar que tu configuración de base de datos es correcta
"""

import sys
import os

# Añadir el directorio actual al path para importar decouple
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from decouple import config
    print("✅ python-decouple importado correctamente")
except ImportError:
    print("❌ Error: python-decouple no está instalado")
    print("Instala con: pip install python-decouple")
    sys.exit(1)

try:
    import psycopg2
    print("✅ psycopg2 importado correctamente")
except ImportError:
    print("❌ Error: psycopg2 no está instalado")
    print("Instala con: pip install psycopg2-binary")
    sys.exit(1)

print("\n" + "="*60)
print("PRUEBA DE CONEXIÓN A POSTGRESQL")
print("="*60 + "\n")

# Leer configuración del archivo .env
try:
    db_name = config('DB_NAME')
    db_user = config('DB_USER')
    db_password = config('DB_PASSWORD')
    db_host = config('DB_HOST')
    db_port = config('DB_PORT')
    
    print("📋 Configuración leída desde .env:")
    print(f"   DB_NAME: {db_name}")
    print(f"   DB_USER: {db_user}")
    print(f"   DB_PASSWORD: {'*' * len(db_password)} (oculta)")
    print(f"   DB_HOST: {db_host}")
    print(f"   DB_PORT: {db_port}")
    print()
    
except Exception as error:
    print("❌ Error al leer el archivo .env:")
    print(f"   {error}")
    print("\n💡 Asegúrate de que:")
    print("   1. El archivo .env existe en el directorio BACKEND")
    print("   2. Tiene todas las variables configuradas (DB_NAME, DB_USER, etc.)")
    sys.exit(1)

# Intentar conectar a PostgreSQL
print("🔄 Intentando conectar a PostgreSQL...")
print()

try:
    connection = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    
    print("✅ ¡CONEXIÓN EXITOSA!")
    print()
    
    # Obtener información de la base de datos
    cursor = connection.cursor()
    
    # Versión de PostgreSQL
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"📊 Versión de PostgreSQL:")
    print(f"   {version[0]}")
    print()
    
    # Usuario actual
    cursor.execute("SELECT current_user;")
    current_user = cursor.fetchone()
    print(f"👤 Usuario conectado: {current_user[0]}")
    
    # Base de datos actual
    cursor.execute("SELECT current_database();")
    current_db = cursor.fetchone()
    print(f"🗄️  Base de datos: {current_db[0]}")
    print()
    
    # Listar tablas (si existen)
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    
    if tables:
        print(f"📋 Tablas existentes en la base de datos:")
        for table in tables:
            print(f"   - {table[0]}")
    else:
        print("📋 No hay tablas en la base de datos (normal si no has ejecutado migraciones)")
    
    print()
    print("="*60)
    print("✅ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
    print("="*60)
    print()
    print("🚀 Siguiente paso: Ejecuta las migraciones")
    print("   python manage.py migrate")
    print()
    
    cursor.close()
    connection.close()
    
except psycopg2.OperationalError as error:
    print("❌ ERROR DE CONEXIÓN:")
    print()
    error_msg = str(error)
    
    # Analizar el tipo de error y dar sugerencias específicas
    if "authentication failed" in error_msg.lower():
        print("🔐 Problema de autenticación")
        print()
        print("Causas posibles:")
        print("   1. La contraseña en .env es incorrecta")
        print("   2. El usuario no existe")
        print()
        print("Soluciones:")
        print("   1. Verifica DB_PASSWORD en tu archivo .env")
        print("   2. Prueba conectarte manualmente:")
        print(f"      psql -U {db_user} -h {db_host} -p {db_port}")
        
    elif "does not exist" in error_msg.lower() and "database" in error_msg.lower():
        print("🗄️  La base de datos no existe")
        print()
        print("Solución:")
        print("   1. Conéctate a PostgreSQL:")
        print(f"      psql -U {db_user} -h {db_host} -p {db_port}")
        print()
        print("   2. Crea la base de datos:")
        print(f"      CREATE DATABASE {db_name};")
        print()
        print("   3. Vuelve a ejecutar este script")
        
    elif "could not connect" in error_msg.lower() or "connection refused" in error_msg.lower():
        print("🔌 No se puede conectar al servidor PostgreSQL")
        print()
        print("Causas posibles:")
        print("   1. PostgreSQL no está corriendo")
        print("   2. Puerto o host incorrectos")
        print()
        print("Soluciones:")
        print("   1. Verifica que PostgreSQL esté corriendo:")
        print("      Windows: Get-Service -Name postgresql*")
        print()
        print("   2. Verifica el puerto:")
        print("      netstat -an | findstr 5432")
        print()
        print("   3. Inicia PostgreSQL si está detenido:")
        print("      Start-Service postgresql-x64-XX")
        
    else:
        print("Error desconocido:")
        print(f"   {error}")
    
    print()
    print("="*60)
    print("💡 Consulta SOLUCION_ERROR_POSTGRESQL.md para más ayuda")
    print("="*60)
    sys.exit(1)
    
except Exception as error:
    print("❌ ERROR INESPERADO:")
    print(f"   {error}")
    print()
    print("💡 Consulta SOLUCION_ERROR_POSTGRESQL.md para más ayuda")
    sys.exit(1)
