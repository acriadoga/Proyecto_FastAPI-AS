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

@pytest.mark.asyncio
async def test_get_item_by_id(client):
    create_resp = await client.post("/items/", json={
        "nombre": "Monitor", "descripcion": "4K", "precio": 399.0, "en_stock": True
    })
    item_id = create_resp.json()["id"]
    response = await client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Monitor"

@pytest.mark.asyncio
async def test_get_item_not_found(client):
    response = await client.get("/items/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item no encontrado"

@pytest.mark.asyncio
async def test_update_item(client):
    create_resp = await client.post("/items/", json={
        "nombre": "Auriculares", "descripcion": "Inalámbricos", "precio": 59.0, "en_stock": True
    })
    item_id = create_resp.json()["id"]
    response = await client.put(f"/items/{item_id}", json={
        "nombre": "Auriculares Pro", "descripcion": "ANC", "precio": 89.0, "en_stock": True
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Auriculares Pro"
    assert response.json()["precio"] == 89.0

@pytest.mark.asyncio
async def test_update_item_not_found(client):
    response = await client.put("/items/9999", json={
        "nombre": "X", "descripcion": None, "precio": 1.0, "en_stock": True
    })
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_item(client):
    create_resp = await client.post("/items/", json={
        "nombre": "Cable", "descripcion": "USB-C", "precio": 9.99, "en_stock": True
    })
    item_id = create_resp.json()["id"]
    del_resp = await client.delete(f"/items/{item_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["mensaje"] == "Item eliminado"
    assert (await client.get(f"/items/{item_id}")).status_code == 404

@pytest.mark.asyncio
async def test_delete_item_not_found(client):
    response = await client.delete("/items/9999")
    assert response.status_code == 404
