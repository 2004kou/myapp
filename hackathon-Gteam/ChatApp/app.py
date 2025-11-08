from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from datetime import timedelta
import hashlib
import uuid
import re
import os
import json
from flask_login import login_user, logout_user, login_required, LoginManager, current_user

from models import User, Login, Genre, Search, Rank, Message, Question






# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
PASSWORDS_PATTERN = r"^.{8,16}$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days = SESSION_DAYS)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_view'
login_manager.login_message = "ログインが必要です。先にログインしてください。"

@login_manager.user_loader
def load_user(user_id):
    return  Login(user_id)

##ログインしている時だけは入れるページにはこれを書いてください--->@login_required





# 新規登録画面の表示
@app.route('/signup', methods=['GET'])
def signup_view():
    return render_template('signup.html')

# 新規登録
@app.route('/signup', methods=['POST'])
def signup_process():
    email = request.form.get('email')
    password = request.form.get('password')
    password_second = request.form.get('password_second')
    nickname = request.form.get('nickname')
    if email == '' or password == '' or password_second == '' or nickname == "":
        flash('空のフォームがあるようです')
    elif password != password_second:
        flash('二つのパスワードの値が間違っています')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    elif re.match(PASSWORDS_PATTERN, password) is None:
        flash("パスワードは8文字以上16文字以内で入力してください。")
    else:
       user_id = uuid.uuid4() 
       password = hashlib.sha256(password.encode('utf-8')).hexdigest()
       registered_user = User.find_by_email(email)
       if registered_user != None:
           flash('既に登録されているようです')
       else:
            User.create(user_id, email, password, nickname)
            UserId = str(user_id)
            session['user_id'] = UserId
            return redirect(url_for('login_view'))
    return redirect(url_for('signup_view'))




