from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_crear_zona():
    r = client.post("/zonas/", json={
        "nombre": "Centro",
        "codigo_postal": "12345",
        "limite_velocidad": 25})
    assert r.status_code == 200


def test_crear_patinete():
    zona = client.post("/zonas/", json={
        "nombre": "Zona1",
        "codigo_postal": "00000",
        "limite_velocidad": 20}).json()

    r = client.post("/patinetes/", json={
        "numero_serie": "ABC",
        "modelo": "Xiaomi",
        "bateria": 80,
        "zona_id": zona["id"]})

    assert r.status_code == 200


def test_bateria_invalida():
    zona = client.post("/zonas/", json={
        "nombre": "Zona2",
        "codigo_postal": "11111",
        "limite_velocidad": 20}).json()

    r = client.post("/patinetes/", json={
        "numero_serie": "FAIL",
        "modelo": "Test",
        "bateria": 150,
        "zona_id": zona["id"]})

    assert r.status_code == 422


def test_mantenimiento():
    zona = client.post("/zonas/", json={
        "nombre": "Zona3",
        "codigo_postal": "22222",
        "limite_velocidad": 20}).json()

    client.post("/patinetes/", json={
        "numero_serie": "LOW",
        "modelo": "Test",
        "bateria": 10,
        "zona_id": zona["id"]})

    r = client.post(f"/zonas/{zona['id']}/mantenimiento")

    assert r.status_code == 200
    assert len(r.json()) > 0


def test_estado_mantenimiento():
    zona = client.post("/zonas/", json={
        "nombre": "Zona4",
        "codigo_postal": "33333",
        "limite_velocidad": 20}).json()

    patinete = client.post("/patinetes/", json={
        "numero_serie": "LOW2",
        "modelo": "Test",
        "bateria": 5,
        "zona_id": zona["id"]}).json()

    res = client.post(f"/zonas/{zona['id']}/mantenimiento").json()

    assert res[0]["estado"] == "mantenimiento"