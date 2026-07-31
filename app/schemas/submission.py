from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class SubmissionCreate(BaseModel):
    model_config = ConfigDict(extra="allow")

    fecha: Optional[datetime] = None
    tipo_cliente: Optional[str] = None
    tipo_vinculacion: Optional[str] = None
    ciudad_id: Optional[int] = None
    oficina: Optional[str] = None
    tipo_persona: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    razon_social: Optional[str] = None
    tipo_id: Optional[str] = None
    numero_id: Optional[str] = None
    fecha_expedicion: Optional[datetime] = None
    estructura_juridica: Optional[str] = None
    codigo_ciiu: Optional[str] = None
    pais_origen_id: Optional[int] = None
    pais_residencia_id: Optional[int] = None
    zona: Optional[str] = None
    regimen_tributario: Optional[str] = None
    total_ingresos: Optional[float] = None
    total_egresos: Optional[float] = None
    aut_datos: Optional[bool] = False
    aut_laft: Optional[bool] = False
    aut_anticorrupcion: Optional[bool] = False
    aut_etica: Optional[bool] = False
