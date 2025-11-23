from flask import Flask
import os
from flask_login import LoginManager



from config import DevelopmentConfig
from models import Login
from extensions import bcrypt
from routes import auth_bp, chat_bp, room_bp, profile_bp, survey_bp





app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
bcrypt.init_app(app)




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
    app.run(host='0.0.0.0', debug=os.getenv('FLASK_DEBUG', 'False') == 'True')