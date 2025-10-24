# Campo de Maniobras Cognitivo - Backend

Backend desarrollado en Django para la plataforma de simulación de redes sociales y periódicos.

## Tecnologías

- Django 5.2.7
- PostgreSQL
- Python 3.x

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/cestort/CAMPO_MANIOBRAS_COGNITIVO.git
cd CAMPO_MANIOBRAS_COGNITIVO/BACKEND
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura tus credenciales:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus datos:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-generada
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=campo_maniobras_cognitivo
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Crear la base de datos

Asegúrate de tener PostgreSQL instalado y crea la base de datos:

```sql
CREATE DATABASE campo_maniobras_cognitivo;
```

### 6. Ejecutar migraciones

```bash
python manage.py migrate
```

### 7. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 8. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## Estructura del Proyecto

```
BACKEND/
├── config/              # Configuración principal del proyecto Django
│   ├── settings.py      # Configuración (usa variables de .env)
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── .env                 # Variables de entorno (no se sube a git)
├── .env.example         # Plantilla de variables de entorno
├── .gitignore
└── requirements.txt     # Dependencias del proyecto
```

## Características Principales

- **Gestión de Usuarios**: Sistema de usuarios con permisos para cargas masivas
- **Publicaciones Masivas**: Funcionalidad para crear publicaciones con sesgo asignado
- **Redes Sociales Simuladas**: Interacción orgánica entre usuarios
- **Periódicos Simulados**: Sistema de noticias simuladas

## Desarrollo

El proyecto está en fase inicial. Próximas funcionalidades a implementar:

- [ ] Modelos de datos (Usuarios, Publicaciones, Redes Sociales)
- [ ] Sistema de autenticación y permisos
- [ ] API REST para cargas masivas
- [ ] Sistema de sesgo para publicaciones
- [ ] Interface de administración

## Contribuir

Este es un proyecto en desarrollo activo. Las contribuciones son bienvenidas.
