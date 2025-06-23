import os
from flask import request, current_app, send_from_directory
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.file_model import FileModel, SharedFileModel
from app.models.user_model import UserModel
from app.schemas.file_schema import FileSchema, SharedFileSchema
from app.utils.file_utils import hash_file, permission_to_download_file
from app import db
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint("files", __name__)

@bp.route("/files/upload")
class FileUpload(MethodView):
    # Upload file
    @jwt_required()
    @bp.response(201, FileSchema)
    def post(self):

        # Check for uploaded file
        uploaded_file = request.files.get("file")
        if not uploaded_file or not uploaded_file.filename:
            abort(404, message="File not found.")
        
        # Save file
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True) # create dir, no error if dir already exists
        file_path = os.path.join(upload_folder, uploaded_file.filename)
        uploaded_file.save(file_path)
        
        # Hash file & file owner
        file_hash = hash_file(file_path)
        owner_id = int(get_jwt_identity())

        # Check for duplicate file hash
        existing_hash = FileModel.query.filter_by(file_hash=file_hash).first()
        if existing_hash:
            abort(400, message="File with this content already exists.")

        # Store metadata in db
        file_data = FileModel(file_name=uploaded_file.filename, file_hash=file_hash, owner_id=owner_id, is_public=True) # type: ignore
        try:
            db.session.add(file_data)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(500, message=f"Adding file data to database failed due to error: {str(error)}")
        
        return file_data

@bp.route("/files/<int:file_id>")
class FileId(MethodView):
    # Download file
    @jwt_required()
    def get(self, file_id):

        # Collect file data and user data
        file_data = FileModel.query.get_or_404(file_id)
        user_id = int(get_jwt_identity())

        # Permisions
        if not permission_to_download_file(file_data, user_id):
            abort(403, message="You don't have permissions to access this file.")
        
        # Download
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        return send_from_directory(upload_folder, file_data.file_name, as_attachment=True)
    
    # Delete file
    @jwt_required()
    def delete(self, file_id):
        
        # Get file and current user's ID
        file_data = FileModel.query.get_or_404(file_id)
        user_id = int(get_jwt_identity())
        
        # Check permissions for file deletion
        if user_id != file_data.owner_id and user_id != 1:
            abort(403, message="Insufficient permissions.")

        try:
            db.session.delete(file_data)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(500, message=f"Deleting file data from database failed due to error: {str(error)}")
        return "", 204 # no content

@bp.route("/files")
class FileList(MethodView):
    # List user's files
    @bp.response(200, FileSchema(many=True))
    @bp.doc(description="List of user's owned files.")
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        files_owned = FileModel.query.filter_by(owner_id=user_id).all()
        if not files_owned:
            return [], 200
        return files_owned

@bp.route("/files/share")
class FileShare(MethodView):
    # Share file with user
    @bp.arguments(SharedFileSchema)
    @bp.response(200, SharedFileSchema)
    @bp.doc(description="Share file with other user.")
    @jwt_required()
    def post(self, file_data):
        
        file_id = file_data["file_id"]
        shared_with_user_id = file_data["shared_with_user_id"]
        access_level = file_data["access_level"]

        # Check if file exists
        file = FileModel.query.get_or_404(file_id)

        # Permissions
        current_user_id = int(get_jwt_identity())
        if current_user_id != file.owner_id and current_user_id != 1:
            abort(403, message="Insufficient permissions.")

        # Check if target user exists
        target_user = UserModel.query.get_or_404(shared_with_user_id) # noqa

        # Prevent duplicate shares
        existing_share = SharedFileModel.query.filter_by(file_id=file_id, shared_with_user_id=shared_with_user_id).first()
        if existing_share:
            abort(409, message="File already shared with this user.")

        # Add to database
        shared_file = SharedFileModel(file_id=file_id, shared_with_user_id=shared_with_user_id, access_level=access_level) # type: ignore
        try:
            db.session.add(shared_file)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(500, message=f"Adding file data to database failed due to error: {str(error)}")

        return shared_file

