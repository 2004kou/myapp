from flask import flash, session, request
import re
import hashlib
from flask_login import login_user

from models import User,Login

PASSWORDS_PATTERN = r"^.{8,16}$"
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


def validate_signup_form(email, password, password_second, nickname):
    """
    新規登録フォームのバリデーション

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not all([email, password, password_second, nickname]):
        return False, '空のフォームがあるようです'

    if password != password_second:
        return False, '二つのパスワードの値が間違っています'

    if not re.match(EMAIL_PATTERN, email):
        return False, '正しいメールアドレスの形式ではありません'

    if not re.match(PASSWORDS_PATTERN, password):
        return False, 'パスワードは8文字以上16文字以内で入力してください。'

    return True, None
    

def password_Reset_val(email,current_password,new_password,new_password_second):
    if not all([email,current_password,new_password,new_password_second]):
        return False,'空欄を埋めてください'
    if new_password != new_password_second:
        return False,'パスワードが一致しません'
    if not new_password == new_password_second:
        return False,'新しいパスワードと確認用パスワードが違います'
    if len(new_password) < 8 or len(new_password) > 16:
        return False,'パスワードは8～16文字で入力してください'
    if not re.match(EMAIL_PATTERN, email):
        return False, '正しいメールアドレスの形式ではありません'
    user = User.find_by_email(email)
    if user is None:
            return False,'メールアドレスかパスワードが間違えています。'  
    return True, None
           


def login_process_val(email,password):
    if not all([email,password]):
        return False,'空のフォームがあるようです'
    user = User.find_by_email(email)
    if user is None:
        return False,'メールアドレスかパスワードが間違えています。'
    hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if hashPassword != user['password']:
        return False,'メールアドレスかパスワードが間違えています。'
    else:
        user_id = user['user_id']
        login_user(Login(user_id))
        session["user_id"] = user_id
        return True, None
            

def channel_val(channels):
    if channels ==():
        return False,"該当するルームがまだありません"
    else:
        return True
    


def profile_edit_val(favorite,occupation,residence, bio):    
    if not all([favorite,occupation,residence]):
        return False, '空のフォームがあるようです'
    if bio and len(bio) > 200:
        return False, 'ひとことコメントは200字以内で入力してください'
    return True,None




def survey_val():
     data={}
     for i in range(1, 16):
            pid = f"p{i}"
            data[pid] = request.form.get(pid)
            if data[pid] == None:
                flash(f"{i}番目の質問に答えてください")
            else:
                return True

