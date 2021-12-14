from marshmallow import fields

from schemas.bases import BaseComplaintSchema


class ComplaintCreateRequestSchema(BaseComplaintSchema):
    photo = fields.String(required=True)
    photo_extension = fields.String(required=True)
