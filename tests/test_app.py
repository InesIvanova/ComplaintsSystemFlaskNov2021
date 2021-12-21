import json

from flask_testing import TestCase

from config import create_app
from db import db


class TestApplication(TestCase):
    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        return create_app("config.TestApplicationConfiguration")

    def test_authentication_missing_auth_header_raises(self):
        # Arrange
        url_methods = [
            ("/complainers/complaints", "GET"),
            ("/complainers/complaints", "POST"),
            ("/complainers/complaints/1", "PUT"),
            ("/complainers/complaints/1", "DELETE"),
            ("/approvers/complaints/1/approve", "PUT"),
            ("/approvers/complaints/1/reject", "PUT"),
        ]

        # Act
        for url, method in url_methods:
            if method == "GET":
                resp = self.client.get(url)
            elif method == "POST":
                resp = self.client.post(url, data=json.dumps({}))
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}))
            else:
                resp = self.client.delete(url)

            # Assert
            assert resp.status_code == 400
            assert resp.json == {"message": "Invalid token"}

    def test_permission_required_endpoints_admin_access_raises(self):
        # Create complainer, create token for it and test all
        # ADMIN endpoints with complainer token -
        # they should return
        pass

