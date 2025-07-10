# routes/clientes_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
from auth.dependencies import get_current_user

router = APIRouter()

@router.get("/clientes")
def listar_clientes(current_user: dict = Depends(get_current_user)):
    db: Session = SessionLocal()

    result = db.execute(text("""
        SELECT id, dni, nombres, apellidos, correo, estado
        FROM clientes
        ORDER BY id
    """)).mappings().all()

    db.close()

    if current_user["role_name"] == "Admin":
        return list(result)

    elif current_user["role_name"] == "Analyst":
        return [
            {
                "id": r["id"],
                "nombres": r["nombres"],
                "apellidos": r["apellidos"],
                "estado": r["estado"]
            }
            for r in result
        ]
    else:
        raise HTTPException(status_code=403, detail="Rol no autorizado")


