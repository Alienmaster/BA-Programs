import redis
import os
import time

class Uploader:
    def __init__(self, filename, channel):
        self._red = redis.Redis(host="localhost", port=6379, password="")

        self.sendFileToRedis(filename, channel)

    def sendFileToRedis(self, filename, channel):
        red = self._red
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
    nu1 = Uploader("/var/freeswitch/meetings/2020-12-25-21-36-45_ECHO_TO_CONFERENCE_write.wav", "test1")
    nu2 = Uploader("/var/freeswitch/meetings/2020-12-25-21-51-36_ECHO_TO_CONFERENCE_write.wav", "test2")