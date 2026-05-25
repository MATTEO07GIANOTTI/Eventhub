from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    full_name = fields.String(required=True)
    city = fields.String(required=False)


class EventSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    category = fields.String(required=True)
    city = fields.String(required=True)
    venue = fields.String(required=True)
    date = fields.DateTime(required=True)
    price = fields.Float(required=True)
    capacity = fields.Integer(required=True, validate=validate.Range(min=1))


class ReviewSchema(Schema):
    rating = fields.Integer(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.String(required=True, validate=validate.Length(min=5))
