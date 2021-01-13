from models.hospital import HospitalModel
from models.doctor import DoctorModel
import uuid
from flask_restful import Resource, reqparse, abort, request, inputs
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional

from models.user import UserModel


_patient_parser = reqparse.RequestParser()

_patient_parser.add_argument('name',
                             type=str,
                             required=True,
                             help="This field cannot be blank."
                             )

_patient_parser.add_argument('birthdate',
                             type=inputs.date,
                             required=True,
                             help="This field cannot be blank."
                             )

_patient_parser.add_argument('email',
                             type=str,
                             required=True,
                             help="This field cannot be blank."
                             )

_patient_parser.add_argument('phone_number',
                             type=str,
                             required=True,
                             help="This field cannot be blank."
                             )

_patient_parser.add_argument('address',
                             type=str,
                             required=True,
                             help="This field cannot be blank."
                             )

_patient_parser.add_argument('hospital_auth_id',
                             type=str,
                             required=True,
                             help="This field cannot be blank."
                             )


def get_or_abort_if_user_doesnt_exist(auth_user_id):
    user = UserModel.find_by_identification(auth_user_id)
    if user is None:
        abort(404, message="User {} doesn't exist".format(auth_user_id))
    return user


def get_or_abort_if_hospitals_doesnt_exist(hospital_user_auth_id):
    user = get_or_abort_if_user_doesnt_exist(hospital_user_auth_id)
    hospital = HospitalModel.find_by_user_id(user.id)
    if hospital is None:
        abort(404, message="Hospital {} doesn't exist".format(hospital_user_auth_id))
    return user


def validate_doctor_register(doctor_auth_id):
    data = _patient_parser.parse_args()
    hospital = get_or_abort_if_hospitals_doesnt_exist(data['hospital_auth_id'])
    return {
        'name': data['name'],
        'birthdate': data['birthdate'],
        'hospital_id': hospital.id,
    }, {
        'user_auth_id': doctor_auth_id,
        'email': data['email'],
        'password': str(uuid.uuid4()),
        'phone_number': data['phone_number'],
        'address': data['address']
    }


class DoctorResource(Resource):
    def __init__(self):
        from app import bcrypt
        self.bcrypt = bcrypt

    @jwt_required
    def post(self, doctor_user_auth_id):
        doctor_data, user_data = validate_doctor_register(doctor_user_auth_id)

        user_copy = user_data.copy()
        user_data['password'] = self.bcrypt.generate_password_hash(user_data['password'])
        new_user = UserModel(**user_data)
        new_user.save_to_db()

        doctor_data['user_id'] = new_user.id
        new_doctor = DoctorModel(**doctor_data)
        new_doctor.save_to_db()

        return {"message": "Doctor saved successfully.", "user": user_copy}, 201


class DoctorListResource(Resource):
    pass
