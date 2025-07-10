from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from auth.dependencies import get_current_user
from schemas.campania_schema import CampaniaCreate, CampaniaOut
from sqlalchemy import text

router = APIRouter()

@router.get("/campanias")
def listar_campanias(nombre: str = "", current_user: dict = Depends(get_current_user)):
    with SessionLocal() as db:
        if nombre:
            result = db.execute(
                text("SELECT * FROM campanias WHERE nombre LIKE :nombre"),
                {"nombre": f"%{nombre}%"}
            ).mappings().fetchall()
        else:
            result = db.execute(
                text("SELECT * FROM campanias")
            ).mappings().fetchall()
        return [dict(row) for row in result]




@router.post("/campanias", response_model=CampaniaOut)
def crear_campania(data: CampaniaCreate, current_user: dict = Depends(get_current_user)):
    with SessionLocal() as db:
        try:
            result = db.execute(
                text("""
                    INSERT INTO campanias (nombre, ultima_actualizacion, duracion, estrategia, estado, created_by)
                    OUTPUT inserted.*
                    VALUES (:nombre, :ultima_actualizacion, :duracion, :estrategia, :estado, :created_by)
                """),
                {
                    "nombre": data.nombre,
                    "ultima_actualizacion": data.ultima_actualizacion,
                    "duracion": data.duracion,
                    "estrategia": data.estrategia,
                    "estado": data.estado or "Activo",
                    "created_by": current_user["sub"]
                }
            ).mappings().fetchone()
            db.commit()
            return result
        except Exception as e:
            print("Error al crear campaña:", e)
            raise HTTPException(status_code=500, detail="Error al insertar campaña")

@router.put("/campanias/{id}", response_model=CampaniaOut)
def actualizar_campania(id: int, data: CampaniaCreate, current_user: dict = Depends(get_current_user)):
    print("🟡 Data recibida en PUT:", data.dict())  # << DEBUG
    with SessionLocal() as db:
        result = db.execute(
            text("""
                UPDATE campanias
                SET nombre = :nombre,
                    ultima_actualizacion = :ultima_actualizacion,
                    duracion = :duracion,
                    estrategia = :estrategia,
                    estado = :estado
                OUTPUT inserted.*
                WHERE id = :id
            """),
            {
                "id": id,
                "nombre": data.nombre,
                "ultima_actualizacion": data.ultima_actualizacion,
                "duracion": data.duracion,
                "estrategia": data.estrategia,
                "estado": data.estado
            }
        ).mappings().fetchone()
        db.commit()
        if not result:
            raise HTTPException(status_code=404, detail="Campaña no encontrada")
        return result


@router.delete("/campanias/{id}")
def eliminar_campania(id: int, current_user: dict = Depends(get_current_user)):
    with SessionLocal() as db:
        result = db.execute(
            text("DELETE FROM campanias OUTPUT deleted.* WHERE id = :id"),
            {"id": id}
        ).fetchone()
        db.commit()
        if not result:
            raise HTTPException(status_code=404, detail="Campaña no encontrada")
        return {"message": "Campaña eliminada correctamente"}
