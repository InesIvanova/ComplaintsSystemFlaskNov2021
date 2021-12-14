from marshmallow import fields, validate, Schema


class BaseComplaintSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(max=100))
    description = fields.String(required=True, validate=validate.Length(max=100))
    amount = fields.Float(required=True)
