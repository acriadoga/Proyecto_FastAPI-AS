from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, ConfigDict
from models import Item
from dependencies import get_db

app = FastAPI()


class ItemCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    en_stock: bool = True


class ItemResponse(ItemCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@app.get("/items/", response_model=list[ItemResponse])
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    return result.scalars().all()
