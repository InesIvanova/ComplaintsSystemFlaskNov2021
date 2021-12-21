import json

from flask_testing import TestCase

from config import create_app
from db import db
from models import ComplainerModel, RoleType
from tests.helpers import object_as_dict


class TestAuth(TestCase):
    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestApplicationConfiguration")

    def test_register_complainer(self):
        """
        Test if a complainer is in database when register endpoint is hit.
        Assure that the role assign is a Complainer role.
        """
        url = "/register"

        data = {
            "email": "test@test.com",
            "password": "123456",
            "first_name": "Test",
            "last_name": "Testov",
            "phone": "1234567890123",
            "iban": "BNBG966110203456781234",
        }

        complainers = ComplainerModel.query.all()
        assert len(complainers) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        assert resp.status_code == 201
        assert "token" in resp.json
        complainers = ComplainerModel.query.all()
        assert len(complainers) == 1
        complianer = object_as_dict(complainers[0])
        complianer.pop("password")
        data.pop("password")

        assert complianer == {
            "id": complianer["id"],
            "role": RoleType.complainer,
            **data,
        }
