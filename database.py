from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DB_SERVER = 'USERNANNO'
DB_NAME = 'ML4Credit'
DB_USER = 'T48130'
DB_PASSWORD = 'passpwd!'
DRIVER = 'ODBC Driver 17 for SQL Server'

DATABASE_URL = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
    f"?driver={DRIVER.replace(' ', '+')}&charset=utf8"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
