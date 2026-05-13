from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import models
import schemas
from dependencies import get_db

app = FastAPI()


# --- Categorías ---

@app.post("/categorias/", response_model=schemas.CategoriaResponse)
async def crear_categoria(cat: schemas.CategoriaCreate, db: AsyncSession = Depends(get_db)):
    db_cat = models.Categoria(nombre=cat.nombre)
    db.add(db_cat)
    await db.commit()
    await db.refresh(db_cat)
    return db_cat


@app.get("/categorias/", response_model=list[schemas.CategoriaResponse])
async def listar_categorias(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Categoria))
    return result.scalars().all()


# --- Tags ---

@app.post("/tags/", response_model=schemas.TagResponse)
async def crear_tag(tag: schemas.TagBase, db: AsyncSession = Depends(get_db)):
    db_tag = models.Tag(nombre=tag.nombre)
    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag


@app.get("/tags/", response_model=list[schemas.TagResponse])
async def listar_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Tag))
    return result.scalars().all()


# --- Items ---

@app.post("/categorias/{cat_id}/items/", response_model=schemas.ItemDetalle)
async def crear_item(cat_id: int, item: schemas.ItemBase, db: AsyncSession = Depends(get_db)):
    cat = await db.get(models.Categoria, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db_item = models.Item(**item.model_dump(), categoria_id=cat_id)
    db.add(db_item)
    await db.commit()
    result = await db.execute(
        select(models.Item)
        .where(models.Item.id == db_item.id)
        .options(selectinload(models.Item.categoria), selectinload(models.Item.tags))
    )
    return result.scalar_one()


@app.get("/items/", response_model=list[schemas.ItemDetalle])
async def listar_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Item).options(
            selectinload(models.Item.categoria),
            selectinload(models.Item.tags),
        )
    )
    return result.scalars().all()


@app.get("/items/{item_id}", response_model=schemas.ItemDetalle)
async def leer_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Item)
        .where(models.Item.id == item_id)
        .options(selectinload(models.Item.categoria), selectinload(models.Item.tags))
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item


@app.put("/items/{item_id}", response_model=schemas.ItemDetalle)
async def actualizar_item(item_id: int, item: schemas.ItemBase, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Item).where(models.Item.id == item_id))
    db_item = result.scalar_one_or_none()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
    await db.commit()
    result = await db.execute(
        select(models.Item)
        .where(models.Item.id == item_id)
        .options(selectinload(models.Item.categoria), selectinload(models.Item.tags))
    )
    return result.scalar_one()


@app.delete("/items/{item_id}")
async def eliminar_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Item).where(models.Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    await db.delete(item)
    await db.commit()
    return {"mensaje": "Item eliminado"}


@app.post("/items/{item_id}/tags/{tag_id}")
async def asignar_tag(item_id: int, tag_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Item)
        .where(models.Item.id == item_id)
        .options(selectinload(models.Item.tags))
    )
    item = result.scalar_one_or_none()
    tag_result = await db.execute(select(models.Tag).where(models.Tag.id == tag_id))
    tag = tag_result.scalar_one_or_none()
    if not item or not tag:
        raise HTTPException(status_code=404, detail="No encontrado")
    item.tags.append(tag)
    await db.commit()
    return {"mensaje": "Tag vinculado con éxito"}
