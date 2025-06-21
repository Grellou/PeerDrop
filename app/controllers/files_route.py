from flask import request, current_app
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.file_schema import FileSchema

bp = Blueprint("files", __name__)

@bp.route("/files/upload")
class FileUpload(MethodView):
    # Upload file
    @jwt_required()
    @bp.response(201, FileSchema)
    def post(self):
        uploaded_file = request.files.get("file")
        


