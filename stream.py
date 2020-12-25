import time
import os
import redis
import json
import argparse
import greenswitch
import inspect
import gevent

def send_file_redis(filename):
    # Open the file
    file = open(filename,'rb', buffering=2048)

    # Find the actual size of the file and move to the end
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--filename", required=False, type=str)
    parser.add_argument("-p", "--password", type=str)

    args = parser.parse_args()
    filename = args.filename
    esl_password = args.password
    get_info_esl(esl_password)
    
    # send_file_redis(filename)