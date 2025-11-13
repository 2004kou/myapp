from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from flask_login import login_required
import uuid

from models import Genre, Search, Rank

from util.validators import channel_val

room_bp = Blueprint(
    'room', __name__,
    url_prefix='/room'  
)

#room作成画面
@room_bp.route('/room_create', methods=['GET'])
@login_required
def room_create_view():

    return render_template('room/room_create.html')

# room作成
@room_bp.route('/room_create', methods=['POST'])
@login_required
def room_create_process():
    channel_name = request.form.get('channel_name')
    hobby_genre_name = request.form.get('hobby_genre_name')
    channel_comment = request.form.get('comment')
    if channel_name == '' or hobby_genre_name == '' :
        flash('空のフォームがあるようです')

    else:
       registered_channel_name = Genre.find_by_channel_name(channel_name)
       if registered_channel_name != None:
           flash('そのチャンネル名は登録されているようです')
           return redirect(url_for('room.room_create_view'))
       else:
           if channel_comment == "":
            channel_id = uuid.uuid4() 
            user_id = session["user_id"]
            genre_id_dic = Genre.find_by_genre_id(hobby_genre_name)
            hobby_genre_id = genre_id_dic["hobby_genre_id"]
            Genre.create(channel_id, channel_name, user_id , hobby_genre_id)
            flash('作成できました。')
            return redirect(url_for('room.index_create_view'))
           else:
            channel_id = uuid.uuid4() 
            user_id = session["user_id"]
            genre_id_dic = Genre.find_by_genre_id(hobby_genre_name)
            hobby_genre_id = genre_id_dic["hobby_genre_id"]
            Genre.create_comment(channel_id, channel_name, channel_comment, user_id , hobby_genre_id)
            flash('作成できました。')
    return redirect(url_for('room.index_view'))


# チャットルーム一覧の表示
@room_bp.route('/index', methods=['GET'])
@login_required
def index_view():
    channels = Genre.get_all()
    return render_template('room/index.html', channels=channels)

# チャット部屋の削除
@room_bp.route('/chatroom_screen/<channel_id>/delete_room', methods=['POST'])
@login_required
def delete_room(channel_id):
    user_id = session["user_id"]
    user_id_req =Genre.find_by_userid(channel_id)
    user_id_reqq_key = user_id_req["user_id"]
    if user_id_reqq_key != user_id:
        flash('このチャットルームの作成者ではないため削除出来ません')
        return redirect(url_for('room.index_view'))
    else:
        # チャンネル削除処理（関連するメッセージ含めて）
        Genre.delete(channel_id)
        flash('チャットルームを削除しました')
        return redirect(url_for('room.index_view'))
    

# ジャンル検索画面の表示、ランキング表示画面ランキング表示画面表示
@room_bp.route('/room_search')
@login_required
def room_search_view():
    return render_template('room/room_search.html')


#ジャンル検索画面,ランキング表示画面
@room_bp.route('/room_search', methods=['POST'])
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
        return render_template('room/room_search.html')
    elif search_genre_name == "all":
        channels = Search.find_all()
        if channel_val(channels):
            channel_id = Rank.ranking_all()
            genre_rank = Rank.channel_name_find(channel_id)
            return render_template('room/room_search_result.html', 
                                    channels = channels, 
                                    genre =genre , 
                                    content_type='text/html; charset=utf-8', 
                                    genre_rank = genre_rank)
        else:
            return render_template('room/room_search.html')
             
    else:
            channels = Search.find_by_search(search_genre_name)
            if channel_val(channels):
                rank_genre_id_dic = Rank.rank_serch_id(search_genre_name)
                channel_id = Rank.ranking(rank_genre_id_dic)
                genre_rank = Rank.channel_name_find(channel_id)
                return render_template('room/room_search_result.html', 
                                        channels = channels, 
                                        genre =genre , 
                                        content_type='text/html; charset=utf-8', 
                                       genre_rank = genre_rank)               
            else: 
                 return render_template('room/room_search.html')
               


# ジャンル検索結果画面の表示
@room_bp.route('/room_search_result', methods=['GET'])
@login_required
def room_search_result():
    genre = request.args.get('genre')
    return render_template('room/room_search_result.html', genre=genre)