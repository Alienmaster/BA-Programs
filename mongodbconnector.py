import pymongo
import time
import redis
import json

myclient = pymongo.MongoClient("mongodb://127.0.1.1:27017")

red = redis.Redis(host="localhost", port=6379, password="")

mydb = myclient["meteor"]["captions"]


print(mydb)
myquery = {"$and": [{"meetingId" : "d379fb14d262b7cd51d768079ad59cf08db23287-1609942180842"}, {"length" : 0}, {"locale.locale" : "en"}]}

for i in mydb.find(myquery):
    print(i)

def handler(message):
    message = json.loads(message["data"].decode("UTF-8"))
    print(message["Event"])
    if message["Event"] == "KALDI_START":
        ASR = message["ASR-Channel"]
        pubsub.subscribe(**{ASR : kaldi_text})
        thread2 = pubsub.run_in_thread(sleep_time=0.001)

def kaldi_text(message):
    message = json.loads(message["data"].decode("UTF-8"))
    print(message)
    if message["handle"] == "completeUtterance":
        print(message["utterance"])



pubsub = red.pubsub()
pubsub.subscribe(**{"test_channel": handler})
thread = pubsub.run_in_thread(sleep_time=0.001)


# old_value = mydb.find_one({"_id": "mx9P7sZRPSgAjjzBS"})
# print(old_value)
# mydb.update({
#     '_id': old_value['_id']
# },{
#     '$set': {
#         'data': '<h1 style="color:blue;">This is a heading</h1>',
#         'revs': 11,
#         'length': 170
#     }
# }, upsert=False)
# time.sleep(0.1)
# mydb.update({
#     '_id': old_value['_id']
# },{
#     '$set': {
#         'data': '<h1 style="font-size:300%;">This is a heading</h1>',
#         'revs': 12,
#         'length': 180
#     }
# }, upsert=False)

# while True:
#     time.sleep(1)
#     for a in range(0,20):
#         mydb.update({
#             '_id': old_value['_id']
#         },{
#             '$set': {
#             'data': a,
#             'revs': a + 10,
#             'length': a + 10
#             }
#         }, upsert=False)

# print(myclient.list_database_names())

# mydict = {'$set': {'meetingId': 'd379fb14d262b7cd51d768079ad59cf08db23287-1609767751372', 'padId': '42f421d2_captions_en', 'locale': {'locale': 'en', 'name': 'English'}, 'ownerId': '', 'readOnlyPadId': '', 'data': 'lel', 'revs': 1, 'length': 3}}
# myquery = {'_id': 'E9pNtAk9mgPcY3nLp'}
# x = mydb.update_one(myquery, mydict)
# for i in mydb.find({},{'locale' : {'locale' : 'en'}}):
#     print(i)
# print(x.inserted_id)