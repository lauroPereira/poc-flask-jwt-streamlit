from datetime import datetime, UTC
from . import db

class BaseModel(db.Model):
    __abstract__ = True  # Não cria tabela para esta classe

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))