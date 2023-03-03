import os

from user import User
from biosignals.process_rawdata import ProcessRawData

def create_users(data):
    users = []
    for d in data:
        new_user = User(d, data[d])
        users.append(new_user)
    return users


def main():
    process_rawdata = ProcessRawData()
    users_data = process_rawdata.users_data

    '''users = create_users(users_data)

    ecg_lists = []
    eda_lists = []
    for user in users:
        ecg_lists += user.baseline_ecg.filtered_signals + user.ingame_ecg.filtered_signals
        eda_lists += user.baseline_eda.filtered_signals + user.ingame_eda.filtered_signals

    for user in users:
        user.create_graphs([int(min(ecg_lists)) - 50, int(max(ecg_lists)) + 50], [int(min(eda_lists)) - 50, int(max(eda_lists)) + 50])'''
    

if __name__ == "__main__":
    main()