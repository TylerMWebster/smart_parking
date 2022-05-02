import requests
import json

def post_status(device_id, status):
    request_dict = {'device_id':device_id, 'status':status}
    request_json = json.dumps(request_dict)
    #print('Posting status')
    print(request_json)

def post_status_req(url, device_id, status):
    request_dict = {'device_id':device_id, 'status':status}
    request_json = json.dumps(request_dict)
    #print('Posting status')
    req = requests.post(url, json=request_json)
    print(request_json)
    print(req.status_code)


if __name__ == '__main__':
    post_status_req('http://127.0.0.1:5000/push-data',1, 'True')