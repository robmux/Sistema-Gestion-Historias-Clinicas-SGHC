from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional


# if UserModel.find_by_identification(data['user_auth_id']):
#     abort(404, message="User {} doesn't exist".format(data['user_auth_id']))


class PatientResource(Resource):
    pass


class PatientListResource(Resource):
    pass
