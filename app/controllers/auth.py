from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.user_model import UserModel
from app.schemas.user_schema import AuthResponseSchema, AuthSchema, UserSchema

bp = Blueprint("auth", __name__)

# Register route
@bp.route("/auth/register")
class Register(MethodView):
    @bp.arguments(UserSchema)
    @bp.response(200, UserSchema)
    @bp.doc(description="Register user.")
    def post(self, user_data):
        
        # Check if username or email already exists
        username = UserModel.query.filter_by(username=user_data["username"]).first()
        email = UserModel.query.filter_by(username=user_data["email_address"]).first()
        if username or email:
            abort(409, message="User with such username or email address already exists.")

        # Create account
        user = UserModel(username=user_data["username"], email_address=user_data["email_address"]) #type: ignore
        user.set_password(user_data["password"])

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as error:
            abort(500, message=f"Error occurred while registering user: {str(error)}")

        return {"message": "User registered."}
