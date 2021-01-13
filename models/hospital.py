from db import db


class HospitalModel(db.Model):
    __tablename__ = "hospitals"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel", uselist=False)

    medical_services = db.relationship('MedicalServiceModel', lazy='dynamic')

    def __init__(self, name: str, user_id: str):
        self.name = name
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
