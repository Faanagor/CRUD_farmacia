from sqlalchemy.orm import Session
from app.db.session import engine, Base


def init_db():
    # Crear las tablas definidas en los modelos
    Base.metadata.create_all(bind=engine)
