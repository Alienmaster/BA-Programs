from jaspion import Jaspion
import redis
import json

app = Jaspion(host='127.0.0.1', port=8021, password='042f799c91402289')

red = redis.Redis(host="localhost", port=6379, password="")


@app.handle('MEDIA_BUG_START')
def media_bug_start(event):
    CallerDestinationNumber = event["Caller-Destination-Number"]
    Event = event["Event-Name"]
    OrigCallerIDName = event["Caller-Orig-Caller-ID-Name"]
    Media_Bug_Target = event["Media-Bug-Target"]
    Media_Bug_Function = event["Media-Bug-Function"]
    
    if Media_Bug_Function == "session_record":
        start_MB = {"Event" : Event, "Caller-Destination-Number" : CallerDestinationNumber, "Caller-Orig-Caller-ID-Name" : OrigCallerIDName, "Media-Bug-Target" : Media_Bug_Target}
        send_to_pubsub(start_MB)


@app.handle('MEDIA_BUG_STOP')
def media_bug_stop(event):
    CallerDestinationNumber = event["Caller-Destination-Number"]
    Event = event["Event-Name"]
    OrigCallerIDName = event["Caller-Orig-Caller-ID-Name"]
    Media_Bug_Target = event["Media-Bug-Target"]
    Media_Bug_Function = event["Media-Bug-Function"]
    
    if Media_Bug_Function == "session_record":
        stop_MB = {"Event" : Event, "Caller-Destination-Number" : CallerDestinationNumber, "Caller-Orig-Caller-ID-Name" : OrigCallerIDName, "Media-Bug-Target" : Media_Bug_Target}
        send_to_pubsub(stop_MB)


def send_to_pubsub(data):
    data = json.dumps(data)
    red.publish("test_channel", data)


if __name__ == '__main__':
    app.run()