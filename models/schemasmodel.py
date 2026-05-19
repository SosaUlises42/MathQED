from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

class UsuarioLogin(BaseModel):
    email: str
    password: str = Field(..., min_length=8)
    
class UsuarioSchema(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    email: str
    password: str = Field(..., min_length=8)
    
class TareaSchema(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = None
    prioridad: str = "Media"
    clasificacion: str= "personal"