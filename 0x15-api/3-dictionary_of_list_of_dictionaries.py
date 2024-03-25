#!/usr/bin/python3
"""Module to export employee's details
to be save to JSON"""
if __name__ == "__main__":
    import json
    import requests

    employID = {}
    link = f"https://jsonplaceholder.typicode.com/users"
    res = requests.get(link).json()
    for employee in res:
        employeeName = employee.get("username")
        task = requests.get(f"{link}/{employee.get('id')}/todos")
        todos = task.json()
        temp = []
        for i in todos:
            employtask = {}
            employtask["task"] = i["title"]
            employtask["completed"] = i["completed"]
            employtask["username"] = employeeName
            temp.append(employtask)
        employID[employee.get('id')] = temp

    with open(f"todo_all_employees.json", "w") as json_file:
        json_obj = json.dumps(employID)
        json_file.write(json_obj)
