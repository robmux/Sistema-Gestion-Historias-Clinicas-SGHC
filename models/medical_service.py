from db import db


class MedicalServiceModel(db.Model):
    __tablename__ = 'medical_services'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    hospital = db.relationship('HospitalModel', uselist=False)
