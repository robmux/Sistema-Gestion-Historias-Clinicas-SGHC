from db import db
from datetime import date


class PatientModel(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel", uselist=False)

    def __init__(self, name: str, birthdate: date, user_id: int) -> None:
        self.name = name
        self.birthdate = birthdate
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_identification(cls, identification: str) -> "PatientModel":
        return cls.query.filter_by(user_auth_id=identification).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "PatientModel":
        return cls.query.filter_by(id=_id).first()
