import pytest

@pytest.mark.asyncio
async def test_create_item(client):
    response = await client.post("/items/", json={
        "nombre": "Teclado",
        "descripcion": "Teclado mecánico",
        "precio": 79.99,
        "en_stock": True,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Teclado"
    assert data["precio"] == 79.99
    assert data["en_stock"] is True
    assert "id" in data

@pytest.mark.asyncio
async def test_list_items_empty(client):
    response = await client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_list_items_after_create(client):
    await client.post("/items/", json={
        "nombre": "Ratón",
        "descripcion": None,
        "precio": 25.0,
        "en_stock": True,
    })
    response = await client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nombre"] == "Ratón"
