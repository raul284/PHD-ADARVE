import json
from datetime import datetime

def haz_todo():

    for name in ["AAAA", "AAAB", "AAAC"]:
        f = open('../results/exp1/users/{0}.json'.format(name))
        data = json.load(f)
        for phase in data["phase"]:
            data["phase"][phase]["start_time"] = int(datetime.strptime(data["phase"][phase]["start_time"], "%Y-%m-%d %H:%M:%S").timestamp())
            data["phase"][phase]["end_time"] = int(datetime.strptime(data["phase"][phase]["end_time"],"%Y-%m-%d %H:%M:%S").timestamp())
            data["phase"][phase]["duration"] = int((datetime.strptime(data["phase"][phase]["duration"],'%M:%S')- datetime(1900, 1, 1)).total_seconds())

        for event_type in data["events"]:
            for phase in data["events"][event_type]:
                raw_copy = data["events"][event_type][phase]["raw"]
                data["events"][event_type][phase]["raw"] = []
                for e in raw_copy:
                    e["event_type"] = e["event_type"].replace("CA_", "")
                    e["event_datetime"] = int(datetime.strptime(e["event_datetime"],"%Y-%m-%d %H:%M:%S").timestamp())
                    data["events"][event_type][phase]["raw"].append(e)
                
                cleaned_copy = data["events"][event_type][phase]["cleaned"]
                data["events"][event_type][phase]["cleaned"] = []
                for e in cleaned_copy:
                    e["event_type"] = e["event_type"].replace("CA_", "")
                    e["event_datetime"] = int(datetime.strptime(e["event_datetime"],"%Y-%m-%d %H:%M:%S").timestamp())
                    data["events"][event_type][phase]["cleaned"].append(e)


        with open('../results/exp1/users/copy_{0}.json'.format(name), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)