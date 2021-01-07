import redis
import os
import time
import multiprocessing as mp

def sendFileToRedis(filename, channel):
    red = redis.Redis(host="localhost", port=6379, password="")
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
    p = mp.Process(target=sendFileToRedis, args=("/var/freeswitch/meetings/2021-01-01-20-07-08_ECHO_TO_CONFERENCE_write.wav", "test1",))
    r = mp.Process(target=sendFileToRedis, args=("/var/freeswitch/meetings/2021-01-01-20-04-52_ECHO_TO_CONFERENCE_write.wav", "test2",))
    p.start()
    r.start()
    time.sleep(30)
    p.terminate()
    time.sleep(10)
    r.terminate()