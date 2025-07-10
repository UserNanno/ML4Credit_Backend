# Backend/routes/ml_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from auth.dependencies import get_current_user
from pydantic import BaseModel
import requests
import pandas as pd
import json
from sqlalchemy import text

ml_router = APIRouter()

class CodigoClientes(BaseModel):
    codigos: list[str]
    tipo_modelo: str  # "clasificacion" o "regresion"

@ml_router.post("/ml/ejecutar_desde_bd")
def ejecutar_modelo_desde_bd(data: CodigoClientes, current_user: dict = Depends(get_current_user)):
    if not data.codigos:
        raise HTTPException(status_code=400, detail="No se proporcionaron códigos de cliente.")

    db: Session = SessionLocal()
    try:
        placeholders = ",".join([f":cod{i}" for i in range(len(data.codigos))])
        query = f"""
            SELECT GENERO, ESTADO_CIVIL, DESNIVELEDUCACIONAL2, CODFUENTEINGR,
                   DESCODDEPARTAMENTO, EDAD, MTOINGRESOSOL, CANT_ACTIVOS, CANT_PASIVOS,
                   CANT_SEGUROS, CANT_PRODUCTOS_XSELL, CANT_PRODUCTOS_VINC,
                   SALDO_PASIVO_U3M_RS, NUMSCORERIESGO_CEF, ctd_trx_hbk_prom_u3m,
                   ctd_trx_yape_prom_u3m, CTD_POS_PROM_U3M, CTD_ECOMMERCE_PROM_U3M,
                   FLG_CTAPLAZO, FLG_CTASUELDO, FLG_CTS, FLG_CTAAHORRO, FLG_CTA_CTE,
                   FLG_SEG_MULTIPLE
            FROM clientes
            WHERE codinternocliente IN ({placeholders})
        """

        params = {f"cod{i}": cod for i, cod in enumerate(data.codigos)}
        rows = db.execute(text(query), params).mappings().all()

        if not rows:
            raise HTTPException(status_code=404, detail="No se encontraron clientes.")

        df = pd.DataFrame(rows)
        if data.tipo_modelo == "clasificacion":
            url = "http://localhost:8002/ml/predecir"
        elif data.tipo_modelo == "regresion":
            url = "http://localhost:8002/ml/predecir_monto"
        else:
            raise HTTPException(
                status_code=400,
                detail="Tipo de modelo inválido. Usa 'clasificacion' o 'regresion'."
            )

        ml_response = requests.post(url, json=json.loads(df.to_json(orient="records")))

        if ml_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error al ejecutar modelo ML")

        return ml_response.json()

    finally:
        db.close()
