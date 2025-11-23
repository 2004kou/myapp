from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from models import User
from flask_login import login_required,current_user

from util.validators import profile_edit_val
from util.DB import ensure_conn

profile_bp = Blueprint(
    'profile', __name__,
    url_prefix='/profile'  
)

#チャットルームからほかの人のプロフィール画面表示
@profile_bp.route('/show_profile/<user_id>/<channel_id>')
@login_required
def show_profile(user_id,channel_id):
    ensure_conn()
    users = User.get_by_profile(user_id)
    channel_id = channel_id
    if users:
        if not users.get("public"):
            flash('こちらのユーザーはプロフィールが非公開です')
            return redirect(url_for('chat.chatroom_screen_view', channel_id = channel_id))
        else:
            return render_template('profile.html',users = users)
    return redirect(url_for('chat.chatroom_screen_view', channel_id = channel_id))

# プロフィール画面の表示

@profile_bp.route('/profile', methods=['GET']) 
@login_required
def profile_view():
    ensure_conn()
    user_id = session.get('user_id')
    users = User.get_by_profile(user_id)
    return render_template('profile/profile.html',users = users)

# プロフィール編集画面の表示
@profile_bp.route('/edit_profile', methods=['GET']) 
@login_required
def edit_profile_view():
    ensure_conn()
    user_id = session.get('user_id')
    profile = User.get_by_profile(user_id)
    return render_template('profile/edit_profile.html',profile = profile)


#プロフィール編集
@profile_bp.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    ensure_conn()
    nickname = request.form.get('nickname')
    icon_image_url = request.form.get('icon')
    favorite = request.form.get('favorite')
    bio = request.form.get('bio')
    occupation = request.form.get('occupation')
    residence = request.form.get('residence')
    public = request.form.get('public')
    if not nickname:
        nickname = current_user.nickname
    is_valid, error_msg = profile_edit_val(favorite,occupation,residence, bio)
    if not is_valid:
        flash(error_msg)
        return redirect(url_for('profile.edit_profile_view'))
    else:
    # プロフィール更新処理
        user_id = session.get('user_id')
        User.update_profile(user_id, nickname, icon_image_url, favorite, bio, occupation, residence, public)
        flash('プロフィールを更新しました')
        return redirect(url_for('profile.profile_view'))
