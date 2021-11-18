from app.admin.base.models.proxy import ProxyTable
from app.extensions import ma, db


class ProxySchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = ProxyTable
        sqla_session = db.session
        load_instance = True
