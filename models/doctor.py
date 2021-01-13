from db import db
from sqlalchemy.sql import expression
from datetime import date


class DoctorModel(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade', onupdate='cascade'))
    user = db.relationship('UserModel', uselist=False)

    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id', ondelete='cascade', onupdate='cascade'))
    hospital = db.relationship('HospitalModel', uselist=False)

    has_old_passwprd = db.Column(db.Boolean, server_default=expression.false(), nullable=False)

    medical_observations = db.relationship('MedicalObservationModel', lazy='dynamic')

    def __init__(self, name: str, user_id: int, hospital_id: int, birthdate: date):
        self.name = name
        self.user_id = user_id
        self.hospital_id = hospital_id
        self.birthdate = birthdate

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @ classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @ classmethod
    def find_by_userid(cls, _id):
        return cls.query.filter_by(user_id=_id).first()

    @ classmethod
    def find_all(cls):
        return [user.json() for user in cls.query.all()]
