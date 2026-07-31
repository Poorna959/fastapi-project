from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy import text
from .config import settings

DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)





engine = create_engine(DATABASE_URL)
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("✅ Database connected successfully")
except Exception as e:
    print("❌ Database connection failed")
    print(e)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()