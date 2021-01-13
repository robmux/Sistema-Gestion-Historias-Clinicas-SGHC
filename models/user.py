from db import db
from sqlalchemy.sql import expression


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_auth_id = db.Column(db.String(255), unique=True)
    password = db.Column(db.Binary(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    phone_number = db.Column(db.String(255), unique=True)
    address = db.Column(db.String(255))

    is_active = db.Column(db.Boolean, server_default=expression.false(), nullable=False)

    def __init__(self, user_auth_id, email, password, phone_number, address=""):
        self.user_auth_id = user_auth_id
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.address = address

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'user_auth_id': self.user_auth_id,
            'email': self.email,
            'password': self.password,
            'phone_number': self.phone_number,
            'is_active': self.is_active,
        }

    def activate(self):
        self.is_active = True
        db.session.add(self)
        db.session.commit()

    def update_address(self, address):
        self.address = address
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_identification(cls, identification: str):
        return cls.query.filter_by(user_auth_id=str(identification)).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return [user.json() for user in cls.query.all()]
