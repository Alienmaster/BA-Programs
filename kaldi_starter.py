import os
import redis
import json
import multiprocessing as mp

red = redis.Redis(host="ltbbb2", port=6379, password="")

data_channel = "test_channel"

kaldi_instances = {}

def start_kaldi(input, output):
    os.chdir("/home/bbb/ba/kaldi_modelserver_bbb")
    os.system("pykaldi_bbb_env/bin/python3.7 nnet3_model.py -m 0 -e -t -y models/kaldi_tuda_de_nnet3_chain2.yaml --redis-audio=%s --redis-channel=%s -fpc 190" %  (input, output))


def wait_for_channel():
    pubsub = red.pubsub()
    pubsub.subscribe(data_channel)

    while True:
        message = pubsub.get_message()
        if message and message["data"] != 1:
            message = json.loads(message["data"].decode("UTF-8"))
            print(message)
            try:
                input_channel = message["ASR-Channel"]
                output_channel = message["Caller-Orig-Caller-ID-Name"].replace(" ", ".") + "_data"
                CallerDestinationNumber = message["Caller-Destination-Number"]
                OrigCallerIDName = message["Caller-Orig-Caller-ID-Name"]
                CallerUsername = message["Caller-Username"]
                meetingId = message["meetingId"]
                if message["Event"] == "LOADER_START":
                    print("Start Kaldi")
                    p = mp.Process(target=start_kaldi, args=(input_channel, output_channel,))
                    p.start()
                    kaldi_instances[input_channel] = p
                    
                    Loader_Start_msg = {"Event" : "KALDI_START", "Caller-Destination-Number" : CallerDestinationNumber, "meetingId" : meetingId, "Caller-Orig-Caller-ID-Name" : OrigCallerIDName, 'Caller-Username': CallerUsername, "Input-Channel" : input_channel, "ASR-Channel" : output_channel}
                    red.publish(data_channel, json.dumps(Loader_Start_msg))
                
                if message["Event"] == "LOADER_STOP":
                    input_channel = message["ASR-Channel"]
                    print("Stop Kaldi")
                    p = kaldi_instances.pop(input_channel, None)
                    if p:
                        p.terminate()
                        Loader_Stop_msg = {"Event" : "KALDI_STOP", "Caller-Destination-Number" : CallerDestinationNumber, "meetingId" : meetingId, "Caller-Orig-Caller-ID-Name" : OrigCallerIDName, 'Caller-Username': CallerUsername, "Input-Channel" : input_channel, "ASR-Channel" : output_channel}
                        red.publish(data_channel, json.dumps(Loader_Stop_msg))
            except:
                pass



if __name__ == "__main__":
    wait_for_channel()