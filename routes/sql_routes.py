from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from auth.dependencies import get_current_user
from pydantic import BaseModel
from sqlalchemy import text

router = APIRouter()

class SQLQuery(BaseModel):
    consulta: str

@router.post("/sql/ejecutar")
def ejecutar_consulta(data: SQLQuery, current_user: dict = Depends(get_current_user)):
    # solo permitir SELECT
    if not data.consulta.strip().lower().startswith("select"):
        raise HTTPException(status_code=403, detail="Solo se permiten consultas SELECT")

    db: Session = SessionLocal()
    try:
        resultado = db.execute(text(data.consulta)).mappings().fetchall()
        return [dict(row) for row in resultado]
    except Exception as e:
        print("❌ Error ejecutando consulta SQL:", e)
        raise HTTPException(status_code=400, detail="Consulta inválida o error de ejecución")
    finally:
        db.close()

@router.get("/sql/metadata")
def obtener_metadata(current_user: dict = Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        bases = []
        # Solo usaremos la base actual (puedes extender luego)
        tablas = db.execute(text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")).fetchall()
        lista_tablas = [t[0] for t in tablas]
        bases.append({"base": "ML4Credit", "tablas": lista_tablas})
        return bases
    finally:
        db.close()
