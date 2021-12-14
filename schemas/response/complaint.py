from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from models.enums import State
from schemas.bases import BaseComplaintSchema


class ComplaintCreateResponseSchema(BaseComplaintSchema):
    id = fields.Integer(required=True)
    photo_url = fields.String(required=True, validate=validate.Length(max=255))
    create_on = fields.DateTime(required=True)
    status = EnumField(State, by_value=True)
