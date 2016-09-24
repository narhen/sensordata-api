#!/usr/bin/env python

from flask.ext.bcrypt import Bcrypt
from common.db import Storage
import mock
import unittest
from auth import Auth, AuthenticatedUser

class AuthTestCase(unittest.TestCase):

    def test_authenticate_success(self):
        username, password = "user", "pass"
        mock_storage = mock.create_autospec(Storage)
        mock_bcrypt = mock.create_autospec(Bcrypt)
        auth = Auth(mock_storage, mock_bcrypt)

        db_result = {"id": 1, "name": "Name", "password": "pass"}
        mock_storage.get_user_by_name_with_password.return_value = db_result
        mock_bcrypt.check_password_hash.return_value = True
        result = auth.authenticate(username, password)

        mock_storage.get_user_by_name_with_password.assert_called_with(username)
        mock_bcrypt.check_password_hash.assert_called_with(db_result["password"], password)

        self.assertIsInstance(result, AuthenticatedUser)

    def test_authenticate_failed_db_query(self):
        username, password = "user", "pass"
        mock_storage = mock.create_autospec(Storage)
        mock_bcrypt = mock.create_autospec(Bcrypt)
        auth = Auth(mock_storage, mock_bcrypt)

        mock_storage.get_user_by_name_with_password.return_value = None
        self.assertIsNone(auth.authenticate(username, password))

    def test_authenticate_wrong_password(self):
        username, password = "user", "incorrect password"
        mock_storage = mock.create_autospec(Storage)
        mock_bcrypt = mock.create_autospec(Bcrypt)
        auth = Auth(mock_storage, mock_bcrypt)

        db_result = {"id": 1, "name": "Name", "password": "correct password"}
        mock_storage.get_user_by_name_with_password.return_value = db_result
        mock_bcrypt.check_password_hash.return_value = False
        result = auth.authenticate(username, password)

        mock_storage.get_user_by_name_with_password.assert_called_with(username)
        mock_bcrypt.check_password_hash.assert_called_with(db_result["password"], password)

        self.assertIsNone(result)

    def test_identity_success(self):
        username, password = "user", "incorrect password"
        mock_storage = mock.create_autospec(Storage)
        mock_bcrypt = mock.create_autospec(Bcrypt)
        auth = Auth(mock_storage, mock_bcrypt)

        db_result = {"id": 1, "name": "Name"}
        mock_storage.get_user_by_id.return_value = db_result
        result = auth.identity({"identity": 1})

        mock_storage.get_user_by_id.assert_called_with(1)
        self.assertIsInstance(result, AuthenticatedUser)

    def test_identity_failed_db_query(self):
        username, password = "user", "incorrect password"
        mock_storage = mock.create_autospec(Storage)
        mock_bcrypt = mock.create_autospec(Bcrypt)
        auth = Auth(mock_storage, mock_bcrypt)

        mock_storage.get_user_by_id.return_value = None
        result = auth.identity({"identity": 1})

        mock_storage.get_user_by_id.assert_called_with(1)
        self.assertIsNone(result)
