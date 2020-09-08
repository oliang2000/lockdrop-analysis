import json
import csv

file_path = "./sample.json"
froot = './data/2nd'
write_path = "./data/2nd/summary.csv"

def get_account_id(params):
    return params[1]["value"]
def get_value(params):
    return params[2]["value"]

def write_csv(event):
    with open(write_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(event)


sum = 0
for i in range(0,500):
    fname = "{}/{}_events.json".format(froot,i)
    try:
        with open(fname, "r") as json_file:
            body = json.load(json_file)
            if body["data"]["events"] == None:
                print('total issued plm', sum)
                exit(0)
            event_list = body["data"]["events"]
            for event in event_list:
                print('event', event['params'])
                event_dict = json.loads(event['params'])
                id = get_account_id(event_dict)
                value = get_value(event_dict)
                print('event:[]', id, value)
                write_csv([id, value])
                sum += int(value)
    except:
        print('not found.')
        print('total issued plm', sum)
        exit(0)
