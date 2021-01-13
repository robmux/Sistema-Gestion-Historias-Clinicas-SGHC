import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from db import db
from resources.user import UserListResource, UserRegisterResource, UserLoginResource, UserResource
from resources.hospital import HospitalResource, HospitalListResource
from resources.patient import PatientResource, PatientListResource
from resources.doctor import DoctorResource, DoctorListResource
from resources.medical_observation import MedicalObservationResource, MedicalObservationListResource
from config import Config, ProductionConfig, DevelopmentConfig

app = Flask(__name__)
environment_configuration = os.environ['CONFIGURATION_SETUP']
app.config.from_object(environment_configuration)

bcrypt = Bcrypt(app)
api = Api(app)

"""
JWT related configuration. The following functions includes:
1) add claims to each jwt
2) customize the token expired error message 
"""
jwt = JWTManager(app)

"""
`claims` are data we choose to attach to each jwt payload
and for each jwt protected endpoint, we can retrieve these claims via `get_jwt_claims()`
one possible use case for claims are access level control, which is shown below
"""


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # instead of hard-coding, we should read from a config file to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401

# JWT configuration ends


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(HospitalListResource, '/hospitals')
api.add_resource(HospitalResource, '/hospitals/<string:user_auth_id>')

api.add_resource(DoctorListResource, '/doctors')
api.add_resource(DoctorResource, '/doctors/<string:doctor_user_auth_id>')

api.add_resource(PatientListResource, '/patients')
api.add_resource(PatientResource, '/patients/<string:user_auth_id>')

api.add_resource(MedicalObservationListResource, '/patients//<string:patient_user_auth_id>/medical_observations')
api.add_resource(MedicalObservationResource, '/patients//<string:patient_user_auth_id>/medical_observations')

# Auth
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<string:user_auth_id>')
api.add_resource(UserRegisterResource, '/register')
api.add_resource(UserLoginResource, '/login')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
