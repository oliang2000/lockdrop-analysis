import json
import csv
from substrateinterface import SubstrateInterface, Keypair, SubstrateRequestException
from scalecodec.type_registry import load_type_registry_file

file_path = "./sample.json"
froot = './data/2ndclaim'
write_path = "./data/2ndclaim/summary.csv"

custom_type_registry = load_type_registry_file("types/plasm.json")

substrate = SubstrateInterface(
    url="wss://rpc.plasmnet.io",
    address_type=5,
    type_registry_preset='plasm',
    type_registry=custom_type_registry
)

def get_claim_id(params):
    return params[0]["value"]

def write_csv(event):
    with open(write_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(event)

def get_claim_call(claim_id):
    print('get_claim_info', claim_id)
    try:
        claim_info = substrate.get_runtime_state(
            module='PlasmLockdrop',
            storage_function='Claims',
            params=[claim_id]
        ).get('result')
    except Exception as e:
        print(e)
    print('claim_info', claim_info)

    if claim_info:
        print("\n\nCurrent claim: ", claim_info)

    return claim_info

sum = 0
for i in range(0,500):
    fname = "{}/{}_events.json".format(froot,i)
    try:
        with open(fname, "r") as json_file:
            body = json.load(json_file)
            if body["data"]["events"] == None:
                exit(0)
            event_list = body["data"]["events"]
            for event in event_list:
                print('event', event['params'])
                event_dict = json.loads(event['params'])
                id = get_claim_id(event_dict)
                claim = get_claim_call(id)
                print('event:', id)

    except:
        print('not found.')
        exit(0)
