# IDEA

IDEA es una plataforma gratuita y de código abierto para la creación, personalización y administración de exámenes en tiempo real. Está pensada para docentes y estudiantes, permitiendo generar pruebas sin límite de participantes e integrando funciones de inteligencia artificial, gamificación y análisis de resultados. Además, se puede integrar con Moodle, lo que facilita su adopción en diversos contextos educativos.

## Carpetas principales

- **frontend/**: código de la interfaz y componentes visuales.
- **backend/**: API en FastAPI y lógica de negocio.
- **model/**: modelos de inteligencia artificial y procesos de entrenamiento/inferencia.
- **database/**: esquema y configuraciones de la base de datos.
- **docs/**: documentación técnica y manuales de uso.
- **tests/**: pruebas automatizadas.
- **scripts/**: utilidades para despliegue y automatización.

Cada carpeta contiene un `README.md` descriptivo que puede ampliarse a medida que se desarrollen los distintos módulos.

## Instalación

Instala las dependencias del proyecto ejecutando:


```bash
pip install -r requirements.txt
```

## Frontend

Ejecuta la interfaz de ejemplo con:
```bash
streamlit run frontend/main.py
```

## Backend

Inicia la API desde la carpeta `backend`:

```bash
cd backend && uvicorn main:app --reload
```

El archivo `database/questions.db` se creará automáticamente la primera vez que se ejecute la aplicación.

=======
## Relleno de la base de datos

En la carpeta `tests` se incluye el script `seed_questions.py` que genera una base
de datos SQLite con 100 preguntas de ingeniería informática. Para poblar la
tabla `preguntas` basta con ejecutar:

```bash
python3 tests/seed_questions.py
```

Esto creará el archivo `database/questions.db` (ignorado en Git) y
poblará su contenido con datos de ejemplo.
Si el archivo no existe, también se generará automáticamente al arrancar el backend.

