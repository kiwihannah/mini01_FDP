from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.fdp

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/result')
def result():
    return render_template('result.html')

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
@app.route('/result', methods=['POST'])
def find_words():
    try:
        result = db.survey.find_one({'email':'Hannah@gmail.com'})
        print(result)
    except:
        msg = 'no results'
    return jsonify({'msg': msg, result:result})

#3. re-form
@app.route('/delete', methods=['POST'])
def delete_word():
    word_receive = request.form['delete_word_give']
    db.neologism.delete_one({'word':word_receive})

    return jsonify({'msg': 'deleted'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)