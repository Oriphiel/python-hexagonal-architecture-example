# Modelos de datos para la API, usando Pydantic.
from pydantic import BaseModel, Field

class CreateDiscountRequest(BaseModel):
    code: str = Field(..., min_length=3, description="Código único del descuento")
    percentage: float = Field(..., gt=0, le=100, description="Porcentaje de descuento")

class CreateDiscountResponse(BaseModel):
    code: str
    is_active: bool

class ValidateDiscountRequest(BaseModel):
    code: str
    cart_id: str
    total_amount: float
    user_id: str

class ValidateDiscountResponse(BaseModel):
    message: str

class DiscountResponse(BaseModel):
    code: str
    percentage: float
    is_active: bool

    class Config:
        from_attributes = True
