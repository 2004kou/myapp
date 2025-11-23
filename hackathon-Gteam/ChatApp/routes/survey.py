from flask import Blueprint, request, redirect, url_for, flash, session, render_template
from flask_login import login_required
import json
import uuid
from models import Question


from util.validators import survey_val


survey_bp = Blueprint(
    'survey', __name__,
    url_prefix='/survey'  
)


#趣味がある人のアンケートをデータ化
@survey_bp.route('/questionnaire', methods=['POST'])
@login_required
def questions_hobby_name():
    hobby_name = request.form.get('hobby_name')
    hobby_name_none = Question.find_by_hobby(hobby_name)
    hobby_name_id = uuid.uuid4() 
    if hobby_name == None or hobby_name=="":
        flash("趣味を記入してください。")
        return redirect(url_for('survey.questionnaire_view'))
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
                return redirect(url_for('survey.questionnaire_view'))
            data_prev[qid] =float( request.form.get(qid))
        for num in range(1, 16):
            qid = f"q{num}"
            result[qid] = str((data_prev[f'q{num}'] + values[num-1]))
        class_size = class_size+1
        Question.hobby_data_update(result,class_size,hobby_name)    
        flash('ご協力ありがとうございました')
        return redirect(url_for('survey.questionnaire_view'))
    else:
        data = {}
        for i in range(1, 16):
            qid = f"q{i}"
            data[qid] = request.form.get(qid)
            if data[qid] == None:
                flash(f"{i}番目の質問に答えてください")
                return redirect(url_for('survey.questionnaire_view'))
        class_size = 1
        Question.register_none(hobby_name_id,hobby_name,data,class_size)
        flash('ご協力ありがとうございました')        
        return redirect(url_for('survey.questionnaire_view'))

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

@survey_bp.route('/questionnaire', methods=['GET'])
@login_required
def questionnaire_view():
    return render_template('survey/questionnaire.html', questions = questions)


@survey_bp.route('/survey', methods=['GET'])
@login_required
def survey_view():
    return render_template('survey/survey.html', questions = questions)


@survey_bp.route('/survey_result', methods=['GET'])
@login_required
def survey_result_view():
    lists = session.get("hobby_name_list")
    return render_template('survey/survey_result.html',lists = lists)


@survey_bp.route('/survey', methods=['POST'])
@login_required
def survey_result():
    survey_data ={}
    min_data = []
    rec_hobby_name =[]
    if survey_val():   
        total_data = Question.survey_get_data()
        for j in total_data:
            result_data = 0
            for i in range(1, 16):
                total_data = json.loads(j["total_json_data"])
                average = float(total_data[f"q{i}"]) / int(j["class_size"])
                user_value = float(survey_data[f"p{i}"])
                result_data += abs(round(average - user_value, 2))
            if len(rec_hobby_name)<3:
                    rec_hobby_name.append(j["hobby_name"])
                    min_data.append(result_data)
            elif max(min_data)>result_data:
                    n  =min_data.index(max(min_data))
                    min_data[n] = result_data
                    rec_hobby_name[n] = j["hobby_name"]
        session["hobby_name_list"] = rec_hobby_name   
        return redirect(url_for('survey.survey_result_view'))
    else:
        return redirect(url_for('survey.survey_view'))
