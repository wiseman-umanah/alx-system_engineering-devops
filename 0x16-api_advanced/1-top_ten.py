#!/usr/bin/python3
"""a function that queries the Reddit API
and prints the titles of the first 10 hot posts
listed for a given subreddit."""
import requests


def top_ten(subreddit):
    """The function to implement the logic"""
    try:
        link = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
        r = requests.get(link, headers={"User-Agent": "My-User-Agent"})
        for i in r.json().get("data").get("children"):
            print(i["data"]["title"])
    except Exception:
        print(None)
