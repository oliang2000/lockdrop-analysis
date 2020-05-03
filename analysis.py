import json
import csv
from introducers import introducers
from crypto import recover_transaction

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

def is_valid_intro(introducer):
    return introducer in introducers

def add_list_num(arr, address, num):
    if address in arr:
        arr[address] += num
    else:
        arr[address] = num

def get_or(arr, address):
    if address in arr:
        return arr[address]
    else:
        return 0

def get_or_str(arr, address):
    if address in arr:
        return bg_str(arr[address])
    else:
        return '0'

def bg_str(num):
    return '{:d}'.format(num)

FEMTO = 1000000000000000
TOTAL_ISSUE_PLM = 500000000 * FEMTO
TOTAL_LOCKDROP_PLM = TOTAL_ISSUE_PLM * 17 // 20
total_issue_ratio = 0
# curl -X GET "https://api.coingecko.com/api/v3/coins/ethereum/history?date=01-05-2020&localization=false" -H "accept: application/json"
eth_exchange_rate = 20555600541063674
eth_exchange_rate_div = 100000000000000
WEI = 1000000000000000000

tx_issue_rate = {}
tx_introducer = {}
tx_issue_plm = {}

for event in events['result']:
    # value
    value = int(event['topics'][1], 16)
    # day
    day = int(event['topics'][2], 16)
    introducer = '0x' + event['data'][-40:]
    issue_ratio = value * day_to_bonus(day) * eth_exchange_rate // eth_exchange_rate_div
    print('issue_ratio', issue_ratio)
    tx_hash = event['transactionHash']

    total_issue_ratio += issue_ratio
    tx_issue_rate[tx_hash] = issue_ratio
    tx_introducer[tx_hash] = introducer


print(total_issue_ratio)

address_list = []
plm_list = {}
plm_ref_list = {}
plm_intro_list = {}
refrenced_bonus = {}
introduce_bonus = {}

for tx in txs['result']:
    hash = tx['hash']
    address = tx['from']
    if not hash in tx_issue_rate:
        continue
    issued_plm = TOTAL_LOCKDROP_PLM * tx_issue_rate[hash] // total_issue_ratio
    tx_issue_plm[hash] = issued_plm

    add_list_num(plm_list, address, issued_plm)

    introducer = tx_introducer[hash]
    if is_valid_intro(introducer):
        issued_aff_plm = issued_plm // 100
        add_list_num(plm_ref_list, introducer, issued_aff_plm)
        add_list_num(plm_intro_list, address, issued_aff_plm)        

# recover public keys
keys = { tx['from']:recover_transaction(tx['hash']) for tx in txs['result'] }

for (address, plm) in plm_list.items():
    print(address, plm)
    print(address, keys[address])

# /1e-18 because of wei.
print('total/total', TOTAL_LOCKDROP_PLM * WEI, total_issue_ratio * FEMTO);
alpha_1 = (TOTAL_LOCKDROP_PLM * WEI) / (total_issue_ratio * FEMTO)
# /(WEI/FEMTO)
print('alpha_1', alpha_1)
alpha_2 = alpha_1 * 5 / 6
alpha_3 = alpha_1 * 4 / 6

print('alpha_2', alpha_2)
print('alpha_3', alpha_3)

with open('data/alpha.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['alpha', 'float value', 'numerator', 'denominator'])
    writer.writerow(['alpha_1', alpha_1, TOTAL_LOCKDROP_PLM * WEI, total_issue_ratio * FEMTO])
    writer.writerow(['alpha_2', alpha_2, TOTAL_LOCKDROP_PLM * WEI * 5, total_issue_ratio * FEMTO * 6])
    writer.writerow(['alpha_3', alpha_3, TOTAL_LOCKDROP_PLM * WEI * 4, total_issue_ratio * FEMTO * 6])
    writer.writerow(['ETH valua at May 1', eth_exchange_rate/eth_exchange_rate_div, eth_exchange_rate, eth_exchange_rate_div])

with open('data/out.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['address', 'lock return', 'ref_bonnus', 'intro_bonnus', 'total return'])
    for (address, plm) in plm_list.items():
        all_plm = plm + get_or(plm_ref_list, address) + get_or(plm_intro_list, address)
        print([address, plm, get_or(plm_ref_list, address), get_or(plm_intro_list, address), all_plm])
        writer.writerow([address, bg_str(plm), get_or_str(plm_ref_list, address), get_or_str(plm_intro_list, address), bg_str(all_plm)])
print(type(TOTAL_LOCKDROP_PLM))

with open('data/holders.csv', 'w') as f:
    writer = csv.writer(f)
    for (address, plm) in plm_list.items():
        all_plm = plm + get_or(plm_ref_list, address) + get_or(plm_intro_list, address)
        writer.writerow([keys[address], bg_str(all_plm)])
