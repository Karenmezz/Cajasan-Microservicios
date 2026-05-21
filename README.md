# Cajasan-Microservicios

Karen Tatiana Pimiento Martinez

## Tienda Microservicios

Prueba tecnica. Un backend en Python con FastAPI que expone la API con login por JWT, y un frontend en React que lo consume.

## Carpetas

- backend-python: API en FastAPI
- frontend-react: app en React + TypeScript

## Usuarios de prueba

admin / admin123 (ADMIN)
user / user123 (USER)

No hay base de datos, los usuarios estan hardcodeados.

## Endpoints

POST /auth/login -> recibe usuario y contrasena, devuelve access_token y refresh_token
POST /auth/refresh -> recibe el refresh_token y devuelve un nuevo access_token
POST /auth/logout -> invalida el token
GET /products y GET /orders -> requieren el header Authorization: Bearer <token>

El access_token dura 3 minutos y el refresh_token 1 dia. Cuando el access_token vence el backend responde 401 y el frontend pide uno nuevo con el refresh_token de forma automatica. Si el refresh tambien vencio se borran los tokens y se vuelve al login.

## Como correr

backend-python (puerto 8000):

    cd backend-python
    python -m venv .venv
    .venv\Scripts\activate
    pip install fastapi uvicorn "python-jose[cryptography]"
    uvicorn app.main:app --reload

frontend-react (puerto 5173):

    cd frontend-react
    npm install
    npm run dev

Los tokens se guardan en sessionStorage. La URL del backend se cambia en frontend-react/src/api/client.ts.
