from db import db


class MedicalObservationModel(db.Model):
    __tablename__ = 'medical_observation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    health_state = db.Column(db.Text, nullable=False)

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    patient = db.relationship('PatientModel', uselist=False)

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    doctor = db.relationship('DoctorModel', uselist=False)

    medical_service_id = db.Column(db.Integer, db.ForeignKey('medical_services.id'))
    medical_service = db.relationship('DoctorModel', uselist=False)

    def __init__(self, title, description, health_state, patient_id: int, doctor_id: int, medical_service_id: int) -> None:
        self.title = title
        self.description = description
        self.health_state = health_state
        self.patient_id = patient_id
        self.doctor_id = doctor_id

    def json(self):
        return {
            'title': self.title,
            'description': self.description,
            'health_state': self.health_state,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
