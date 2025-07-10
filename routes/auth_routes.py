from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal
from auth.auth import verify_password, create_access_token
from schemas.user_schemas import LoginResponse
from sqlalchemy import text

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db: Session = SessionLocal()
    user = db.execute(
        text("""
             SELECT u.*, r.name AS role_name
             FROM users u
                      LEFT JOIN roles r ON u.role_id = r.id
             WHERE u.email = :email
             """),
        {"email": form_data.username}
    ).mappings().fetchone()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token_data = {
        "sub": str(user["id"]),
        "email": user["email"],
        "role_id": user["role_id"],
        "role_name": user["role_name"],
        "full_name": user["full_name"]
    }

    token = create_access_token(data=token_data)

    return LoginResponse(
        id=str(user["id"]),
        email=user["email"],
        full_name=user["full_name"],
        role_id=user["role_id"],
        role_name=user["role_name"],
        access_token=token
    )

