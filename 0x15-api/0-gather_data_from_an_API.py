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
    num_todos = len(todos)
    completed = []
    for i in todos:
        if i["completed"] is True:
            completed.append(i["title"])
    num_com = len(completed)
    with open("student_output", "w") as file:
        string = f"Employee {employeeName} is done with tasks"
        file.write(f"{string}({num_com}/{num_todos}):\n")
        print(f"{string}({num_com}/{num_todos}):")
    with open("student_output", "a") as file:
        for i in completed:
            file.write("\t " + i + "\n")
            print("\t", i)
