USERS = [
    {"username": "admin", "password": "admin123", "role": "ADMIN"},
    {"username": "user", "password": "user123", "role": "USER"},
]

PRODUCTS = [
    {"id": 1, "name": "Teclado mecanico", "price": 120000, "stock": 15},
    {"id": 2, "name": "Mouse inalambrico", "price": 80000, "stock": 30},
    {"id": 3, "name": "Monitor 24 pulgadas", "price": 650000, "stock": 8},
]

ORDERS = [
    {"id": 1, "user": "admin", "product_id": 1, "quantity": 2, "total": 240000},
    {"id": 2, "user": "user", "product_id": 2, "quantity": 1, "total": 80000},
]


def find_user(username):
    for u in USERS:
        if u["username"] == username:
            return u
    return None
