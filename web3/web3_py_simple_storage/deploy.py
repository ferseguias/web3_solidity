from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile:
install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compalied_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Bytecode
# ABI

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/134027dbcc8b4ec6ac2a56e4a9a30c85")
)
chain_id = 4
my_address = "0x1C2bE776934c49c17aa4869b8d9408375F0194FE"
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Nonce
nonce = w3.eth.getTransactionCount(my_address)

# deploy:
# 1. create transaction to deploy contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# 2. sign transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. submit transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Waiting for transaction to finish..")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Deployed contract address: {tx_receipt.contractAddress}")

# work with deployed contracts:
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> simulate a call to get a number (no changes in blockchain, no gas paid)
print(simple_storage.functions.retrieve().call())

# Transact -> generate blockchain changes (gas fees to be paid)
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
print("Updating stored value")

tx_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(simple_storage.functions.retrieve().call())
