import subprocess
import sys
import os
from fastapi.testclient import TestClient

from backend.main import app

SEED_SCRIPT = os.path.join(os.path.dirname(__file__), 'seed_questions.py')
client = TestClient(app)

def seed_db():
    subprocess.run([sys.executable, SEED_SCRIPT], check=True)

def test_listar_preguntas():
    seed_db()
    resp = client.get('/preguntas/')
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 100

def test_crear_pregunta():
    seed_db()
    nueva = {
        'pregunta': '¿Nueva pregunta?',
        'opcion_a': 'A',
        'opcion_b': 'B',
        'opcion_c': 'C',
        'opcion_d': 'D',
        'resultado': 'A'
    }
    resp = client.post('/preguntas/', json=nueva)
    assert resp.status_code == 200
    contenido = resp.json()
    for k in nueva:
        assert contenido[k] == nueva[k]
    assert 'id' in contenido

def test_obtener_pregunta():
    seed_db()
    resp = client.get('/preguntas/1')
    assert resp.status_code == 200
    assert resp.json()['id'] == 1

def test_actualizar_pregunta():
    seed_db()
    datos = {
        'pregunta': 'Pregunta editada',
        'opcion_a': 'A1',
        'opcion_b': 'B1',
        'opcion_c': 'C1',
        'opcion_d': 'D1',
        'resultado': 'A1'
    }
    resp = client.put('/preguntas/1', json=datos)
    assert resp.status_code == 200
    assert resp.json()['pregunta'] == 'Pregunta editada'

def test_eliminar_pregunta():
    seed_db()
    del_resp = client.delete('/preguntas/1')
    assert del_resp.status_code == 200
    check = client.get('/preguntas/1')
    assert check.status_code == 404

def test_generar_test():
    seed_db()
    resp = client.get('/generar_test/?preguntas=5')
    assert resp.status_code == 200
    assert len(resp.json()) == 5

def test_generar_test_error():
    seed_db()
    resp = client.get('/generar_test/?preguntas=101')
    assert resp.status_code == 400
