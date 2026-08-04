# management-providers

Sistema de gestión y vinculación de proveedores para **Lagobo Distribuciones S.A.S.**

## 1. Entorno Virtual

python -m venv venv

venv\Scripts\activate

## 2. Instalación de Dependencias

pip install -r requirements.txt

## 3. Ejecución del Servidor

uvicorn main:app --host 127.0.1.1 --port 8000

## 4. Tecnologías

### Backend
- **Python 3.x**
- **FastAPI** — framework web y construcción de la API REST
- **Uvicorn** — servidor ASGI
- **SQLAlchemy 2.0** — ORM y mapeo de modelos
- **Alembic** — migraciones de base de datos
- **Pydantic** — validación y esquemas de datos
- **PyJWT / python-jose** — autenticación con tokens JWT
- **Argon2** — hash seguro de contraseñas
- **ReportLab** — generación de documentos (formularios)
- **Pillow** — procesamiento de imágenes (escaneos/firmas)
- **Pandas** — lectura y carga de datos maestros desde Excel
- **Psycopg2** — driver para PostgreSQL
- **python-dotenv** — gestión de variables de entorno

### Base de datos
- **SQLite** (por defecto, archivo local)
- **PostgreSQL** (producción, configurable con `DATABASE_URL`)

### Frontend
- **HTML5, CSS3 y JavaScript** (vanilla, sin frameworks)
- **Fetch API** — consumo de la API REST
- Frontend servido como archivos estáticos por FastAPI

### Herramientas y flujo de trabajo
- **Git + GitHub** — control de versiones (ramas `feature/`, `fix/`, `refactor/`)
- **jsdom** — pruebas del frontend en Node.js

## Autor

**Miguel Angel Diaz Gomez** — GitHub: [Najuis](https://github.com/Najuis)

## Por cada cambio o trabajo nuevo se crea una nueva rama con el nombre del cambio o trabajo a realizar

## Ejemplo de rama 

## para nuevo cambio
git checkout -b feature/nombre-de-la-funcionalidad 

## para cuando se organiza algo 

git checkout -b fix/nombre-del-arreglo o  git checkout -b refactor/nombre-del-arreglo
