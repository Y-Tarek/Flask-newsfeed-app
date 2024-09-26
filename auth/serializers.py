""" Serialzier File for request fields validations """
from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()