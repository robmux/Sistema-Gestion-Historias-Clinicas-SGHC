from models.medical_observation import MedicalObservationModel
from models.doctor import DoctorModel
from models.medical_service import MedicalServiceModel
from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from models.user import UserModel


def get_or_abort_if_user_doesnt_exist(auth_user_id):
    user = UserModel.find_by_identification(auth_user_id)
    if user is None:
        abort(404, message="User {} doesn't exist".format(auth_user_id))
    return user


def get_or_abort_if_medical_service_doesnt_exist(medical_service_id):
    user = MedicalServiceModel.find_by_identification(medical_service_id)
    if user is None:
        abort(404, message="Medical Service {} doesn't exist".format(medical_service_id))
    return user


_medical_observation_parser = reqparse.RequestParser()

_medical_observation_parser.add_argument('medical_service_id',
                                         type=int,
                                         required=True,
                                         help="This field cannot be blank."
                                         )

_medical_observation_parser.add_argument('title',
                                         type=str,
                                         required=True,
                                         help="This field cannot be blank."
                                         )
_medical_observation_parser.add_argument('description',
                                         type=int,
                                         required=True,
                                         help="This field cannot be blank."
                                         )
_medical_observation_parser.add_argument('health_state',
                                         type=str,
                                         required=True,
                                         help="This field cannot be blank."
                                         )


def validate_create():
    data = _medical_observation_parser.parse_args()
    get_or_abort_if_medical_service_doesnt_exist(data['medical_service_id'])
    return data


class MedicalObservationResource(Resource):
    @jwt_required
    def post(self, patient_user_auth_id):
        identity = get_jwt_identity()
        doctor = DoctorModel.find_by_userid(identity)
        if doctor:
            data = validate_create()
            patient = get_or_abort_if_user_doesnt_exist(patient_user_auth_id)

            data = {
                'title': data['title'],
                'description': data['description'],
                'health_state': data['health_state'],
                'patient_id': patient.id,
                'doctor_id': doctor.id,
            }
            new_observation = MedicalObservationModel(data)
            new_observation.save_to_db()

            return new_observation.json(), 201
        else:
            abort(401, message="User is not authorized")
