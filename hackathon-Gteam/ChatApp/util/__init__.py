# from flask import Flask
# from .extensions import bcrypt
# from .routes.auth import auth_bp
# from .routes.profile import profile_bp
# from .routes.chat import chat_bp
# from .routes.survey import survey_bp

# def create_app():
#     app = Flask(__name__)
#     app.config["SECRET_KEY"] = "secret"

#     # ここで初期化
#     bcrypt.init_app(app)

#     # Blueprint 登録
#     app.register_blueprint(auth_bp, url_prefix="/auth")
#     app.register_blueprint(profile_bp, url_prefix="/profile")
#     app.register_blueprint(chat_bp, url_prefix="/chat")
#     app.register_blueprint(survey_bp, url_prefix="/survey")

#     return app