from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from models.enums import State


class ComplaintCreateResponseSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True, validate=validate.Length(max=100))
    description = fields.String(required=True, validate=validate.Length(max=100))
    photo_url = fields.String(required=True, validate=validate.Length(max=255))
    amount = fields.Float(required=True)
    create_on = fields.DateTime(required=True)
    status = EnumField(State, by_value=True)
