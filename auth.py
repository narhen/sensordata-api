#!/usr/bin/env python

class AuthenticatedUser:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Auth:
    def __init__(self, storage, bcrypt):
        self.storage = storage
        self.bcrypt = bcrypt

    def identity(self, payload):
        user = self.storage.get_user_by_id(payload["identity"])
        return AuthenticatedUser(user['id'], user['name'])

    def authenticate(self, username, password):
        db_user = self.storage.get_user_by_name_with_password(username)
        if not db_user:
            return None

        if self.bcrypt.check_password_hash(db_user['password'], password):
            return AuthenticatedUser(db_user['id'], db_user['name'])
