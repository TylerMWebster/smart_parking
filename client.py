from requests import request
import json

def post_status(device_id, status):
    request_dict = {'device_id':device_id, 'status':status}
    request_json = json.dumps(request_dict)
    print('Posting status')
    print(request_json)

if __name__ == '__main__':
    post_status(12, True)