from db import db


class HospitalModel(db.Model):
    __tablename__ = 'hospitals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='cascade', onupdate='cascade'))
    user = db.relationship("UserModel", uselist=False)

    medical_services = db.relationship('MedicalServiceModel', lazy='dynamic')

    doctors = db.relationship('DoctorModel', lazy='dynamic')

    def __init__(self, name: str, user_id: str):
        self.name = name
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, user_id: str):
        return cls.query.filter_by(user_id=str(user_id)).first()

    @ classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @ classmethod
    def find_all(cls):
        return [user.json() for user in cls.query.all()]
