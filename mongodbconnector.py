import pymongo
import time
import redis
import json
from multiprocessing import Manager

myclient = pymongo.MongoClient("mongodb://127.0.1.1:27017")

### REDIS ###
red = redis.Redis(host="localhost", port=6379, password="")
pubsub = red.pubsub()
pubsub.subscribe("test_channel")

mydb = myclient["meteor"]["captions"]

# manager = Manager()
# u = manager.list()
# meeting = manager.dict()


print(mydb)
myquery = {"$and": [{"meetingId" : "d379fb14d262b7cd51d768079ad59cf08db23287-1609944939692"}, {"length" : 0}, {"locale.locale" : "en"}]}

for i in mydb.find(myquery):
    print(i)

def the_loop():
    meetings = {}
    while True:
            fullmessage = pubsub.get_message()
            if fullmessage and not isinstance(fullmessage["data"], int):
                message = json.loads(fullmessage["data"].decode("UTF-8"))
                # print(message)
                try:
                    if "Event" in message.keys():
                        if message["Event"] == "KALDI_START":
                            print("Kaldi is started. Lets get ASR!")
                            ASR = message["ASR-Channel"]
                            meetingId = message["meetingId"]
                            OrigCallerIDName = message["Caller-Orig-Caller-ID-Name"]
                            meetings = dict_handler(meetings, meetingId, ASR, OrigCallerIDName)
                            print(meetings)
                            pubsub.subscribe(ASR)
                            # Loader_Start_msg = {"Event" : "KALDI_START", "Caller-Destination-Number" : CallerDestinationNumber, "meetingId" : meetingId, "Caller-Orig-Caller-ID-Name" : OrigCallerIDName, 'Caller-Username': CallerUsername, "Input-Channel" : input_channel, "ASR-Channel" : output_channel}
                        
                    if message["handle"] == "partialUtterance":
                        print(fullmessage)
                        print(message)
                        print(message["utterance"])
                        # meetings[]
                        # Loader_Stop_msg = {"Event" : "KALDI_STOP", "Caller-Destination-Number" : CallerDestinationNumber, "meetingId" : meetingId, "Caller-Orig-Caller-ID-Name" : OrigCallerIDName, 'Caller-Username': CallerUsername, "Input-Channel" : input_channel, "ASR-Channel" : output_channel}
                except:
                    pass

def dict_handler(d, meetingId, ASR, participant):
    if ASR not in d.keys():
        d[ASR] = {}
        d[ASR]["meetingId"] = meetingId
        d[ASR]["participants"] = {}
    d[ASR]["participants"][participant] = ""
    return d



if __name__ == "__main__":
    the_loop()

# def handler(message):
#     message = json.loads(message["data"].decode("UTF-8"))
#     print(message["Event"])
#     if message["Event"] == "KALDI_START":
#         ASR = message["ASR-Channel"]
#         InputChannel = message["Input-Channel"]
#         CallerUsername = message["Caller-Username"]
#         pubsub.subscribe(**{ASR : kaldi_text})
#         thread2 = pubsub.run_in_thread(sleep_time=0.001)
#         print(CallerUsername)
#         print(meeting)
#     return message
            
        
# def kaldi_text(message):
#     message = json.loads(message["data"].decode("UTF-8"))
#     if message["handle"] == "partialUtterance":
#         u.append(message["utterance"])
#         # print(u)


# message = pubsub.subscribe(**{"test_channel": handler})
# thread = pubsub.run_in_thread(sleep_time=0.001)

# while True:
#     time.sleep(1)
    # ASR = u.pop(0) if u else None
    # if ASR:
        # print(ASR)



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