from config import Contants
from flask_restful import Resource, reqparse, abort, request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)

from models.user import UserModel
_user_parser = reqparse.RequestParser()

_user_parser.add_argument('user_type',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )

_user_parser.add_argument('user_auth_id',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )

_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )

_user_parser.add_argument('phone_number',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )

_user_login_parser = reqparse.RequestParser()

_user_login_parser.add_argument('user_auth_id',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )
_user_login_parser.add_argument('password',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )


def get_or_abort_if_user_doesnt_exist(auth_user_id):
    user = UserModel.find_by_identification(auth_user_id)
    if user is None:
        abort(404, message="User {} doesn't exist".format(auth_user_id))
    return user


def validate_register(base_parser_copy: reqparse.RequestParser):
    register_parser = base_parser_copy.copy()
    data = register_parser.parse_args()

    if data['user_type'] not in Contants.USER_TYPES:
        abort(400, message="Invalid user type {} ".format(data['user_type']))
    return {'user_auth_id': data['user_auth_id'],
            'email': data['email'],
            'password': data['password'],
            'phone_number': data['phone_number']}


class UserRegisterResource(Resource):
    def __init__(self):
        from app import bcrypt
        self.bcrypt = bcrypt

    def post(self):

        data = validate_register(_user_parser)
        data['password'] = self.bcrypt.generate_password_hash(data['password'])
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLoginResource(Resource):

    def __init__(self):
        from app import bcrypt
        self.bcrypt = bcrypt

    def post(self):
        data = _user_login_parser.parse_args()

        user = UserModel.find_by_identification(data['user_auth_id'])

        if user and self.bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {"message": "Invalid Credentials!"}, 401


class UserResource(Resource):

    def get(self, user_auth_id: int):
        user = get_or_abort_if_user_doesnt_exist(user_auth_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        return user.json(), 200

    def delete(self, user_auth_id: int):
        user = get_or_abort_if_user_doesnt_exist(user_auth_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200

    def patch(self, user_auth_id):
        user = get_or_abort_if_user_doesnt_exist(user_auth_id)
        is_confirming = True if 'confirm_request' in request.args and request.args['confirm_request'] == '1' else False
        sent_email = request.args['email'] if 'email' in request.args else str(None)

        if is_confirming:
            if safe_str_cmp(user.email, sent_email):
                user.activate()
            else:
                abort(400, message=f"Incorrect email {sent_email}")

        return {'message': 'User updated.'}, 200


class UserListResource(Resource):
    def get(self):
        return {'users': UserModel.find_all()}, 200
