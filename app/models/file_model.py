from app import db

class FileModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(40), nullable=False, unique=True)
    file_hash = db.Column(db.String(40), nullable=False, unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user_model.id"), nullable=False) # file ownership by user id
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    owner = db.relationship("UserModel", backref="files") # allows to access all user files (user.files)

class SharedFileModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey("file_model.id"), nullable=False) # which file is shared
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"), nullable=False) # to which user file is shared
    access_level = db.Column(db.String(20), nullable=False, default="read") # read or write access

    file = db.relationship("FileModel", backref="shared_with") # all shares of this file (file.shared_with)
    user = db.relationship("UserModel", backref="shared_files", foreign_keys=[shared_with_user_id]) # all files shared with user (user.shared_files)
