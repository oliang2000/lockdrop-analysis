import requests
import eth_keys
from hexbytes import HexBytes
from eth_utils import to_int
from utils.transactions import Transaction, vrs_from, hexstr_if_str, TRANSACTION_VALID_VALUES
from utils.signing import hash_of_signed_transaction, to_standard_signature_bytes, to_standard_v

INFURA_KEY='96a78ea1923d41cb837b07476c42b744'
INFURA_URI='https://mainnet.infura.io/v3/'+INFURA_KEY

def fetch_transaction(tx_hash):
    headers = {"content-type": "application/json"}
    req = { 'id': 1, 'jsonrpc': "2.0", 'method': 'eth_getTransactionByHash', 'params': [tx_hash] }
    r = requests.post(INFURA_URI, headers=headers, json=req)
    tx = r.json()['result']
    
    if not tx['to']:
        return None

    signed_tx = { 
        'nonce': int(tx['nonce'][2:], 16), 
        'gasPrice': int(tx['gasPrice'][2:], 16), 
        'gas': int(tx['gas'][2:], 16), 
        'to': HexBytes(tx['to'][2:]), 
        'value': int(tx['value'][2:], 16), 
        'data': HexBytes(tx['input'][2:]),
        'v': int(tx['v'][2:], 16),
        'r': int(tx['r'][2:], 16),
        's': int(tx['s'][2:], 16),} 
    return Transaction.from_dict(signed_tx)

def recover_transaction(tx_hash):
    txn = fetch_transaction(tx_hash)
    if not txn:
        return ''

    v, r, s = vrs_from(txn)
    hash_bytes = HexBytes(hash_of_signed_transaction(txn))
    if len(hash_bytes) != 32:
        raise ValueError("The message hash must be exactly 32-bytes")
    v_standard = to_standard_v(v)
    signature_obj = eth_keys.keys.Signature(vrs=(v_standard, r, s))
    return signature_obj.recover_public_key_from_msg_hash(hash_bytes)
