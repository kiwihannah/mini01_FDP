# 카카오톡 api test 용
import requests

url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = '어플리케이션 REST API 키'
redirect_uri = '어플리케이션 Redirect URI'
authorize_code = '발급받은 토큰'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# json 저장
import json

with open("kakao_code.json","w") as fp:
    json.dump(tokens, fp)