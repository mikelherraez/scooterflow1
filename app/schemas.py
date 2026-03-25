from pydantic import BaseModel, Field
from app.enums import Estado


class ZonaCreate(BaseModel):
    nombre: str
    codigo_postal: str
    limite_velocidad: int


class PatineteCreate(BaseModel):
    numero_serie: str
    modelo: str
    bateria: float = Field(..., ge=0, le=100)
    zona_id: int
    estado: Estado | None = None


class ZonaOut(BaseModel):
    id: int
    nombre: str
    codigo_postal: str
    limite_velocidad: int

    model_config = {"from_attributes": True}  


class PatineteOut(BaseModel):
    id: int
    numero_serie: str
    modelo: str
    bateria: float
    zona_id: int
    estado: Estado

    model_config = {"from_attributes": True} 

class ZonaConPatinetes(BaseModel):
    id: int
    nombre: str
    codigo_postal: str
    limite_velocidad: int
    patinetes: list[PatineteOut]

    model_config = {"from_attributes": True}