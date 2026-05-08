from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Gestión de Taller API")

class Coche(BaseModel):
    id: int
    marca: str
    modelo: str
    matricula: str
    cliente_id: int

class Cliente(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    coches: Optional[List[Coche]] = None

clientes_db: List[Cliente] = [
    Cliente(id=1, nombre="Juan Pérez", telefono="600123456", email="juan@example.com")
]

coches_db: List[Coche] = [
    Coche(id=1, marca="Toyota", modelo="Corolla", matricula="1234ABC", cliente_id=1)
]

@app.get("/clientes/", response_model=List[Cliente])
def get_clientes() -> List[Cliente]:
    resultado = []
    for cliente in clientes_db:
        coches_del_cliente = [c for c in coches_db if c.cliente_id == cliente.id]
        cliente_completo = cliente.model_copy(update={"coches": coches_del_cliente})
        resultado.append(cliente_completo)
    return resultado

@app.post("/clientes/", response_model=Cliente)
def create_cliente(cliente: Cliente) -> Cliente:
    if any(c.id == cliente.id for c in clientes_db):
        raise HTTPException(status_code=400, detail="El ID de cliente ya existe")
    clientes_db.append(cliente)
    return cliente

@app.get("/coches/", response_model=List[Coche])
def get_coches() -> List[Coche]:
    return coches_db

@app.get("/coches/matricula/{matricula}", response_model=Coche)
def get_coche_por_matricula(matricula: str) -> Coche:
    coche = next((c for c in coches_db if c.matricula == matricula), None)
    if coche is None:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    return coche

@app.post("/coches/", response_model=Coche)
def create_coche(coche: Coche) -> Coche:
    if not any(c.id == coche.cliente_id for c in clientes_db):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if any(c.id == coche.id for c in coches_db):
        raise HTTPException(status_code=400, detail="El ID de coche ya existe")
    coches_db.append(coche)
    return coche

@app.delete("/coches/{coche_id}")
def delete_coche(coche_id: int):
    global coches_db
    coche = next((c for c in coches_db if c.id == coche_id), None)
    if coche is None:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    coches_db = [c for c in coches_db if c.id != coche_id]
    return {"mensaje": f"Vehículo con ID {coche_id} eliminado correctamente"}
