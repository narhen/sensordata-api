import json
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from errors import UserAlreadyExists

class UserController(Resource):
    def __init__(self, storage=None, bcrypt=None):
        self.storage = storage
        self.bcrypt = bcrypt

    @jwt_required()
    def get(self):
        return self.storage.get_user_by_id(current_identity.id)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True, help="could not parse username")
        parser.add_argument("password", type=str, required=True, help="could not parse password")
        args = parser.parse_args()

        user = self._new_user(args.username, args.password)
        if not user:
            raise UserAlreadyExists("User with name '%s' already exists!" % args.username)
        return user

    def _new_user(self, username, plaintext_password):
        hashed_password = self.bcrypt.generate_password_hash(plaintext_password)
        return self.storage.new_user(username, plaintext_password)
