from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PANIER = {
    "commerce": "Boulangerie du coin",
    "titre": "Panier viennoiseries",
    "description": "Croissants de la veille",
    "prix_initial": 12,
    "prix_reduit": 4,
    "quantite": 2,
}


def test_health():
    reponse = client.get("/health")
    assert reponse.status_code == 200
    assert reponse.json() == {"status": "ok"}


def test_creer_et_lister():
    reponse = client.post("/paniers", json=PANIER)
    assert reponse.status_code == 201
    id_panier = reponse.json()["id"]
    liste = client.get("/paniers").json()
    assert any(p["id"] == id_panier for p in liste)


def test_prix_reduit_invalide():
    reponse = client.post("/paniers", json={**PANIER, "prix_reduit": 20})
    assert reponse.status_code == 400


def test_reserver_jusqu_a_epuisement():
    id_panier = client.post("/paniers", json=PANIER).json()["id"]
    assert client.post(f"/paniers/{id_panier}/reserver").json()["quantite"] == 1
    assert client.post(f"/paniers/{id_panier}/reserver").json()["quantite"] == 0
    assert client.post(f"/paniers/{id_panier}/reserver").status_code == 400


def test_supprimer():
    id_panier = client.post("/paniers", json=PANIER).json()["id"]
    assert client.delete(f"/paniers/{id_panier}").status_code == 204
    assert client.delete(f"/paniers/{id_panier}").status_code == 404