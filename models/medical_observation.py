from db import db


class MedicalObservationModel(db.Model):
    __tablename__ = 'medical_observation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    health_state = db.Column(db.Text, nullable=False)

    patient_id = db.Column(db.Integer, db.Foreignkey('patients.id'))
    patient = db.relationship('PatientModel', uselist=False)

    doctor_id = db.Column(db.Integer, db.Foreignkey('doctors.id'))
    doctor = db.relationship('DoctorModel', uselist=False)

    medical_service_id = db.Column(db.Integer, db.Foreignkey('medical_services.id'))
    medical_service = db.relationship('DoctorModel', uselist=False)
