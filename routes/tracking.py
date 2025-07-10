from fastapi import APIRouter
from database import SessionLocal
from sqlalchemy import text

router = APIRouter()

@router.get("/tracking")
def obtener_tracking():
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT TOP 100 id, email, evento, timestamp, delivery_code
            FROM tracking_eventos
            ORDER BY timestamp DESC
        """))
        eventos = [
            {
                "id": row.id,
                "email": row.email,
                "evento": row.evento,
                "timestamp": row.timestamp,
                "delivery_code": row.delivery_code
            }
            for row in result.fetchall()
        ]
        return eventos
    finally:
        db.close()
