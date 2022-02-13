import requests

BASE_URL = "http://localhost:8888"

def check_server_lamp(id) -> bool:
    api_url = BASE_URL + "/lamp"
    print(api_url)
    # response = requests.get(api_url, timeout = 5)
    response = requests.get(api_url, params={'id':id}, timeout = 5)
    # print(response.json())
    # print(response.status_code)
    lamp_status = response.json()
    temp = response.content
    return lamp_status

def set_color() -> bool:
    api_url = BASE_URL + "/lamp/setcolor"
    print(api_url)
    # response = requests.get(api_url, timeout = 5)
    body={'id':'amanda', 'color':'#00080'}
    response = requests.post(api_url, json=body, timeout = 5)
    # print(response.json())
    # print(response.status_code)
    lamp_status = response.json()
    temp = response.content
    return lamp_status

print(check_server_lamp('amanda'))
# print(set_color())