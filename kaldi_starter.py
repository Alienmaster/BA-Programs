import os
import redis

red = redis.Redis(host="ltbbb2", port=6379, password="")

def start_kaldi():
    os.system("../projects/")



if __name__ == "__main__":
    start_kaldi()