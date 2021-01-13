from models.medical_service import MedicalServiceModel
from models.hospital import HospitalModel
from flask_restful import Resource, reqparse, abort, request, inputs
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional

from models.user import UserModel


def get_or_abort_if_user_doesnt_exist(auth_user_id):
    user = UserModel.find_by_identification(auth_user_id)
    if user is None:
        abort(404, message="User {} doesn't exist".format(auth_user_id))
    return user


_hospital_parser = reqparse.RequestParser()

_hospital_parser.add_argument('name',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )

_hospital_parser.add_argument('address',
                              type=str,
                              required=True,
                              help="This field cannot be blank."
                              )

_hospital_parser.add_argument('medical_services',
                              type=dict,
                              required=True,
                              action='append',
                              help="This field cannot be blank."
                              )


def validate_hospital_register():
    data = _hospital_parser.parse_args()
    return data


def validate_medical_services(medical_services: list, hospital_id: int):
    try:
        new_medical_services = [MedicalServiceModel(**medical_service, hospital_id=hospital_id) for medical_service in medical_services]
    except Exception as e:
        print(f"Exception {e}")
        abort(400, message="Bad request, incorrect medical service data")

    return new_medical_services


class HospitalResource(Resource):
    def post(self, user_auth_id):
        user = get_or_abort_if_user_doesnt_exist(user_auth_id)
        hospital_data = validate_hospital_register()

        new_hospital = HospitalModel(name=hospital_data['name'], user_id=user.id)
        new_medical_services = validate_medical_services(hospital_data['medical_services'], new_hospital.id)

        user.update_address(hospital_data['address'])
        new_hospital.medical_services.extend(new_medical_services)
        new_hospital.save_to_db()

        return {"message": "Hospital data saved successfully."}, 201


class HospitalListResource(Resource):
    pass
