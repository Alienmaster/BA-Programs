import time
import os
import redis
import json


#Set the filename and open the file
filename = '/var/freeswitch/meetings/2020-12-22-19-52-01_ECHO_TO_CONFERENCE_write.wav'
file = open(filename,'rb', buffering=2048)

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

red = redis.Redis(host="localhost")

pubsub = red.pubsub()

pubsub.subscribe("audio_read")

meeting = 0
while True:
    text = pubsub.get_message()
    # if text:
    #     if text["data"] not in {1, 2}:
    #         text = json.loads(text["data"].decode("UTF-8"))
    #         print(text["core"]["header"]["name"])
    #         if text["core"]["header"]["name"] == "MeetingCreatedEvtMsg":
    #             meeting = text["core"]["body"]["props"]["voiceProp"]["voiceConf"]
    #             print(meeting)
    #         if text["core"]["header"]["name"] == "MeetingDestroyedEvtMsg":
    #             os.system("rm -f /var/freeswitch/meetings/%s.wav" % meeting)
    if text:
        print(text)
    where = file.tell()
    line = file.read()
    if not line:
        time.sleep(0.1)
        file.seek(where)
    else:
        red.publish("audio_data", line)
