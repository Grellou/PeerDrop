from marshmallow import Schema, fields, validate

class FileSchema(Schema):
    id = fields.Int(dump_only=True)
    file_name = fields.Str(required=True)
    file_hash = fields.Str(required=True)
    ipfs_hash = fields.Str(required=False)
    owner_id = fields.Int(required=True)
    is_public = fields.Bool(required=True)
    created_at = fields.DateTime(dump_only=True)

class SharedFileSchema(Schema):
    id = fields.Int(dump_only=True)
    file_id = fields.Int(required=True)
    shared_with_user_id = fields.Int(required=True)
    access_level = fields.Str(required=True, validate=validate.OneOf(["read", "write"]))
