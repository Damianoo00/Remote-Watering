import time
import requests

url = 'http://127.0.0.1:5000/api/programm?ip=192.168.1.95&rack=0&slot=1&db=0&start_addr=0&programm_id=classic'

url_output = 'http://127.0.0.1:5000/api/digital/output?ip=192.168.1.95&rack=0&slot=1&db=0&start_addr=0&value='

if (requests.get(url=url).status_code == 200):
    res = requests.get(url=url)
    programm = res.json()
    for step in programm:
        print(f"Set [{step['value']}] [{step['time']}]")
        requests.post(url=f"{url_output}{step['value']}")
        time.sleep(step['time'])
    requests.delete('http://127.0.0.1:5000/api/programm?ip=192.168.1.95&rack=0&slot=1&db=0&start_addr=0&programm_id=classic')