from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router
from routes.campania_routes import router as campania_router
from routes.sql_routes import router as sql_router
from routes.ml_routes import ml_router
from routes.cliente_routes import router as clientes_router
from routes.email import router as email_router
from routes.tracking import router as tracking_router

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(clientes_router)
app.include_router(campania_router)
app.include_router(email_router)
app.include_router(tracking_router)
app.include_router(sql_router)
app.include_router(ml_router)