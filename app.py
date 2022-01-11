from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import hashlib
import jwt
import requests

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.fdp

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
def go_form():
    mbti_list = list(db.result.find({}, {'_id': False}))
    for mbti in mbti_list:
        a_list = mbti['mbti']
    return render_template('form.html', mbti_list=a_list)

# login -> find_one으로 찾고 있으며 true 든 반환
@app.route('/login', methods=['GET'])
def fining():
    users = list(db.users.find({}, {'_id': False}))
    return jsonify({'all_users': users})

# login -> 기존 아이디가 없는지 있는지 확인하는 기능 추가 예정
@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    db.users.insert_one({'id': id_receive, 'password': password_hash})
    return jsonify({'msg': '로그인완료!!'})

# form 작성
@app.route('/save_form', methods=['POST'])
def save_form():
    mbti_receive = request.form['mbti_give']
    size_dog_receive = request.form['size_dog_give']
    size_house_receive = request.form['size_house_give']
    time_receive = request.form['time_give']

    doc = {
        'email': 'Hannah@gmail.com',
        'mbti': mbti_receive,
        'size_dog': size_dog_receive,
        'size_house': size_house_receive,
        'ins_date': time_receive,
    }

    print(doc)
    db.survey.insert_one(doc)

    return jsonify({'msg': 'Your survey has been saved'})

#2. result
# ?? 그냥 except 쓰지 말라고 충고하는데 어떤식으로 바꿔야 할까?
# 이미지 url 크롤링 다른 팀원이 하는중 --> 결과 값과 비교하여 이미지와 db 결과값 한꺼번에 노출
@app.route('/result')
def result():
    try:
        survey_result = db.survey.find_one({'email':'Hannah@gmail.com'})['mbti'].upper()
        final_result = db.result.find_one({'mbti':survey_result})
        print(f'Finding {survey_result}')
    except:
        final_result = 'no results'
    return render_template("result.html", result=final_result)

#3. re-form
# 로그인 유지 -> survey 테이블만 변동
@app.route('/delete', methods=['POST'])
def update_form():
    db.neologism.update_one({'email':'Hannah@gmail.com'})

    return jsonify({'msg': 'deleted'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)