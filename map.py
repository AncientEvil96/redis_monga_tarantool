# coding: utf-8
from flask import Flask, render_template, request
from bson import json_util

app = Flask(__name__)
from pymongo import MongoClient

##
## Подключение базе данных и доступ к таблице с индексом
##
client = MongoClient()
# Используем базу данных с именем themap
db = client.themap
places = db.places
places.create_index([('geometry', '2dsphere')])


##
## Отдаём фронтенд
##
@app.route('/')
def root():
    return render_template('index.html')


##
## Создаём новый комментарий к базе данных
##
@app.route('/newplace', methods=['POST'])
def newplace():
    content = request.get_json(silent=True, force=True)
    place_id = places.insert_one(content).inserted_id
    return json_util.dumps(content)


##
## Возвращаем комментарии, которые географически близки
## к запрашиваемой точке
##
@app.route('/places')
def getplaces():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    dist = request.args.get('distance')
    rating = 5
    if dist is None:
        dist = 4000
    # cursor = places.find({
    #     "geometry": {
    #         "$nearSphere": {
    #             "$geometry": {
    #                 "type": "Point",
    #                 "coordinates": [float(lng), float(lat)],
    #                 "properties.rating": rating
    #             },
    #             "$minDistance": 0,
    #             "$maxDistance": dist, }}})

    #TODO: если делать отбор только по рейтингу
    cursor = places.find({'$and': [
        {'geometry': {'$nearSphere': {'$geometry': {'type': 'Point', 'coordinates': [float(lng), float(lat)]},
                                      '$minDistance': 0, '$maxDistance': 4000}}},
        {'properties.rating': rating}]}
    )
    resultset = []
    for place in cursor:
        resultset.append(place)
    return json_util.dumps(resultset)