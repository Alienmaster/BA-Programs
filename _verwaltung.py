import redis
import json

class dataSender:
    
    def __init__(self):
        self._red = redis.Redis()
        self.subscribe()

    def subscribe(self):
        red = self._red
        pubsub = red.pubsub()
        pubsub.subscribe("test_channel")
        self._pubsub = pubsub

    def get_redis_msg(self):
        pubsub = self._pubsub

        while True:
            message = pubsub.get_message()
            if message is not None:
                if message is not 1:
                    print(message)
    


if __name__ == "__main__":
    sender = dataSender()
    sender.get_redis_msg()
