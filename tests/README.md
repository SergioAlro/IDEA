# Test Seeder – Preguntas Tipo Test

Este módulo tiene como objetivo poblar la base de datos con **preguntas tipo test** utilizando datos simulados (mockeados). Es útil para propósitos de desarrollo, pruebas o demostraciones del sistema de evaluación.

---

## Contenido generado

El script inserta datos en las siguientes tablas:

- `questions`: Preguntas con campos como texto, categoría y dificultad.
- `answers`: Respuestas asociadas a cada pregunta, marcando cuál(es) son correctas.

---

## Ejecución

### Prerrequisitos

- Base de datos configurada y migraciones aplicadas.
- Acceso a un entorno Python con las siguientes librerías instaladas (si aplica):

```bash
pip install SQLAlchemy
