#!/usr/bin/python3
"""Module to display for a given employee ID,
returns information about his/her TODO list progress."""
if __name__ == "__main__":
    import requests
    from sys import argv

    link = f"https://jsonplaceholder.typicode.com/users/{argv[1]}"
    res = requests.get(link)
    task = requests.get(f"{link}/todos")
    employeeName = res.json().get("name")
    todos = task.json()
    completed = []
    for i in todos:
        if i["completed"] is True:
            completed.append(i["title"])
    string = f"Employee {employeeName} is done with tasks"
    print(f"{string}({len(completed)}/{len(todos)}):")
    for i in completed:
        print("\t", i)
