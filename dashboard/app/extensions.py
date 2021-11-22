"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_babel import Babel

from app.api.commons.apispec import APISpecExt
from flask_login import LoginManager

login_manager = LoginManager()

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
apispec = APISpecExt()
babel = Babel()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
