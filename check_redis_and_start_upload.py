import redis
import json
import file_to_redis
import multiprocessing as mp

red = redis.Redis(host="localhost", port=6379, password="")

pubsub = red.pubsub()

pubsub.subscribe("test_channel")

mp.get_context("spawn")
rr = {}

def wait_for_start():
    while True:
        message = pubsub.get_message()
        if message:
            if message["data"] != 1:
                text = json.loads(message["data"].decode("UTF-8"))
                print(text)
                if "Action" in text.keys():
                    if text["Action"] == "Media-Bug-Start":
                        MBT = text["Media-Bug-Target"]
                        print("Start Bug")
                        p = mp.Process(target=file_to_redis.sendFileToRedis, args=(MBT, "test1",))
                        p.start()
                        rr[MBT] = p
                    if text["Action"] == "Media-Bug-Stop":
                        MBT = text["Media-Bug-Target"]
                        print("Remove Bug")
                        p = rr[MBT]
                        p.terminate()


if __name__ == "__main__":
    mp.get_context("spawn")
    wait_for_start()
    # p = mp.Process(target=sendFileToRedis, args=("/var/freeswitch/meetings/2021-01-01-20-07-08_ECHO_TO_CONFERENCE_write.wav", "test1",))
    # r = mp.Process(target=sendFileToRedis, args=("/var/freeswitch/meetings/2021-01-01-20-04-52_ECHO_TO_CONFERENCE_write.wav", "test2",))
    # p.start()
    # r.start()
    # time.sleep(30)
    # p.terminate()
    # time.sleep(10)
    # r.terminate()