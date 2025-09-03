# Este adaptador usa FastAPI y se comunica con el servicio del núcleo.
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from .schemas import (
    CreateDiscountRequest, CreateDiscountResponse,
    ValidateDiscountRequest, ValidateDiscountResponse, DiscountResponse
)
from src.discounts.domain.models import Cart
from src.discounts.application.services import DiscountService
from main import get_discount_service # Función para inyección de dependencias

router = APIRouter()

@router.post("/discounts", response_model=CreateDiscountResponse, status_code=201)
def create_discount_endpoint(
    request: CreateDiscountRequest,
    service: DiscountService = Depends(get_discount_service)
):
    """Endpoint para crear un nuevo descuento."""
    print("ADAPTER (API): Petición recibida para crear descuento.")
    try:
        discount = service.create_discount(code=request.code, percentage=request.percentage)
        return CreateDiscountResponse(code=discount.code, is_active=discount.is_active)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate-discount", response_model=ValidateDiscountResponse, status_code=202)
def validate_discount_endpoint(
    request: ValidateDiscountRequest,
    service: DiscountService = Depends(get_discount_service)
):
    """Endpoint para solicitar la validación asíncrona de un descuento."""
    print("ADAPTER (API): Petición recibida para validar descuento.")
    cart = Cart(
        cart_id=request.cart_id,
        total_amount=request.total_amount,
        user_id=request.user_id
    )
    service.request_discount_validation(code=request.code, cart=cart)
    return ValidateDiscountResponse(message="Solicitud de validación recibida. Se procesará en segundo plano.")

@router.get("/discounts", response_model=List[DiscountResponse])
def get_all_discounts_endpoint(
    service: DiscountService = Depends(get_discount_service)
):
    """Endpoint para obtener una lista de todos los descuentos."""
    print("ADAPTER (API): Petición recibida para obtener todos los descuentos.")
    return service.get_all_discounts()

@router.get("/discounts/{code}", response_model=DiscountResponse)
def get_discount_by_code_endpoint(
    code: str,
    service: DiscountService = Depends(get_discount_service)
):
    """Endpoint para obtener un descuento específico por su código."""
    print(f"ADAPTER (API): Petición recibida para obtener el descuento '{code}'.")
    discount = service.get_discount_by_code(code)
    if not discount:
        raise HTTPException(
            status_code=404,
            detail=f"Descuento con código '{code}' no encontrado."
        )
    return discount
