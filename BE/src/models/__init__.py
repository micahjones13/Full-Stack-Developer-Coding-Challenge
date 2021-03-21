from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy
from src.models.UserModel import *
# from . import UserModel
# from .UserModel import UserSchema
from .UserModel import *

db = SQLAlchemy()

bcrypt = Bcrypt()
