import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Les infos de connexion viennent des variables d'environnement
# (docker-compose en local, ConfigMap + Secret dans Kubernetes)
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "antigaspi")
DB_USER = os.getenv("DB_USER", "antigaspi")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

if DB_HOST:
    DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    # Sans DB_HOST, on utilise un petit fichier SQLite pour tester sans Docker
    DATABASE_URL = "sqlite:///./antigaspi.db"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()