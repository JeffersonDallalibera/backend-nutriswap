# services/tipo_alimento_service.py
from app import db
from app.models.alimento import Alimento

def get_alimentos_by_tipo(id_tipo_alimento):
    try:
        return Alimento.query.filter_by(tipo_alimento_id=id_tipo_alimento).all()
    except Exception as e:
        db.session.rollback()
        raise e
