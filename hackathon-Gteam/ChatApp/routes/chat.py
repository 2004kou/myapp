from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from flask_login import login_required, current_user
from models import Message
import uuid
from util.DB import ensure_conn

chat_bp = Blueprint(
    'chat', __name__,
    url_prefix='/chat'  
)





# チャット画面の表示
@chat_bp.route('/chatroom_screen/<channel_id>', methods=['GET'])
@login_required
def chatroom_screen_view(channel_id):
    ensure_conn()
    messages = Message.get_all(channel_id)
    channel_name_tuple = Message.get_channel_name(channel_id)
    channel_name = channel_name_tuple["channel_name"]
    user = session["user_id"]

    return render_template('chat/chatroom_screen.html', user_id=current_user.user_id, messages=messages, channel_id=channel_id,channel_name = channel_name, user = user)

# チャット送信
@chat_bp.route('/chatroom_screen/<channel_id>', methods=['POST'])
@login_required
def send_message(channel_id):
    ensure_conn()
    message_content = request.form.get('message')
    if message_content:
        message_id = str(uuid.uuid4())
        Message.create(message_id, message_content, channel_id, current_user.user_id)
    return redirect(url_for('chat.chatroom_screen_view', channel_id = channel_id))

# チャット削除
@chat_bp.route('/chatroom_screen/<channel_id>/<message_id>/delete', methods=['POST'])
@login_required
def delete_message(channel_id, message_id):
    ensure_conn()
    if message_id:
        Message.delete(message_id, current_user.user_id)
    return redirect(url_for('chat.chatroom_screen_view', channel_id = channel_id))

# チャット編集
@chat_bp.route('/chatroom_screen/<channel_id>/<message_id>/edit', methods=['POST'])
@login_required
def update_message(channel_id, message_id):
    ensure_conn()
    new_content = request.form.get('message')   
    if message_id and new_content:
        message_owner = Message.get_by_user_id(message_id)
        if message_owner != current_user.user_id:
            flash('他人のメッセージは編集できません')
            return redirect(url_for('chatroom_screen_view', channel_id=channel_id))
        else:
            Message.update_message_content(message_id, new_content)
    return redirect(url_for('chat.chatroom_screen_view', channel_id = channel_id))

