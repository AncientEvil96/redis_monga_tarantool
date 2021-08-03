from flask import Flask, request, make_response
import redis
from time import strftime
import hashlib
import uuid

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/count_requests')
def theanswer():
    day = strftime("%Y-%m-%d")
    # не уверен что этот парамерт уникален для пользователя но думаю пойдет
    # user_id = request.cookies.get('abcxyz')
    user_hash_id = request.cookies.get('user_hash_id')

    if user_hash_id is None:
        hash_object = hashlib.md5(str(uuid.uuid1()).encode('utf-8'))
        user_hash_id = hash_object.hexdigest()

    # TODO: На моей машине это работает не вдавался в подробности почему это тут не работает
    # user_id = request.cookies['username-localhost-8888'].split('|')[-1:][0]
    key = f'page:index:counter:{day}:{user_hash_id}'
    r.incr(key)

    resp = make_response(f'42  / {key} / - ' + str(int(r.get(key))))
    resp.set_cookie('user_hash_id', user_hash_id, max_age=None)

    return resp