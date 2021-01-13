from db import db
from sqlalchemy.sql import expression


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_auth_id = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    address = db.Column(db.String(255))

    is_active = db.Column(db.Boolean, server_default=expression.true(), nullable=False)

    doctor = db.relationship("DoctorModel", uselist=False, backref="users")
