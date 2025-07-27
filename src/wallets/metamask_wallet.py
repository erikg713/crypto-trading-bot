# Placeholder for metamask wallet interaction

from web3 import Web3
import os

INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("METAMASK_PRIVATE_KEY")
ADDRESS = os.getenv("METAMASK_ADDRESS")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def send_eth_transaction(to_address, amount_eth):
    nonce = w3.eth.get_transaction_count(ADDRESS)
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': w3.to_wei(amount_eth, 'ether'),
        'gas': 21000,
        'gasPrice': w3.to_wei('40', 'gwei')
    }
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()

def get_balance():
    print("Metamask wallet balance fetched (stub)")
    return 0.0

def sign_transaction(tx):
    print("Metamask transaction signed (stub)")
    return None

