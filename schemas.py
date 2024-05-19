# schemas.py

from pydantic import BaseModel

# Definir el esquema de datos para las pólizas de seguro
class Policy(BaseModel):
    id: int
    name: str
    description: str
    coverage: str
    premium: float
    deductible: float
    coverage_limit: float
    start_date: str
    end_date: str
    company: str
    contact_person: str
    contact_email: str
    contact_phone: str
