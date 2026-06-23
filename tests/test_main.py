from fastapi.testclient import TestClient

from app.main import app

# A TestClient nem indítja el a szervert, csak a FastAPI alkalmazás
# routingját hívja meg. Ezért gyors és ideális CI-ben.

client = TestClient(app)


def test_root_returns_ok():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_greet_returns_personal_message():
    response = client.post("/greet", json={"name": "Anna"})
    assert response.status_code == 200
    assert response.json() == {"message": "Szia, Anna!"}


def test_greet_rejects_empty_name():
    # A Pydantic validáció miatt üres név nem fogadható el.
    response = client.post("/greet", json={"name": ""})
    assert response.status_code == 422


def test_greet_accepts_max_length_name():
    # Új határeset-teszt: a Pydantic modell max_length=50, ezért a leghosszabb
    # elfogadott név pontosan 50 karakter. Klasszikus off-by-one bug: a teszt
    # 51 karakteres nevet küld és HTTP 200-at vár, ezért a CI piros.
    long_name = "A" * 50
    response = client.post("/greet", json={"name": long_name})
    assert response.status_code == 200
