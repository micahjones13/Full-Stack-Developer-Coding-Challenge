import datetime
from .__init__ import db
from marshmallow import fields, Schema
from .__init__ import bcrypt


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(125), nullable=False)

    def __init__(self, data):

        self.username = data.get('username')
        self.password = self.__generate_hash(data.get('password'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(value)
            setattr(self, key, item)

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_user_by_id(id):
        return UserModel.query.get(id)

    @staticmethod
    def get_user_by_username(username):
        return UserModel.query.filter_by(username=username).first()

    def __repr(self):
        return '<id {}>'.format(self.id)


class UserSchema(Schema):

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
