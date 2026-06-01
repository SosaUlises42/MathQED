from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

class UsuarioLogin(BaseModel):
    email: str
    password: str = Field(..., min_length=8)
    
class UsuarioSchema(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    email: str
    control: str = Field(
        ...,
        min_length=14, max_length=14,
        pattern=r"^\d+$"
    )
    password: str = Field(..., min_length=8)
    grado: str = Field(
        ...,
        min_length=1, max_length=1,
        pattern=r"^\d+$"
    )
    grupo: str = Field(..., min_length=1, max_length=1)
    print("UsuarioSchema se ejecuta correctamente...")
    
class TareaSchema(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = None
    prioridad: str = "Media"
    clasificacion: str= "personal"