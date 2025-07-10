from auth.auth import hash_password
from sqlalchemy import text
from database import SessionLocal

## Datos del nuevo usuario
email = "t48130@gmail.com"
password = "root123"
full_name = "Mariano Canecillas"
role_id = 1


#email = "T45123@gmail.com"
#password = "root123"
#full_name = "Adrian Lizarbe"
#role_id = 2


hashed = hash_password(password)

db = SessionLocal()
db.execute(
    text("""
        INSERT INTO users (email, password_hash, full_name, role_id)
        VALUES (:email, :password_hash, :full_name, :role_id)
    """),
    {
        "email": email,
        "password_hash": hashed,
        "full_name": full_name,
        "role_id": role_id
    }
)
db.commit()
db.close()
