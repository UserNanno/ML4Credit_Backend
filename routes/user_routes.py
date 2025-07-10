from fastapi import APIRouter, Depends
from sqlalchemy import text
from database import SessionLocal
from auth.dependencies import get_current_user
from schemas.user_schemas import UserInfoResponseWithPermissions

router = APIRouter()


@router.get("/me", response_model=UserInfoResponseWithPermissions)
def get_current_user_data(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()

    result = db.execute(
        text("""
             SELECT p.name
             FROM role_permissions rp
                      JOIN permissions p ON rp.permission_id = p.id
             WHERE rp.role_id = :role_id
             """),
        {"role_id": current_user["role_id"]}
    )

    permissions = [row[0] for row in result]

    db.close()

    return {
        "id": current_user.get("sub"),
        "email": current_user.get("email"),
        "full_name": current_user.get("full_name", ""),
        "role_id": current_user.get("role_id"),
        "role_name": current_user.get("role_name"),
        "permissions": permissions
    }
