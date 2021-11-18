from app.admin.base.models.config import ConfigTable
from app.extensions import ma, db


class ConfigSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    key = ma.String(dump_only=True)

    class Meta:
        model = ConfigTable
        sqla_session = db.session
        load_instance = True


class ConfigPostSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)

    class Meta:
        model = ConfigTable
        sqla_session = db.session
        load_instance = True
