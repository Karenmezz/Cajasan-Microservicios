from fastapi import APIRouter, Depends

from .data import ORDERS
from .security import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("")
def list_orders(user=Depends(get_current_user)):
    return ORDERS
