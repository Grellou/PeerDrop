from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email_address = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class AuthSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class AuthResponseSchema(Schema):
    access_token = fields.Str()
