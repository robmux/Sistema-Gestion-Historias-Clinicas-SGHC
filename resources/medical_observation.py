from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional


class MedicalObservationResource(Resource):
    pass


class MedicalObservationListResource(Resource):
    pass
