#!/usr/bin/env python3
import re
import operator
import sys
import csv

errors_message = {}
user_stats = {}
errors_report = 'error_message.csv'
per_user_report = 'user_statistics.csv'
logfile='syslog.log'
all_data_array = []
error_data_array = []
info_data_array = []
line_stripped = ""
errors_message_fields = ['Error','Count']
user_stats_fields = ['Username','INFO','ERROR']

with open(logfile, 'r') as file:
        for line in file.readlines():
                line_stripped = line.rstrip("\n")
                if bool(re.search(r"ticky: ERROR", line_stripped)):
                        if line_stripped.split(r"ERROR ")[1].split(r" (")[0].strip() not in errors_message.keys():
                                errors_message[line_stripped.split(r"ERROR ")[1].split(r" (")[0].strip()] = 0
                        errors_message[line_stripped.split(r"ERROR ")[1].split(r" (")[0].strip()]+=1

                        if line_stripped.split(r" (")[1].rstrip(")") not in user_stats.keys():
                                user_stats[line_stripped.split(r" (")[1].rstrip(")")] = [0,0]
                        user_stats[line_stripped.split(r" (")[1].rstrip(")")][1]+=1

                elif bool(re.search(r"ticky: INFO", line_stripped)):
                        if line_stripped.split(r" (")[1].rstrip(")") not in user_stats.keys():
                                user_stats[line_stripped.split(r" (")[1].rstrip(")")] = [0,0]
                        user_stats[line_stripped.split(r" (")[1].rstrip(")")][0]+=1

def sort_reverse_dict(temp_dict):
        return sorted(temp_dict.items(), key=operator.itemgetter(1), reverse=True)

def sort_dict(temp_dict2):
        return sorted(temp_dict2.items(), key=operator.itemgetter(0))

errors_message = sort_reverse_dict(errors_message)
user_stats = sort_dict(user_stats)

csv_data_row_errors_message = []
csv_data_row_user_stats = []

for key,values in errors_message:
        csv_data_row_errors_message.append({errors_message_fields[0]:key,errors_message_fields[1]:values})

with open(errors_report, 'w') as errors_message_csvfile:
        writer1 = csv.DictWriter(errors_message_csvfile, fieldnames = errors_message_fields)
        writer1.writeheader()
        writer1.writerows(csv_data_row_errors_message)

for key,values in user_stats:
        csv_data_row_user_stats.append({user_stats_fields[0]:key,user_stats_fields[1]:values[0],user_stats_fields[2]:values[1]})

with open(per_user_report, 'w') as user_stats_csvfile:
        writer1 = csv.DictWriter(user_stats_csvfile, fieldnames = user_stats_fields)
        writer1.writeheader()
        writer1.writerows(csv_data_row_user_stats)
