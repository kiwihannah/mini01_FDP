from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'fdp'

client = MongoClient('3.35.0.78', 27017, username="test", password="test")
db = client.fdp


# 로그인 해두면 -> 설문지 페이지로
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        return render_template('form.html')
    else:
        return render_template('index.html')

# login
@app.route('/login', methods=['POST'])
def sign_in():
    # 로그인
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    info = db.users.find_one({'id': id_receive, 'pw': pw_hash})
    print(f'login info {info}')

    if info is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        print(f'user found {info}')
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        print(f'user NOT found {info}')
        return jsonify({'result': 'fail', 'info': info})

@app.route('/register', methods=['POST'])
def sign_up():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    doc = {
        "id": id_receive,   # 아이디
        "pw": pw_hash,      # 비밀번호
    }
    print('user created')
    db.users.insert_one(doc)

    return jsonify({'result': 'success'})

# 저장된 값이 있다면 노출
@app.route('/form')
def go_form():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload["id"]})
    print(f'go_form user_info {user_info}')
    return render_template('form.html', info=user_info)

# form 작성 -> 저장
@app.route('/save_form', methods=['POST'])
def save_form():
    mbti_receive = request.form['mbti_give']
    size_dog_receive = request.form['size_dog_give']
    size_house_receive = request.form['size_house_give']
    time_receive = request.form['time_give']

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload["id"]})['id']
    exists = bool(db.survey.find_one({"email": user_info}))

    print(f'user id {user_info}')
    doc = {
        'email': user_info,
        'mbti': mbti_receive,
        'size_dog': size_dog_receive,
        'size_house': size_house_receive,
        'ins_date': time_receive,
    }
    print(exists)
    print(f' survey result {doc}')

    if exists:
        db.survey.update_one({'email': user_info}, {'$set': {'mbti': mbti_receive}})
        db.survey.update_one({'email': user_info}, {'$set': {'size_dog': size_dog_receive}})
        db.survey.update_one({'email': user_info}, {'$set': {'size_house': size_house_receive}})
    else:
        db.survey.insert_one(doc)
    return jsonify({'msg': '설문지 작성 완료!'})

# 결과 노출
@app.route('/result')
def result():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload["id"]})['id']
    print(f'result user info {user_info}')
    try:
        saved_mbti = db.survey.find_one({'email': user_info})['mbti']
        saved_dog_size = db.survey.find_one({'email': user_info})['size_dog']
        saved_house_size = db.survey.find_one({'email': user_info})['size_house']
        print(f'testing {saved_mbti}, {saved_dog_size}, {saved_house_size}')

        final_result = db.result.find_one({'mbti': saved_mbti, 'dog_size': saved_dog_size})
        print(f'final result {final_result}')
    except:
        final_result = 'no results'
    return render_template("result.html", result=final_result, house_size=saved_house_size)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
