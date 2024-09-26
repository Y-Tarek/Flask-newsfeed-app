""" Serialzier File for request fields validations """
from marshmallow import Schema, fields, validate
from auth.serializers import UserSchema

class PostShema(Schema):
    content = fields.String(required=True)

class CommentSchema(Schema):
    content = fields.String()
    username = fields.String()


class ReadPostSchema(Schema):
    id = fields.Integer()
    content = fields.String()
    author = fields.Nested(UserSchema)
    likes = fields.Integer()
    comments = fields.List(fields.Nested(CommentSchema))

class PostCommentSchema(Schema):
    post_id = fields.Integer()
    content = fields.String()