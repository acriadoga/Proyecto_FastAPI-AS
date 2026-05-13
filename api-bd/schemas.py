from pydantic import BaseModel, ConfigDict, field_validator


class TagBase(BaseModel):
    nombre: str
    model_config = ConfigDict(from_attributes=True)


class TagResponse(TagBase):
    id: int


class CategoriaCreate(BaseModel):
    nombre: str


class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    model_config = ConfigDict(from_attributes=True)


class ItemBase(BaseModel):
    nombre: str
    precio: float
    model_config = ConfigDict(from_attributes=True)


class ItemDetalle(ItemBase):
    id: int
    categoria: str | None = None
    tags: list[TagBase] = []

    @field_validator("categoria", mode="before")
    @classmethod
    def extract_categoria_nombre(cls, v):
        if hasattr(v, "nombre"):
            return v.nombre
        return v
