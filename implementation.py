import time
import yaml
import requests
import os
import sys
def send_http_request(endpoint):
    try:
        if endpoint.get("method") is None:
            response = requests.get(endpoint['url'])
        else:
            if endpoint["method"]== "GET":
                response = requests.get(endpoint['url'])
            elif endpoint['method']=='POST':
                response= requests.post(endpoint['url'], endpoint['body'])
        if response.status_code>=200 and response.status_code<=299 and response.elapsed.total_seconds() < 0.5:
            return "UP"
        else:
            return "DOWN"
    except Exception as e:
        return "DOWN"

def calculate_percentage(up_count, total_count):
    if total_count == 0:
        return 0
    return round(100 * (up_count / total_count))

def main(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    url_status_dict={}

    try:
        while True:
            for endpoint in config:
                result = send_http_request(endpoint)
                domain = endpoint['url'].split('//')[1].split('/')[0]
                if domain not in url_status_dict:
                    url_status_dict[domain]={'up_status':0, 'total':0}
                if result == "UP":
                    url_status_dict[domain]['up_status'] += 1
                url_status_dict[domain]['total'] += 1

            for url, status in url_status_dict.items():
                availability_percentage = calculate_percentage(status['up_status'], status['total'])
                print(f"{url} has {availability_percentage}% availability percentage")

            time.sleep(15)
    
    #Press Ctrl+C to abort
    except KeyboardInterrupt:
        print("Exiting the program.")

if __name__ == "__main__":
    fn = sys.argv[1]
    if os.path.exists(fn):
        config_file_path= fn
    main(config_file_path)
