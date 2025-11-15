from flask import flash, session, request
import re
import hashlib
from flask_login import login_user,current_user

from models import User,Login

PASSWORDS_PATTERN = r"^.{8,16}$"
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


def sign_up_val(email,password,password_second,nickname):
    if email == '' or password == '' or password_second == '' or nickname == "":
            flash('空のフォームがあるようです')
    elif password != password_second:
            flash('二つのパスワードの値が間違っています')
    elif re.match(EMAIL_PATTERN, email) is None:
            flash('正しいメールアドレスの形式ではありません')
    elif re.match(PASSWORDS_PATTERN, password) is None:
            flash("パスワードは8文字以上16文字以内で入力してください。")
    else:
        return  True
    

def password_Reset_val(email,new_password,new_password_second):
    if email == '' or new_password == '':
        flash('空欄を埋めてください')
    elif new_password != new_password_second:
        flash('パスワードが一致しません')
    elif len(new_password) < 8 or len(new_password) > 16:
        flash('パスワードは8～16文字で入力してください')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式で入力してください')
    else:
        user = User.find_by_email(email)
        if user is None:
            flash('このメールアドレスは登録されていません')
        else:
             return True
           


def login_process_val(email,password):
    if email == '' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = User.find_by_email(email)
        if user is None:
            flash('メールアドレスかパスワードが間違えています。')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user['password']:
                flash('パスワードが間違っています')
            else:
                user_id = user['user_id']
                login_user(Login(user_id))
                session["user_id"] = user_id
                return True
            

def channel_val(channels):
    if channels ==():
            flash("該当するルームがまだありません")
    else:
        return True
    


def profile_edit_val(nickname,favorite,occupation,residence, bio):
    if not nickname:
        nickname = current_user.nickname
        return False
    if not favorite:
        flash('趣味を入力してください')
        return False
    if not occupation:
        flash('職業を入力してください')
        return False
    if not residence:
        flash('所在地を入力してください')
        return False
    if bio and len(bio) > 200:
        flash('ひとことコメントは200字以内で入力してください')
        return False   
    return True




def survey_val():
     data={}
     for i in range(1, 16):
            pid = f"p{i}"
            data[pid] = request.form.get(pid)
            if data[pid] == None:
                flash(f"{i}番目の質問に答えてください")
            else:
                return True

