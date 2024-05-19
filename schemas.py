from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class CoverageInput(BaseModel):
    outpatient_gp: Optional[bool] = Field(None, description="Cobertura para atención ambulatoria con médico general")
    outpatient_sp: Optional[bool] = Field(None, description="Cobertura para atención ambulatoria con especialista")
    outpatient_dental: Optional[bool] = Field(None, description="Cobertura para atención ambulatoria dental")
    personal_accident: Optional[bool] = Field(None, description="Cobertura para accidentes personales")
    term_life: Optional[bool] = Field(None, description="Cobertura de vida a término")
    critical_illness: Optional[bool] = Field(None, description="Cobertura para enfermedades críticas")

class CoverageOutput(CoverageInput):
    coverageId: int = Field(..., description="ID de la cobertura")

class ProductOutput(BaseModel):
    productId: int = Field(..., description="ID del producto")
    pymesId: int = Field(..., description="ID de la Pyme asociada")
    coverageId: int = Field(..., description="ID de la cobertura asociada")
    product_name: Optional[str] = Field(None, description="Nombre del producto")
    product_options: Optional[str] = Field(None, description="Opciones del producto")
    top_feature: Optional[str] = Field(None, description="Características principales del producto")
    inpatient: Optional[str] = Field(None, description="Cobertura para hospitalización")
    outpatient_gp: Optional[str] = Field(None, description="Cobertura para atención ambulatoria con médico general")
    outpatient_sp: Optional[str] = Field(None, description="Cobertura para atención ambulatoria con especialista")
    outpatient_dental: Optional[str] = Field(None, description="Cobertura para atención ambulatoria dental")
    personal_accident: Optional[str] = Field(None, description="Cobertura para accidentes personales")
    term_life: Optional[str] = Field(None, description="Cobertura de vida a término")
    critical_illness: Optional[str] = Field(None, description="Cobertura para enfermedades críticas")
    premium_per_pax: Optional[float] = Field(None, description="Prima por persona")
    total_premium: Optional[float] = Field(None, description="Prima total")

class PymeOutput(BaseModel):
    pymesId: int = Field(..., description="ID de la Pyme")
    total_employee: int = Field(..., description="Número total de empleados")
    average_age: int = Field(..., description="Edad promedio de los empleados")
    is_private: bool = Field(..., description="Indica si la Pyme es privada")
    bedded: int = Field(..., description="Número de camas")
    is_sorted_ascending: bool = Field(..., description="Indica si los datos están ordenados de forma ascendente")
    register_date: Optional[date] = Field(None, description="Fecha de registro de la Pyme")
    products: List[ProductOutput] = Field(..., description="Lista de productos asociados a la Pyme")

class PymeInput(BaseModel):
    total_employee: int = Field(..., description="Número total de empleados")
    average_age: int = Field(..., description="Edad promedio de los empleados")
    is_private: bool = Field(..., description="Indica si la Pyme es privada")
    bedded: int = Field(..., description="Número de camas")
    is_sorted_ascending: bool = Field(..., description="Indica si los datos están ordenados de forma ascendente")
    register_date: Optional[date] = Field(None, description="Fecha de registro de la Pyme")
    coverage: CoverageInput = Field(..., description="Información de cobertura asociada a la Pyme")
