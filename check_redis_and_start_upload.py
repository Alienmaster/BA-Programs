import redis
import json
import os
import multiprocessing as mp
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

red = redis.Redis(host="localhost", port=6379, password="")
pubsub = red.pubsub()
data_channel = ["test_channel", "from-akka-apps-redis-channel"]

pubsub.subscribe(data_channel)

conferences = {}

loader = {}

def handle_loader():
    while True:
        message = pubsub.get_message()
        if message and message["data"] not in [1, 2]:
            message = json.loads(message["data"].decode("UTF-8"))
            try:
                if "Event" in message.keys():
                    Media_Bug_Target = message["Media-Bug-Target"]
                    CallerDestinationNumber = message["Caller-Destination-Number"]
                    OrigCallerIDName = message["Caller-Orig-Caller-ID-Name"]
                    CallerUsername = message["Caller-Username"]
                    meetingId = conferences[CallerDestinationNumber]
                    redis_channel = meetingId + "%" + CallerUsername.replace(" ", ".") + "%asr"
                    if message["Event"] == "MEDIA_BUG_START":
                        logger.info("Media Bug Start")
                        logger.debug(message)
                        p = mp.Process(target=sendFileToRedis, args=(Media_Bug_Target, redis_channel,))
                        p.start()
                        loader[Media_Bug_Target] = p
                        Loader_Start_msg = {"Event" : "LOADER_START", "Caller-Destination-Number" : CallerDestinationNumber, "meetingId" : meetingId, "Caller-Orig-Caller-ID-Name" : OrigCallerIDName, "Caller-Username" : CallerUsername, "ASR-Channel" : redis_channel}
                        red.publish(data_channel[0], json.dumps(Loader_Start_msg))

                    if message["Event"] == "MEDIA_BUG_STOP":
                        logger.debug("Media Bug Stop")
                        logger.info(message)
                        p = loader.pop(Media_Bug_Target, None)
                        if p:
                            p.terminate()
                            Loader_Stop_msg = {"Event" : "LOADER_STOP", "Caller-Destination-Number" : CallerDestinationNumber, "meetingId" : meetingId, "Caller-Orig-Caller-ID-Name" : OrigCallerIDName,  "Caller-Username" : CallerUsername, "ASR-Channel" : redis_channel}
                            red.publish(data_channel[0], json.dumps(Loader_Stop_msg))
                            os.remove(Media_Bug_Target)

                if "envelope" in message.keys():
                    
                    if message["envelope"]["name"] == "VoiceCallStateEvtMsg":
                        logger.info("VoiceCallStateEvtMsg")
                        logger.debug(message)
                        message = message["core"]["body"]
                        voiceConf = message["voiceConf"]
                        meetingId = message["meetingId"]
                        conferences[voiceConf] = meetingId
                        # print(message["voiceConf"])
                        # print(message["meetingId"])
            except:
                pass
    

def sendFileToRedis(filename, channel):
    # Open the file
    file = open(filename,'rb', buffering=2048)
    logger.debug("Opened File: " + filename)
    # Find the actual size of the file and move to the end
    st_results = os.stat(filename)
    st_size = st_results[6]
    file.seek(st_size)

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