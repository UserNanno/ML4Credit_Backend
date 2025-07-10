from sqlalchemy import text
from database import SessionLocal

def test_conexion():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        print("Conexión exitosa:", result)
    except Exception as e:
        print("Error en la conexión:", e)
    finally:
        db.close()

test_conexion()
