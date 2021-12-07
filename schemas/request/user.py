from marshmallow import Schema, fields, validate


class BaseUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=255))


class ComplainerLoginRequestSchema(BaseUserSchema):
    pass


class ApproverLoginRequestSchema(BaseUserSchema):
    pass


class ComplainerRegisterRequestSchema(BaseUserSchema):
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    phone = fields.String(required=True, validate=validate.Length(min=13, max=13))
    iban = fields.String(required=True, validate=validate.Length(min=22, max=22))
