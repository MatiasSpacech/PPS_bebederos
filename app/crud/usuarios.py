from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.usuario import Usuario


def get_by_email(db: Session, email: str) -> Usuario | None:
    statement = select(Usuario).where(Usuario.email == email)
    return db.scalar(statement)


def get_by_id(db: Session, user_id: int) -> Usuario | None:
    return db.get(Usuario, user_id)


def create_user(db: Session, user: Usuario) -> Usuario:
    db.add(user)
    db.flush()
    return user


def touch_last_access(db: Session, user: Usuario) -> Usuario:
    user.fecha_ultimo_acceso = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
