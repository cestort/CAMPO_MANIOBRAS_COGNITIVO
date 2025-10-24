# 🚀 BASE_DATOS - Conexión Automática pgAdmin

## 📋 Descripción

Configuración completa de PostgreSQL + pgAdmin con **conexión automática**.

Al abrir pgAdmin, el servidor PostgreSQL ya estará conectado y listo para usar. Sin configuración manual.

---

## 📁 Estructura de Archivos

```
BASE_DATOS/
├── docker-compose.yml          # Servicios: PostgreSQL + pgAdmin
├── .env                        # Variables de entorno
├── servers.json                # Configuración del servidor para pgAdmin
├── pgpassfile                  # Credenciales (NO subir a Git)
├── pgpassfile.example          # Plantilla de credenciales
├── .gitignore                  # Protege archivos sensibles
├── iniciar_servicios.bat       # Ejecutable para iniciar servicios
├── backups/                    # Carpeta para backups SQL
└── CONEXION_AUTOMATICA.md      # Documentación detallada
```

---

## 🚀 Inicio Rápido

### 1. Verificar configuración

Revisa el archivo `.env` con tus credenciales:

```env
TZ=Europe/Madrid
POSTGRES_USER=postgres
POSTGRES_PASSWORD=Admin
POSTGRES_DB=PRUEBAS
PGADMIN_DEFAULT_EMAIL=CAEI@caei.com
PGADMIN_DEFAULT_PASSWORD=U5u4r10_C431
PORT_PGADMIN=5050
```

### 2. Iniciar servicios

```bash
.\iniciar_servicios.bat
```

O manualmente:
```bash
docker-compose up -d
```

### 3. Acceder a pgAdmin

Abre en tu navegador: `http://localhost:5050`

**Credenciales de pgAdmin:**
- Email: `CAEI@caei.com`
- Password: `U5u4r10_C431`

### 4. ¡Servidor ya conectado!

En el árbol lateral verás:
```
Servers
└── Campo Maniobras DB ✓ (conectado)
    └── Databases
        └── PRUEBAS
```

**Sin configuración manual. Sin escribir contraseñas.**

---

## 🔑 Credenciales

### PostgreSQL
- **Host:** `localhost` (desde el host) / `db` (desde otros contenedores)
- **Puerto:** `5432`
- **Base de datos:** `PRUEBAS`
- **Usuario:** `postgres`
- **Contraseña:** `Admin`

### pgAdmin
- **URL:** `http://localhost:5050`
- **Email:** `CAEI@caei.com`
- **Password:** `U5u4r10_C431`

---

## 🔗 Conexión desde Django

En tu `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'PRUEBAS',
        'USER': 'postgres',
        'PASSWORD': 'Admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

No olvides instalar:
```bash
pip install psycopg2-binary
```

---

## 🛠️ Comandos Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ver solo logs de PostgreSQL
docker-compose logs -f db

# Ver solo logs de pgAdmin
docker-compose logs -f pgadmin

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (¡cuidado, borra datos!)
docker-compose down -v

# Reiniciar servicios
docker-compose restart

# Ver contenedores corriendo
docker ps
```

---

## 💾 Backups

### Crear backup manual

```bash
# Backup de una base de datos específica
docker exec campos_maniobras_db pg_dump -U postgres PRUEBAS > backups/pruebas_backup_$(date +%Y%m%d).sql

# Backup de todas las bases de datos
docker exec campos_maniobras_db pg_dumpall -U postgres > backups/all_databases_$(date +%Y%m%d).sql
```

### Restaurar backup

```bash
# Restaurar una base de datos
docker exec -i campos_maniobras_db psql -U postgres PRUEBAS < backups/pruebas_backup_20241024.sql
```

---

## 🔐 Seguridad

### Para Desarrollo (configuración actual):
✅ Contraseñas en archivos locales
✅ pgPassfile para conexión automática
✅ Archivos sensibles en `.gitignore`

### Para Producción:

1. **Cambia todas las contraseñas**
2. **Elimina pgpassfile** o usa secrets de Docker
3. **No expongas el puerto 5432** si no es necesario
4. **Usa SSL/TLS** para conexiones
5. **Limita acceso a pgAdmin** con firewall/VPN

---

## 📚 Documentación

- **[CONEXION_AUTOMATICA.md](CONEXION_AUTOMATICA.md)** - Guía detallada de la conexión automática
- Docker Compose: https://docs.docker.com/compose/
- PostgreSQL: https://www.postgresql.org/docs/
- pgAdmin: https://www.pgadmin.org/docs/

---

## 🆘 Solución de Problemas

### El servidor no aparece en pgAdmin

```bash
docker-compose down
docker-compose up -d
```

### Error de permisos en pgpassfile

```bash
chmod 600 pgpassfile
docker-compose restart pgadmin
```

### PostgreSQL no inicia

Verifica logs:
```bash
docker-compose logs db
```

Verifica que el puerto 5432 no esté ocupado:
```bash
# Windows
netstat -ano | findstr :5432

# Linux/Mac
lsof -i :5432
```

---

## ✨ Características

✅ **Conexión automática** - pgAdmin se conecta automáticamente a PostgreSQL
✅ **Sin master password** - Acceso directo en modo desarrollo
✅ **Persistencia de datos** - Los datos sobreviven a reinicios
✅ **Healthcheck** - pgAdmin espera a que PostgreSQL esté listo
✅ **Backups fáciles** - Carpeta dedicada montada como volumen
✅ **Documentación completa** - Todo está explicado

---

## 🎉 ¡Listo para Usar!

Solo ejecuta `iniciar_servicios.bat` y tendrás PostgreSQL + pgAdmin corriendo con conexión automática.

**Sin pasos manuales. Sin configuración. Solo funciona.** ✨
