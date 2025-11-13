from flask import Flask
from datetime import timedelta
import uuid
import os
from flask_login import LoginManager

from models import Login


from routes import auth_bp, chat_bp, room_bp, profile_bp, survey_bp




# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days = SESSION_DAYS)


#ブルーポイント
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(room_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(survey_bp)



#ログイン認証
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_view'
login_manager.login_message = "ログインが必要です。先にログインしてください。"

@login_manager.user_loader
def load_user(user_id):
    return  Login(user_id)




if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', debug=True)