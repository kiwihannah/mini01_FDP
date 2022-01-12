# 기본 db 크롤링
import requests
from bs4 import BeautifulSoup

from flask import Flask

from pymongo import MongoClient
client = MongoClient('3.35.0.78', 27017, username='test', password='test')
db = client.fdp

app = Flask(__name__)

# 요청을 막아둔 사이트들이 많음. 브라우저에서 엔터친것처럼 효과를 내줌
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://m.blog.naver.com/qkrgksrl0033/222619371591',headers=headers)

# beautiful soup 형태로 만들기

soup = BeautifulSoup(data.text, 'html.parser')

divs = soup.select('#SEDOC-1641923292356-1254584192 > div:nth-child(6) > div')

for div in divs:
    img = div.find('img')
    title = div.select_one('div > div > div > div > div > span').text
    img_src = img['data-lazy-src']
    print(title,img_src)

    doc = {
        'mbti':title,
        'mbti_img':img_src
    }
    db.mbti.insert_one(doc)