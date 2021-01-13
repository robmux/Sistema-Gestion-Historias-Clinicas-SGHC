from db import db


class PatientModel(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.Foreignkey("users.id"))
    user = db.relationship("UserModel", uselist=False)
