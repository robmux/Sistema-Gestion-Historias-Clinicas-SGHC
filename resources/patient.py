from flask_restful import Resource, reqparse, abort, request, inputs

from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional

from models.user import UserModel
from models.patient import PatientModel


def get_or_abort_if_user_doesnt_exist(auth_user_id):
    user = UserModel.find_by_identification(auth_user_id)
    if user is None:
        abort(404, message="User {} doesn't exist".format(auth_user_id))
    return user


_patient_parser = reqparse.RequestParser()

_patient_parser.add_argument('name',
                             type=str,
                             required=True,
                             help="This field cannot be blank."
                             )

_patient_parser.add_argument('address',
                             type=str,
                             required=True,
                             help="This field cannot be blank."
                             )

_patient_parser.add_argument('birthdate',
                             type=inputs.date,
                             required=True,
                             help="This field cannot be blank."
                             )


def validate_patient_register():
    data = _patient_parser.parse_args()

    return {
        'name': data['name'],
        'birthdate': data['birthdate'],
    }, data['address']


class PatientResource(Resource):
    def post(self, user_auth_id):
        user = get_or_abort_if_user_doesnt_exist(user_auth_id)
        patient_data, address = validate_patient_register()

        patient_data['user_id'] = user.id
        new_patient = PatientModel(**patient_data)

        user.update_address(address)
        new_patient.save_to_db()

        return {"message": "Patient data saved successfully."}, 201
