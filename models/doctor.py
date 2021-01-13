from db import db
from sqlalchemy.sql import expression


class DoctorModel(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel', uselist=False)

    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    hospital = db.relationship('HospitalModel', uselist=False)
