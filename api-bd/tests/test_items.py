import pytest


@pytest.mark.asyncio
async def test_list_items_empty(client):
    response = await client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_crear_item_en_categoria(client):
    cat = await client.post("/categorias/", json={"nombre": "Periféricos"})
    assert cat.status_code == 200
    cat_id = cat.json()["id"]

    response = await client.post(f"/categorias/{cat_id}/items/", json={
        "nombre": "Teclado",
        "precio": 79.99,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Teclado"
    assert data["precio"] == 79.99
    assert data["categoria"] == "Periféricos"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_items_after_create(client):
    cat = await client.post("/categorias/", json={"nombre": "Audio"})
    cat_id = cat.json()["id"]
    await client.post(f"/categorias/{cat_id}/items/", json={"nombre": "Auriculares", "precio": 59.0})

    response = await client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nombre"] == "Auriculares"


@pytest.mark.asyncio
async def test_get_item_by_id(client):
    cat = await client.post("/categorias/", json={"nombre": "Video"})
    cat_id = cat.json()["id"]
    create_resp = await client.post(f"/categorias/{cat_id}/items/", json={"nombre": "Monitor", "precio": 399.0})
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
    cat = await client.post("/categorias/", json={"nombre": "Redes"})
    cat_id = cat.json()["id"]
    create_resp = await client.post(f"/categorias/{cat_id}/items/", json={"nombre": "Router", "precio": 50.0})
    item_id = create_resp.json()["id"]

    response = await client.put(f"/items/{item_id}", json={"nombre": "Router Pro", "precio": 89.0})
    assert response.status_code == 200
    assert response.json()["nombre"] == "Router Pro"
    assert response.json()["precio"] == 89.0


@pytest.mark.asyncio
async def test_update_item_not_found(client):
    response = await client.put("/items/9999", json={"nombre": "X", "precio": 1.0})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_item(client):
    cat = await client.post("/categorias/", json={"nombre": "Cables"})
    cat_id = cat.json()["id"]
    create_resp = await client.post(f"/categorias/{cat_id}/items/", json={"nombre": "Cable USB-C", "precio": 9.99})
    item_id = create_resp.json()["id"]

    del_resp = await client.delete(f"/items/{item_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["mensaje"] == "Item eliminado"
    assert (await client.get(f"/items/{item_id}")).status_code == 404


@pytest.mark.asyncio
async def test_delete_item_not_found(client):
    response = await client.delete("/items/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_crear_item_categoria_inexistente(client):
    response = await client.post("/categorias/9999/items/", json={"nombre": "X", "precio": 1.0})
    assert response.status_code == 404
