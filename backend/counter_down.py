import time
import requests

url = 'http://127.0.0.1:5000/api/counter?name=step1'
counter = 0

while (requests.get(url=url).status_code == 200 and counter > -1):
    res = requests.get(url=url)
    counter = res.json()["time"]
    print(f"counter: [{counter}]")
    time.sleep(1)
    counter -= 1
    if counter > -1:
        obj = {
            "time" : counter
        }
        res = requests.post(url=url, json=obj)
        if res.status_code != 200:
            print(f"Error: Status[{res.status_code}]")
    else:
        res = requests.delete(url=url)
        if res.status_code != 200:
            print(f"Error: Status[{res.status_code}]")