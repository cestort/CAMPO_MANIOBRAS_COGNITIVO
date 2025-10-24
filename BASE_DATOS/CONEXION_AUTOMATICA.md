# 🔗 Conexión Automática pgAdmin → PostgreSQL

## 📁 Archivos Añadidos

### 1. `servers.json`
Define el servidor PostgreSQL pre-configurado que pgAdmin cargará automáticamente.

```json
{
  "Servers": {
    "1": {
      "Name": "Campo Maniobras DB",
      "Group": "Servers",
      "Host": "db",
      "Port": 5432,
      "MaintenanceDB": "PRUEBAS",
      "Username": "postgres",
      "SSLMode": "prefer",
      "PassFile": "/tmp/pgpassfile"
    }
  }
}
```

**Características:**
- Host: `db` (nombre del servicio en docker-compose)
- Database: `PRUEBAS` (según tu .env)
- Usuario: `postgres` (según tu .env)
- PassFile: Referencia al archivo de contraseñas

---

### 2. `pgpassfile`
Archivo de credenciales en formato PostgreSQL estándar.

```
db:5432:*:postgres:Admin
```

**Formato:** `hostname:port:database:username:password`
- `*` = vale para cualquier base de datos

**⚠️ Importante:** 
- Este archivo contiene la contraseña en texto plano
- Está en `.gitignore` (no se sube a Git)
- Permisos: 600 (solo lectura para el propietario)

---

## 🔧 Cambios en `docker-compose.yml`

### Añadido en el servicio `pgadmin`:

```yaml
environment:
  # Nuevas variables para facilitar desarrollo
  PGADMIN_CONFIG_SERVER_MODE: 'False'
  PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED: 'False'

volumes:
  - ./servers.json:/pgadmin4/servers.json:ro      # Servidor pre-configurado
  - ./pgpassfile:/tmp/pgpassfile:ro               # Credenciales
```

**Lo que hace:**
1. `servers.json` → Define el servidor que aparecerá en pgAdmin
2. `pgpassfile` → Proporciona la contraseña automáticamente
3. `:ro` → Montaje de solo lectura (read-only)

---

## 🚀 Cómo Usar

### Primera vez (o después de `docker-compose down -v`)

1. **Asegúrate de tener los archivos:**
   ```
   BASE_DATOS/
   ├── docker-compose.yml
   ├── .env
   ├── servers.json          ← NUEVO
   ├── pgpassfile            ← NUEVO
   ├── iniciar_servicios.bat
   └── backups/
   ```

2. **Inicia los servicios:**
   ```bash
   .\iniciar_servicios.bat
   ```

3. **Accede a pgAdmin:**
   - URL: `http://localhost:5050`
   - Email: `CAEI@caei.com`
   - Password: `U5u4r10_C431`

4. **¡Servidor ya conectado!**
   En el árbol lateral izquierdo verás:
   ```
   Servers
   └── Campo Maniobras DB (conectado automáticamente)
       └── Databases
           └── PRUEBAS
   ```

---

## ✨ Ventajas

✅ **Cero configuración manual** - El servidor aparece automáticamente
✅ **Sin escribir contraseñas** - La conexión es automática
✅ **Coherente con .env** - Usa los mismos valores
✅ **Persiste** - Aunque recrees los contenedores, sigue configurado
✅ **No requiere master password** - Más rápido para desarrollo

---

## 🔐 Seguridad

### Para Desarrollo (actual):
✅ Conveniente - Conexión automática
✅ Contraseña en archivo local
✅ No se sube a Git (está en .gitignore)

### Para Producción:
Si despliegas esto en producción:

1. **Elimina `pgpassfile`** del volumen
2. **Cambia en servers.json:**
   ```json
   "PassFile": "/tmp/pgpassfile"  → Eliminar esta línea
   ```
3. pgAdmin pedirá contraseña al conectar (más seguro)

O mejor aún, usa secrets de Docker Swarm/Kubernetes.

---

## 🛠️ Personalización

### Cambiar nombre del servidor en pgAdmin:
Edita `servers.json`:
```json
"Name": "Mi Servidor Custom"
```

### Añadir más servidores:
```json
{
  "Servers": {
    "1": {
      "Name": "Desarrollo",
      ...
    },
    "2": {
      "Name": "Producción",
      ...
    }
  }
}
```

---

## 🆘 Solución de Problemas

### El servidor no aparece en pgAdmin

**Verificar:**
1. Que `servers.json` esté en la misma carpeta que `docker-compose.yml`
2. Que el volumen esté montado correctamente:
   ```bash
   docker exec campo_maniobras_pgadmin ls -la /pgadmin4/servers.json
   ```

**Solución:**
```bash
docker-compose down
docker-compose up -d
```

### Pide contraseña aunque tengo pgpassfile

**Verificar permisos:**
```bash
ls -l pgpassfile
# Debe mostrar: -rw------- (600)
```

**Corregir:**
```bash
chmod 600 pgpassfile
docker-compose restart pgadmin
```

### Cambié las credenciales en .env

**Actualizar archivos:**
1. Edita `pgpassfile` con la nueva contraseña
2. Edita `servers.json` si cambiaron usuario/database
3. Reinicia:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

---

## 📋 Checklist

- [x] Crear `servers.json`
- [x] Crear `pgpassfile`
- [x] Actualizar `docker-compose.yml`
- [x] Añadir ambos archivos a `.gitignore`
- [x] Establecer permisos 600 en `pgpassfile`
- [x] Iniciar servicios
- [x] Verificar conexión automática

---

## 🎉 Resultado

Al abrir pgAdmin, verás el servidor "Campo Maniobras DB" ya conectado y listo para usar.

**Sin pasos manuales. Sin escribir contraseñas. Solo funciona.** ✨
