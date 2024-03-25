#!/usr/bin/python3
"""Module to export employee's details
to be save to JSON"""
import requests
import json
from sys import argv


link = f"https://jsonplaceholder.typicode.com/users/{argv[1]}"
res = requests.get(link)
task = requests.get(f"{link}/todos")
employeeName = res.json().get("username")
todos = task.json()
employID = {}
temp = []
for i in todos:
    employtask = {}
    employtask["task"] = i["title"]
    employtask["completed"] = i["completed"]
    employtask["username"] = employeeName
    temp.append(employtask)
employID[argv[1]] = temp

with open(f"{argv[1]}.json", "w") as json_file:
    json_obj = json.dumps(employID)
    json_file.write(json_obj)
