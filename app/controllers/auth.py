from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.user_model import UserModel
from app.schemas.user_schema import AuthResponseSchema, AuthSchema, UserSchema
from flask_jwt_extended import create_access_token

bp = Blueprint("auth", __name__)

@bp.route("/auth/register")
class Register(MethodView):
    # Create user
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

        return user

@bp.route("/auth/login")
class Login(MethodView):
    # Login and get access token
    @bp.arguments(AuthSchema)
    @bp.response(200, AuthResponseSchema)
    @bp.doc(description="Login and receive access token.")
    def post(self, user_data):
        
        # Get user by it's username
        user = UserModel.query.filter_by(username=user_data["username"]).first()
        if not user:
            abort(404, message="User not found.")

        # Check credentials
        if not user.check_password(user_data["password"]):
            abort(401, message="Invalid credentials.")

        access_token = create_access_token(identity=str(user.id))
        return {"access_token": access_token}

