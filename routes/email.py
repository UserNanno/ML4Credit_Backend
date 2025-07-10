from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import uuid
import requests
from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy import text

router = APIRouter()

EMAIL_SERVICE_URL = "http://localhost:8003/enviar-email"

# microservicio

class CampaniaEmail(BaseModel):
    asunto: str
    html: str
    destinatarios: List[str]
    usuario: str

@router.post("/campania-email/enviar")
def enviar_campania(campania: CampaniaEmail):
    delivery_code = str(uuid.uuid4())

    # Llamar al microservicio
    try:
        response = requests.post(EMAIL_SERVICE_URL, json={
            "to": campania.destinatarios,
            "subject": campania.asunto,
            "html": campania.html,
            "delivery_code": delivery_code,
            "usuario": campania.usuario
        })
        response.raise_for_status()
    except Exception as e:
        return {"error": f"No se pudo enviar el correo: {e}"}

    # Guardar historial (opcional si ya lo guarda el microservicio)
    try:
        db: Session = SessionLocal()
        db.execute(text("""
            INSERT INTO historial_campanias_email (
                delivery_code, asunto, contenido_html,
                cantidad_destinatarios, destinatarios, usuario
            )
            VALUES (:d, :a, :h, :n, :l, :u)
        """), {
            "d": delivery_code,
            "a": campania.asunto,
            "h": campania.html,
            "n": len(campania.destinatarios),
            "l": ",".join(campania.destinatarios),
            "u": campania.usuario
        })
        db.commit()
    finally:
        db.close()

    return {"status": "ok", "delivery_code": delivery_code}
