from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import BadRequest

from models.user import ComplainerModel, AdministratorModel, ApproverModel

mapper = {
    ComplainerModel: lambda x: ComplainerModel.query.filter_by(id=x),
    ApproverModel: lambda x: ApproverModel.query.filter_by(id=x),
    AdministratorModel: lambda x: AdministratorModel.query.filter_by(id=x),
}


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(days=100),
            "role": user.__class__.__name__,
        }
        return jwt.encode(payload, key=config("JWT_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            data = jwt.decode(token, key=config("JWT_KEY"), algorithms=["HS256"])
            return data["sub"], data["role"]
        except jwt.ExpiredSignatureError:
            raise BadRequest("Token expired")
        except jwt.InvalidTokenError:
            raise BadRequest("Invalid token")


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    user_id, role = AuthManager.decode_token(token)
    # user = mapper[role](user_id)
    user = eval(f"{role}.query.filter_by(id={user_id}).first()")
    return user
