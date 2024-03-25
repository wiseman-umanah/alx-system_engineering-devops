#!/usr/bin/python3
"""Module to save information about
employee in csv file"""
if __name__ == "__main__":
    import csv
    from sys import argv
    import requests

    link = f"https://jsonplaceholder.typicode.com/users/{argv[1]}"
    res = requests.get(link)
    task = requests.get(f"{link}/todos")
    employeeName = res.json().get("username")
    todos = task.json()
    with open(f"{argv[1]}.csv", "w") as csv_file:
        csv_write = csv.writer(csv_file)
        for i in todos:
            csv_write.writerow([argv[1], employeeName,
                                i["completed"], i["title"]])
