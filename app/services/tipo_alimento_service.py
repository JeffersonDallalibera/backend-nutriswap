# services/tipo_alimento_service.py
from app import db
from app.models.tipo_alimento import TipoAlimento;


def get_all_tipo_alimento():
    try:
        tipos = TipoAlimento.query.all()
        return tipos
    except Exception as e:
        db.session.rollback()
        raise e
