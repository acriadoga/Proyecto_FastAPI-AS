import pytest


@pytest.mark.asyncio
async def test_crear_categoria(client):
    response = await client.post("/categorias/", json={"nombre": "Gaming"})
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Gaming"
    assert "id" in data


@pytest.mark.asyncio
async def test_listar_categorias(client):
    await client.post("/categorias/", json={"nombre": "Hogar"})
    response = await client.get("/categorias/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nombre"] == "Hogar"


@pytest.mark.asyncio
async def test_crear_tag(client):
    response = await client.post("/tags/", json={"nombre": "Oferta"})
    assert response.status_code == 200
    assert response.json()["nombre"] == "Oferta"


@pytest.mark.asyncio
async def test_listar_tags(client):
    await client.post("/tags/", json={"nombre": "Nuevo"})
    response = await client.get("/tags/")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_asignar_tag_a_item(client):
    cat = await client.post("/categorias/", json={"nombre": "PC"})
    cat_id = cat.json()["id"]
    item = await client.post(f"/categorias/{cat_id}/items/", json={"nombre": "Ratón", "precio": 35.0})
    item_id = item.json()["id"]

    tag = await client.post("/tags/", json={"nombre": "Gaming"})
    tag_id = tag.json()["id"]

    response = await client.post(f"/items/{item_id}/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json()["mensaje"] == "Tag vinculado con éxito"


@pytest.mark.asyncio
async def test_item_muestra_categoria_y_tags(client):
    cat = await client.post("/categorias/", json={"nombre": "Monitores"})
    cat_id = cat.json()["id"]
    item = await client.post(f"/categorias/{cat_id}/items/", json={"nombre": "Monitor 4K", "precio": 350.0})
    item_id = item.json()["id"]

    tag = await client.post("/tags/", json={"nombre": "4K"})
    tag_id = tag.json()["id"]
    await client.post(f"/items/{item_id}/tags/{tag_id}")

    response = await client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["categoria"] == "Monitores"
    assert any(t["nombre"] == "4K" for t in data["tags"])


@pytest.mark.asyncio
async def test_item_en_lista_incluye_relaciones(client):
    cat = await client.post("/categorias/", json={"nombre": "Teclados"})
    cat_id = cat.json()["id"]
    item = await client.post(f"/categorias/{cat_id}/items/", json={"nombre": "Mecánico", "precio": 120.0})
    item_id = item.json()["id"]
    tag = await client.post("/tags/", json={"nombre": "Silencioso"})
    await client.post(f"/items/{item_id}/tags/{tag.json()['id']}")

    response = await client.get("/items/")
    assert response.status_code == 200
    item_data = response.json()[0]
    assert item_data["categoria"] == "Teclados"
    assert item_data["tags"][0]["nombre"] == "Silencioso"


@pytest.mark.asyncio
async def test_asignar_tag_item_inexistente(client):
    tag = await client.post("/tags/", json={"nombre": "Test"})
    tag_id = tag.json()["id"]
    response = await client.post(f"/items/9999/tags/{tag_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_asignar_tag_inexistente(client):
    cat = await client.post("/categorias/", json={"nombre": "TV"})
    cat_id = cat.json()["id"]
    item = await client.post(f"/categorias/{cat_id}/items/", json={"nombre": "Televisor", "precio": 500.0})
    item_id = item.json()["id"]
    response = await client.post(f"/items/{item_id}/tags/9999")
    assert response.status_code == 404
