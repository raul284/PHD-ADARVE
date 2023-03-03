import os
import json
import pandas as pd
from datetime import datetime, timedelta

class ProcessRawData:

    users_data: dict

    def __init__(self) -> None:
        self.users_data = {}

        users_ids = [subdirs[1] for subdirs in os.walk("../data")][0]
        users_dirs = ["../data/{}".format(user_id) for user_id in users_ids]

        for index in range(len(users_dirs)):
            self.users_data[users_ids[index]] = {}
            for filename in os.listdir("{0}/raw".format(users_dirs[index])):
                if filename.endswith(".txt"):
                    data = self.txt_to_dict("{0}/raw/{1}".format(users_dirs[index], filename))
                    data["raw_signal"].to_csv("{0}/raw.csv".format(users_dirs[index]), index=False)
                    self.users_data[users_ids[index]]["raw_data"] = data


        for user_id in users_ids:
            if not os.path.exists("../results/{0}".format(user_id)):
               os.makedirs("../results/{0}".format(user_id))

        for index in range(len(users_ids)):
            self.users_data[users_ids[index]]["parts"] = self.singal_partitions(users_ids[index], self.users_data[users_ids[index]]["raw_data"])

    def txt_to_dict(self, filename):
        result = {
            "time": "", 
            "hz": "", 
            "col_names": [], 
            "signal": pd.DataFrame}

        lines = []
        with open(filename) as f:
            lines = f.readlines()

        raw_info = json.loads(lines[1][2:])["A4:34:F1:21:5F:73"]
        time_str = str(raw_info["time"].partition(".")[0])
        result["time"] = datetime.strptime(time_str, '%H:%M:%S').strftime('%H:%M:%S')
        result["hz"] = raw_info["sampling rate"]
        result["col_names"] = raw_info["column"]

        #print(result["time"])
        
        filtered_data = ""
        for line in lines[3:]:
            filtered_data += ' '.join(line.split()).replace(' ', ',') + "\n"
        
        result["raw_signal"] = pd.DataFrame([x.split(',') for x in filtered_data[:-1].split('\n')])

        return result

    def singal_partitions(self, id, data):

        if not os.path.exists("../data/{0}/parts".format(id)):
            os.makedirs("../data/{0}/parts".format(id))
        if not os.path.exists("../results/{0}/parts".format(id)):
            os.makedirs("../results/{0}/parts".format(id))

        parts = json.load(open("../data/{0}/parts.json".format(id)))
        signal_start = datetime.strptime(data["time"], '%H:%M:%S')

        if not parts["hasParts"]:
            return []

        result = {}

        for part in parts["parts"]:
            if not os.path.exists("../results/{0}/parts/{1}".format(id, part["id"])):
               os.makedirs("../results/{0}/parts/{1}".format(id, part["id"]))

            start_time_dt = datetime.strptime(part["start_time"], '%H:%M:%S')
            stop_time_dt = datetime.strptime(part["stop_time"], '%H:%M:%S')

            start_index = int((start_time_dt - signal_start).total_seconds() * 100)
            stop_index = int((stop_time_dt - signal_start).total_seconds() * 100)

            print(start_index, stop_index)
            result[part["id"]] = {
                "start_time": start_time_dt.strftime('%H:%M:%S'),
                "start_index": start_index,
                "stop_time": stop_time_dt.strftime('%H:%M:%S'),
                "stop_index": stop_index,
                "data": data["raw_signal"].iloc[start_index - 1: stop_index + 1]
            }

            result[part["id"]]["data"].to_csv("../data/{0}/parts/{1}.csv".format(id, part["id"]), index=False)
            
