import json
import csv

events_path = './data/events.json'
txs_path = './data/txs.json'

with open(events_path, 'r') as f:
    events = json.load(f)

with open(txs_path, 'r') as f:
    txs = json.load(f)

def day_to_bonus(day):
    if day < 30:
        return 0
    elif day < 100:
        return 24
    elif day < 300:
        return 100
    elif day < 1000:
        return 360
    else:
        return 1600

TOTAL_ISSUE_PLM = 500000000
TOTAL_LOCKDROP_PLM = TOTAL_ISSUE_PLM * 17/20
total_issue_ratio = 0
eth_exchange_rate = 156.36
tx_issue_rate = {}

for event in events['result']:
    # value
    value = int(event['topics'][1], 16)
    # day
    day = int(event['topics'][2], 16)
    issue_ratio = value * day_to_bonus(day) * eth_exchange_rate
    # print(value, day)
    total_issue_ratio += issue_ratio
    tx_issue_rate[event['transactionHash']] = issue_ratio

print(total_issue_ratio)

address_list = []
plm_list = {}

for tx in txs['result']:
    hash = tx['hash']
    address = tx['from']
    if not hash in tx_issue_rate:
        continue
    issued_plm = TOTAL_LOCKDROP_PLM * tx_issue_rate[hash] / total_issue_ratio
    if address in plm_list:
        plm_list[address] += issued_plm
    else:
        plm_list[address] = issued_plm
    


for (address, plm) in plm_list.items():
    print(address, plm)

# /1e-18 because of wei.
alpha_1 = TOTAL_LOCKDROP_PLM/total_issue_ratio/1e-18
print('alpha_1', alpha_1)
alpha_2 = alpha_1 * 5/6
alpha_3 = alpha_1 * 4/6

print('alpha_2', alpha_2)
print('alpha_3', alpha_3)

with open('data/out.csv', 'w') as f:
    writer = csv.writer(f)
    for (address, plm) in plm_list.items():
        writer.writerow([address, plm])
