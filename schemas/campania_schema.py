from pydantic import BaseModel
from datetime import date
from typing import Optional

class CampaniaBase(BaseModel):
    nombre: str
    ultima_actualizacion: date
    duracion: str
    estrategia: str
    estado: Optional[str] = "Activo"

class CampaniaCreate(CampaniaBase):
    pass

class CampaniaOut(CampaniaBase):
    id: int
