"""
Solución rápida: Prueba si 127.0.0.1 funciona mejor que localhost
"""

import psycopg2
from pathlib import Path

print("="*70)
print("SOLUCIÓN RÁPIDA: Probando 127.0.0.1 vs localhost")
print("="*70)
print()

DB_CONFIG = {
    'database': 'CAMPO_MAN_COGNITIVO',
    'user': 'postgres',
    'password': 'Admin',
    'port': '5432'
}

# Probar ambos hosts
hosts = ['localhost', '127.0.0.1']
working_host = None

for host in hosts:
    print(f"🔄 Probando con: {host}")
    
    try:
        config = DB_CONFIG.copy()
        config['host'] = host
        
        connection = psycopg2.connect(**config, connect_timeout=3)
        
        print(f"✅ ¡FUNCIONA con {host}!")
        
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"   PostgreSQL: {version[0][:60]}...")
        cursor.close()
        connection.close()
        
        working_host = host
        break
        
    except Exception as e:
        print(f"❌ Falla con {host}: {str(e)[:80]}")
        print()

print()
print("="*70)

if working_host:
    print(f"✅ SOLUCIÓN ENCONTRADA: Usa DB_HOST={working_host}")
    print("="*70)
    print()
    
    # Leer .env actual
    env_path = Path(__file__).parent / '.env'
    
    if env_path.exists():
        print("🔧 Actualizando tu archivo .env...")
        
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Actualizar DB_HOST
        updated = False
        new_lines = []
        for line in lines:
            if line.strip().startswith('DB_HOST='):
                new_lines.append(f'DB_HOST={working_host}\n')
                updated = True
            else:
                new_lines.append(line)
        
        # Si no encontramos DB_HOST, agregarlo
        if not updated:
            new_lines.append(f'DB_HOST={working_host}\n')
        
        # Guardar
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f"✅ Archivo .env actualizado con DB_HOST={working_host}")
        print()
        print("🚀 Ahora ejecuta:")
        print("   python manage.py migrate")
        print()
    else:
        print("⚠️  No se encontró archivo .env")
        print()
        print("Edita manualmente tu .env y agrega:")
        print(f"   DB_HOST={working_host}")
        print()
else:
    print("❌ NO SE ENCONTRÓ SOLUCIÓN")
    print("="*70)
    print()
    print("PostgreSQL no es accesible desde ningún host.")
    print()
    print("Problemas posibles:")
    print("   1. PostgreSQL no está corriendo")
    print("   2. Configuración de pg_hba.conf incorrecta")
    print("   3. Firewall bloqueando")
    print()
    print("Ejecuta estos comandos de diagnóstico:")
    print()
    print("   docker-compose ps")
    print("   docker logs campos_maniobras_db --tail 20")
    print("   docker exec campos_maniobras_db psql -U postgres -c 'SHOW listen_addresses;'")
    print()

print("="*70)
