import redis
import json
import os
import multiprocessing as mp
import time

red = redis.Redis(host="localhost", port=6379, password="")

pubsub = red.pubsub()

data_channel = "test_channel"

pubsub.subscribe(data_channel)

rr = {}

def handle_loader():
    while True:
        message = pubsub.get_message()
        if message and message["data"] != 1:
            message = json.loads(message["data"].decode("UTF-8"))
            print(message)
            try:
                if message["Event"] == "MEDIA_BUG_START":
                    print("Start Bug")
                    Media_Bug_Target = message["Media-Bug-Target"]
                    redis_channel = message["Caller-Orig-Caller-ID-Name"].replace(" ", ".") + "_asr"
                    CallerDestinationNumber = message["Caller-Destination-Number"]
                    OrigCallerIDName = message["Caller-Orig-Caller-ID-Name"]


                    p = mp.Process(target=sendFileToRedis, args=(Media_Bug_Target, redis_channel,))
                    p.start()
                    rr[Media_Bug_Target] = p
                    
                    Loader_Start_msg = {"Event" : "LOADER_START", "Caller-Destination-Number" : CallerDestinationNumber, "Caller-Orig-Caller-ID-Name" : OrigCallerIDName, "ASR-Channel" : redis_channel}
                    red.publish(data_channel, json.dumps(Loader_Start_msg))
                if message["Event"] == "MEDIA_BUG_STOP":
                    MBT = message["Media-Bug-Target"]
                    print("Remove Bug")
                    p = rr.pop(MBT, None)
                    if p:
                        p.terminate()
            except:
                pass


def sendFileToRedis(filename, channel):
    # Open the file
    file = open(filename,'rb', buffering=2048)

    # Find the actual size of the file and move to the end
    st_results = os.stat(filename)
    st_size = st_results[6]
    file.seek(st_size)

    pubsub = red.pubsub()
    meeting = 0
    while True:
        where = file.tell()
        line = file.read()
        if not line:
            time.sleep(0.1)
            file.seek(where)
        else:
            red.publish(channel, line)


if __name__ == "__main__":
    mp.get_context("spawn")
    handle_loader()