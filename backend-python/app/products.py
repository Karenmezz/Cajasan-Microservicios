from fastapi import APIRouter, Depends

from .data import PRODUCTS
from .security import get_current_user

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def list_products(user=Depends(get_current_user)):
    return PRODUCTS
