from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from models import User
from flask_login import logout_user, login_required,current_user
import uuid


from extensions import bcrypt
from util.validators import validate_signup_form,password_Reset_val,login_process_val

auth_bp = Blueprint(
    'auth', __name__,
    url_prefix='/auth'  
)








# ログインページの表示
@auth_bp.route('/login', methods=['GET'])
def login_view():
    return render_template('auth/login.html')

# 新規登録
@auth_bp.route('/signup', methods=['POST'])
def signup_process():
    email = request.form.get('email')
    password = request.form.get('password')
    password_second = request.form.get('password_second')
    nickname = request.form.get('nickname')
    is_valid, error_msg = validate_signup_form(email, password, password_second, nickname)
    if not is_valid:
        flash(error_msg)
        return redirect(url_for('auth.signup_view'))
    else:
        user_id = uuid.uuid4()
        password =bcrypt.generate_password_hash(password).decode('utf-8')
        registered_user = User.find_by_email(email)
        if registered_user != None:
            flash('既に登録されているようです')
        else:
                User.create(user_id, email, password, nickname)
                UserId = str(user_id)
                session['user_id'] = UserId
                return redirect(url_for('auth.login_view'))
        return redirect(url_for('auth.signup_view'))    

# ログイン処理
@auth_bp.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')
    is_valid, error_msg = login_process_val(email, password)
    if not is_valid:
        flash(error_msg)
        return redirect(url_for('auth.login_view'))
    else:
        return redirect(url_for('room.index_view'))
   


# ログアウト
@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('ログアウトしました。')
    return redirect(url_for('auth.login_view'))

# 新規登録画面の表示
@auth_bp.route('/signup', methods=['GET'])
def signup_view():
    return render_template('auth/signup.html')

#パスワード再設定画面
@auth_bp.route('/password_reset', methods=['GET'])
def password_reset_view():
    return render_template('auth/password_reset.html')

#パスワード再設定
@auth_bp.route('/password_reset', methods=['POST'])
def password_reset_process():
    email = request.form.get('email')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    new_password_second = request.form.get('new_password_second')
    is_valid, error_msg = password_Reset_val(email,current_password,new_password,new_password_second)
    if not is_valid:
        flash(error_msg)
        return redirect(url_for('auth.password_reset_view'))
    is_valid, error_msg = password_Reset_val(email,current_password,new_password,new_password_second)
    if not is_valid:
        flash(error_msg)
        return redirect(url_for('auth.password_reset_view'))
    is_valid, error_msg = login_process_val(email,current_password )
    if not is_valid:
        flash(error_msg)
        return redirect(url_for('auth.password_reset_view'))
    user = User.find_by_email(email)
    new_hashPassword = bcrypt.generate_password_hash(new_password).decode('utf-8')
    User.update_password(user['user_id'], new_hashPassword)
    flash('パスワードを変更しました。ログインしてください')
    return redirect(url_for('auth.login_view'))





# アカウント削除
@auth_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account_process():
    user_id = current_user.user_id
    User.delete(user_id)
    logout_user()
    session.pop('user_id', None)
    flash('アカウントを削除しました。ご利用ありがとうございました。')
    return redirect(url_for('auth.signup_view'))