from flask import request
from flask_restful import Resource

from managers.auth import AuthManager
from managers.user import UserManager
from schemas.request.user import (
    ComplainerRegisterRequestSchema,
    ComplainerLoginRequestSchema,
    ApproverLoginRequestSchema,
)
from util.decorators import validate_schema


class Register(Resource):
    @validate_schema(ComplainerRegisterRequestSchema)
    def post(self):
        user = UserManager.register(request.get_json())
        token = AuthManager.encode_token(user)
        return {"token": token}, 201


class Login(Resource):
    @validate_schema(ComplainerLoginRequestSchema)
    def post(self):
        user = UserManager.login(request.get_json())
        token = AuthManager.encode_token(user)
        return {"token": token, "role": "complainer"}, 200


class LoginApprover(Resource):
    @validate_schema(ApproverLoginRequestSchema)
    def post(self):
        user = UserManager.login_approver(request.get_json())
        token = AuthManager.encode_token(user)
        return {"token": token, "role": "approver"}, 200
