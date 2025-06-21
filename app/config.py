import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev118")

    # Db configs
    SQLALCHEMY_DATABASE_URI = "sqlite:////home/dolby/.venv2/PeerDrop/database/data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Api configs
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev118")
    JWT_ACCESS_TOKEN_EXPIRES = 900 # 15 mins
    API_TITLE = "PeerDrop REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Files configs
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads") # saves to uploads folder
    MAX_CONTENT_LENGTH = 24 * 1000 * 1000 # 24mb