# ログインページの表示
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = User.find_by_email(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user['password']:
                flash('パスワードが間違っています')
            else:
                user_id = user['user_id']
                login_user(Login(user_id))
                session["user_id"] = user_id                
                return redirect(url_for('index_view'))
    return redirect(url_for('login_view'))


# ログアウト
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('ログアウトしました。')
    return redirect(url_for('login_view'))


#パスワード再設定画面
@app.route('/password_reset', methods=['GET'])
def password_reset_view():
    return render_template('password_reset.html')

#パスワード再設定
@app.route('/password_reset', methods=['POST'])
def password_reset_process():
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    new_password_second = request.form.get('new_password_second')

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
            new_hashPassword = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
            User.update_password(user['user_id'], new_hashPassword)
            flash('パスワードをリセットしました。ログインしてください')
            return redirect(url_for('login_view'))

    return redirect(url_for('password_reset_view'))


# チャットルーム一覧の表示
@app.route('/index', methods=['GET'])
@login_required
def index_view():
    channels = Genre.get_all()
    return render_template('index.html', channels=channels)

# チャット画面の表示
@app.route('/chatroom_screen/<channel_id>', methods=['GET'])
@login_required
def chatroom_screen_view(channel_id):
    messages = Message.get_all(channel_id)
    channel_name_tapule = Message.get_channel_name(channel_id)
    channel_name = channel_name_tapule["channel_name"]
    user = session["user_id"]

    return render_template('chatroom_screen.html', user_id=current_user.user_id, messages=messages, channel_id=channel_id,channel_name = channel_name, user = user)

#チャットルームからほかの人のプロフィール画面表示
@app.route('/show_profile/<user_id>/<channel_id>')
@login_required
def show_profile(user_id,channel_id):
    users = User.get_by_profile(user_id)
    channel_id = channel_id
    if users:
        if users.get("public") == 0:
            print(channel_id)
            flash('こちらのユーザーはプロフィールが非公開です')
            return redirect(url_for('chatroom_screen_view', channel_id = channel_id))
        else:
            return render_template('profile.html',users = users)
    return redirect(url_for('chatroom_screen_view', channel_id = channel_id))

# チャット送信
@app.route('/chatroom_screen/<channel_id>', methods=['POST'])
@login_required
def send_message(channel_id):
    message_content = request.form.get('message')
    if message_content:
        message_id = str(uuid.uuid4())
        Message.create(message_id, message_content, channel_id, current_user.user_id)
    return redirect(url_for('chatroom_screen_view', channel_id = channel_id))

# チャット削除
@app.route('/chatroom_screen/<channel_id>/<message_id>/delete', methods=['POST'])
@login_required
def delete_message(channel_id, message_id):
    if message_id:
        Message.delete(message_id, current_user.user_id)
    return redirect(url_for('chatroom_screen_view', channel_id = channel_id))

# チャット編集
@app.route('/chatroom_screen/<channel_id>/<message_id>/edit', methods=['POST'])
@login_required
def update_message(channel_id, message_id):
    new_content = request.form.get('message')
    if message_id and new_content:
        Message.update_message_content(message_id, new_content)
    return redirect(url_for('chatroom_screen_view', channel_id = channel_id))




#room作成画面
@app.route('/room_create', methods=['GET'])
@login_required
def room_create_view():

    return render_template('room_create.html')


# room作成
@app.route('/room_create', methods=['POST'])
@login_required
def room_create_process():
    channel_name = request.form.get('channel_name')
    hobby_genre_name = request.form.get('hobby_genre_name')
    channel_comment = request.form.get('comment')
    if channel_name == '' or hobby_genre_name == '' :
        flash('空のフォームがあるようです')

    else:
       registered_channel_name = Genre.find_by_channel_name(hobby_genre_name)
       if registered_channel_name != None:
           flash('既に登録されているようです')
       else:
           if channel_comment == "":
            channel_id = uuid.uuid4() 
            user_id = session["user_id"]
            genre_id_dic = Genre.find_by_genre_id(hobby_genre_name)
            hobby_genre_id = genre_id_dic["hobby_genre_id"]
            Genre.create(channel_id, channel_name, user_id , hobby_genre_id)
            return redirect(url_for('room_create_view'))
           else:
            channel_id = uuid.uuid4() 
            user_id = session["user_id"]
            genre_id_dic = Genre.find_by_genre_id(hobby_genre_name)
            hobby_genre_id = genre_id_dic["hobby_genre_id"]
            Genre.create_comment(channel_id, channel_name, channel_comment, user_id , hobby_genre_id)
    return redirect(url_for('index_view'))

# チャット部屋の削除
@app.route('/chatroom_screen/<channel_id>/delete_room', methods=['POST'])
@login_required
def delete_room(channel_id):
    user_id = session["user_id"]
    user_id_req =Genre.find_by_userid(channel_id)
    user_id_reqq_key = user_id_req["user_id"]
    if user_id_reqq_key != user_id:
        flash('このチャットルームの作成者ではないため削除出来ません')
        return redirect(url_for('index_view'))
    else:
        # チャンネル削除処理（関連するメッセージ含めて）
        Genre.delete(channel_id)
        flash('チャットルームを削除しました')
        return redirect(url_for('index_view'))


# ジャンル検索画面の表示、ランキング表示画面ランキング表示画面表示
@app.route('/room_search')
@login_required
def room_search_view():
    return render_template('room_search.html')

#ジャンル検索画面,ランキング表示画面
@app.route('/room_search', methods=['POST'])
@login_required
def room_search_process():
    search_genre_name= request.form.get('search_genre_name')
    genre = {
    "all": "すべて",
    "travel": "旅行",
    "eat": "飲食",
    "art": "芸術",
    "study": "学習",
    "movie": "映画",
    "comic": "漫画・アニメ・ゲーム",
    "music": "音楽",
    "idol": "アイドル",
    "muscle": "筋トレ",
    "sports": "スポーツ",
    "sauna": "サウナ",
    "relax": "リラックス",
    "fashion": "ファッション",
    "cosme": "コスメ",
    "pet": "ペット",
    "another": "その他"
}
    genre = genre[search_genre_name]
    if  search_genre_name == None:
        flash('ジャンルを選択してください')
        return render_template('room_search.html')
    elif search_genre_name == "all":
        channels = Search.find_all()
        if channels == ():
            flash("該当するルームがまだありません")
            return render_template('room_search.html')
        else:
             channel_id = Rank.ranking_all()
             print(channel_id)
             genre_rank = Rank.channel_name_find(channel_id)
             return render_template('room_search_result.html', 
                                    channels = channels, 
                                    genre =genre , 
                                    content_type='text/html; charset=utf-8', 
                                    genre_rank = genre_rank)

    else:
            channels = Search.find_by_search(search_genre_name)
            if channels == ():
                flash("該当するルームがまだありません")
                return render_template('room_search.html')
            else: 
                rank_genre_id_dic = Rank.rank_serch_id(search_genre_name)
                channel_id = Rank.ranking(rank_genre_id_dic)
                genre_rank = Rank.channel_name_find(channel_id)
                return render_template('room_search_result.html', 
                                        channels = channels, 
                                        genre =genre , 
                                        content_type='text/html; charset=utf-8', 
                                       genre_rank = genre_rank)

# ジャンル検索結果画面の表示
@app.route('/room_search_result', methods=['GET'])
@login_required
def room_search_result():
    genre = request.args.get('genre')
    return render_template('room_search_result.html', genre=genre)

# プロフィール画面の表示

@app.route('/profile', methods=['GET']) 
@login_required
def profile_view():
    user_id = session.get('user_id')
    users = User.get_by_profile(user_id)
    return render_template('profile.html',users = users)

# プロフィール編集画面の表示
@app.route('/edit_profile', methods=['GET']) 
@login_required
def edit_profile_view():
    user_id = session.get('user_id')
    profile = User.get_by_profile(user_id)
    return render_template('edit_profile.html',profile = profile)


@app.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    nickname = request.form.get('nickname')
    icon_image_url = request.form.get('icon')
    favorite = request.form.get('favorite')
    bio = request.form.get('bio')
    occupation = request.form.get('occupation')
    residence = request.form.get('residence')
    public = request.form.get("public")

    if not nickname:
            nickname = current_user.nickname # 入力欄が空なら今のニックネームを使う

    if not favorite:
            flash('趣味を入力してください')
            return redirect(url_for('edit_profile_view'))
    if not occupation:
            flash('職業を入力してください')
            return redirect(url_for('edit_profile_view'))
    if not residence:
            flash('所在地を入力してください')
            return redirect(url_for('edit_profile_view'))
    
        
    if len(bio) > 200:
            flash('ひとことコメントは200字以内で入力してください')
            return redirect(url_for('edit_profile_view'))
    user_id = session.get('user_id')    
    User.update_profile(user_id, nickname, icon_image_url, favorite, bio, occupation, residence, public)
    login_user(current_user) 
    flash('プロフィールを更新しました')
    return redirect(url_for('profile_view'))

#アイコン表示

# アカウント削除
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account_process():
    user_id = current_user.user_id
    User.delete(user_id)
    logout_user()
    session.pop('user_id', None)
    flash('アカウントを削除しました。ご利用ありがとうございました。')
    return redirect(url_for('signup_view'))

#趣味は何
@app.route('/questionnaire', methods=['POST'])
@login_required
def questions_hobby_name():
    hobby_name = request.form.get('hobby_name')
    hobby_name_none = Question.find_by_hobby(hobby_name)
    hobby_name_id = uuid.uuid4() 
    if hobby_name == None or hobby_name=="":
        flash("趣味を記入してください。")
        return redirect(url_for('questionnaire_view'))
    if hobby_name_none != None:
        question_data_taple = Question.get_data(hobby_name) 
        class_size= question_data_taple["class_size"] 
        data = json.loads(question_data_taple['total_json_data'])
        values = [float(data[f'q{i}']) for i in range(1, 16)]
        data_prev = {}
        result = {}
        for i in range(1, 16):
            qid = f"q{i}"
            if request.form.get(qid) == None:
                flash(f"{i}番目の質問に答えてください")
                return redirect(url_for('questionnaire_view'))
            data_prev[qid] =float( request.form.get(qid))
        for num in range(1, 16):
            qid = f"q{num}"
            result[qid] = str((data_prev[f'q{num}'] + values[num-1]))
        class_size = class_size+1
        Question.hobby_data_update(result,class_size,hobby_name)    
        flash('ご協力ありがとうございました')
        return redirect(url_for('questionnaire_view'))
    else:
        data = {}
        for i in range(1, 16):
            qid = f"q{i}"
            data[qid] = request.form.get(qid)
            if data[qid] == None:
                flash(f"{i}番目の質問に答えてください")
                return redirect(url_for('questionnaire_view'))
        class_size = 1
        Question.register_none(hobby_name_id,hobby_name,data,class_size)
        flash('ご協力ありがとうございました')        
        return redirect(url_for('questionnaire_view'))

#趣味検索機能

questions =[
        {"question_id": 1, "text": "休日は外で過ごしたい"},
        {"question_id": 2, "text": "一人の時間が好き"},
        {"question_id": 3, "text": "新しいことを始めるのが好き"},
        {"question_id": 4, "text": "物を作るのが好き"},
        {"question_id": 5, "text": "集中して何かに没頭する方"},
        {"question_id": 6, "text": "アート、デザインに興味がある"},
        {"question_id": 7, "text": "自然の中で過ごすのが好き"},
        {"question_id": 8, "text": "体を動かすことが好き"},
        {"question_id": 9, "text": "SNSなどで発信することが好き"},
        {"question_id": 10, "text": "旅行先では計画的に動きたい"},
        {"question_id": 11, "text": "機械やデジタルが好き"},
        {"question_id": 12, "text": "グループ活動が好き"},
        {"question_id": 13, "text": "初対面の人には積極的に話しかける方"},
        {"question_id": 14, "text": "音楽をよく聞いたり演奏したりする"},
        {"question_id": 15, "text": "体を動かすより頭を使うことの方が好き"}
    ]

@app.route('/questionnaire', methods=['GET'])
@login_required
def questionnaire_view():
    return render_template('questionnaire.html', questions = questions)


@app.route('/survey', methods=['GET'])
@login_required
def survey_view():
    return render_template('survey.html', questions = questions)


@app.route('/survey_result', methods=['GET'])
@login_required
def survey_result_view():
    lists = session.get("hobby_name_list")
    return render_template('survey_result.html',lists = lists)


@app.route('/survey', methods=['POST'])
@login_required
def survey_result():
    survey_data ={}
    min_data = []
    rec_hobby_name =[]
    for i in range(1, 16):
            pid = f"p{i}"
            survey_data[pid] = request.form.get(pid)
            if survey_data[pid] == None:
                flash(f"{i}番目の質問に答えてください")
                return redirect(url_for('survey_view'))
    
    total_data = Question.survey_get_data()
    for j in total_data:
        # print(j)
        result_data = 0
        for i in range(1, 16):
            total_data = json.loads(j["total_json_data"])
            average = float(total_data[f"q{i}"]) / int(j["class_size"])
            user_value = float(survey_data[f"p{i}"])
            result_data += abs(round(average - user_value, 2))
        print(result_data,":::",j["hobby_name"])
        if len(rec_hobby_name)<3:
                rec_hobby_name.append(j["hobby_name"])
                min_data.append(result_data)
        elif max(min_data)>result_data:
                print(max(min_data),"!!!!")
                n  =min_data.index(max(min_data))
                min_data[n] = result_data
                rec_hobby_name[n] = j["hobby_name"]
    session["hobby_name_list"] = rec_hobby_name   
    return redirect(url_for('survey_result_view'))

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(host='0.0.0.0', debug=True)