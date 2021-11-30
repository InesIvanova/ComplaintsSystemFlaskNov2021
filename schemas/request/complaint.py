from marshmallow import Schema, fields, validate


class ComplaintCreateRequestSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(max=100))
    description = fields.String(required=True, validate=validate.Length(max=100))
    photo_url = fields.String(required=True, validate=validate.Length(max=255))
    amount = fields.Float(required=True)
