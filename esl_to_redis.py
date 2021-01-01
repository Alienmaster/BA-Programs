from jaspion import Jaspion
import redis
import json

records = {}
app = Jaspion(host='127.0.0.1', port=8021, password='042f799c91402289')

red = redis.Redis(host="localhost", port=6379, password="")


@app.handle('MEDIA_BUG_START')
def media_bug_start(event):
    print("MEDIA_BUG_START")
    conference = get_conference(records, event)
    CallerDestinationNumber = event["Caller-Destination-Number"]
    
    

    OrigCallerIDName = event["Caller-Orig-Caller-ID-Name"]
    Media_Bug_Target = event["Media-Bug-Target"]
    Media_Bug_Function = event["Media-Bug-Function"]

    start_MB = {"Action" : "Media-Bug-Start", "Caller-Destination-Number" : CallerDestinationNumber, "Media-Bug-Target" : Media_Bug_Target}
    send_to_pubsub(start_MB)

    if OrigCallerIDName not in conference.keys():
        conference[OrigCallerIDName] = {}
    
    conference[OrigCallerIDName]["Media-Bug-Target"] = Media_Bug_Target
    conference[OrigCallerIDName]["Media-Bug-Function"] = Media_Bug_Function
    conference[OrigCallerIDName]["running"] = 1

    send_to_pubsub(conference)

@app.handle('MEDIA_BUG_STOP')
def media_bug_stop(event):
    print("MEDIA_BUG_STOP")
    conference = get_conference(records, event)

    OrigCallerIDName = event["Caller-Orig-Caller-ID-Name"]
    Media_Bug_Function = event["Media-Bug-Function"]
    Media_Bug_Target = event["Media-Bug-Target"]

    CallerDestinationNumber = event["Caller-Destination-Number"]
    stop_MB = {"Action" : "Media-Bug-Stop", "Caller-Destination-Number" : CallerDestinationNumber, "Media-Bug-Target" : Media_Bug_Target}
    send_to_pubsub(stop_MB)

    if Media_Bug_Function == "session_record":
        Caller_Username = event["Caller-Username"]
        if Caller_Username in conference.keys():
            conference[Caller_Username]["running"] = 0
    send_to_pubsub(conference)


@app.handle('conference::maintenance')
def conference_maintenance(event):
    print("conference_maintenance")
    Action = event["Action"]
    if Action in ("del-member", "add-member"):
        conference = get_conference(records, event)
        Caller_Username = event["Caller-Username"]
    
        if Action == "del-member":
            member = conference.pop(Caller_Username, None)
            del_member = {"Action" : "del_member", "member" : member}
            send_to_pubsub(del_member)
            print(del_member)
            send_to_pubsub(conference)
            
        
        if Action == "add-member":
            conference[Caller_Username]["Caller-Destination-Number"] = event["Caller-Destination-Number"]
    
        send_to_pubsub(conference)

def get_conference(record_dict, event):
    Caller_Destination_Number = event["Caller-Destination-Number"]
    if Caller_Destination_Number in record_dict.keys():
        return record_dict[Caller_Destination_Number]
    else:
        RV = record_dict[Caller_Destination_Number] = {}
        return RV

def send_to_pubsub(data):
    data2 = json.dumps(data)
    # print(data2)
    red.publish("test_channel", data2)


if __name__ == '__main__':
    app.run()