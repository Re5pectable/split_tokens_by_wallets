import web3
from configparser import ConfigParser
import json

config = ConfigParser()
config.read('config.ini')

default_ABI = json.loads(open("default_abi.json", "r").read())

def read_wallets_from_txt(path: str = "wallets.txt", proportionally: bool = False) -> list: 
    w = []
    with open(path, "r") as f:
        lines = f.readlines()
    if proportionally:
        for line in lines:
            line = line.replace('\n',"")
            if " " in line:
                raise ValueError("Remove spaces from wallet lines")
            splitted = line.split("|")
            if splitted[1].isdigit():
                splitted[1] = int(splitted[1])
                if splitted[1] > 999 or splitted[1] < 0:
                    raise ValueError(f"Proportions must be from 1 to 999.")
                w.append({"wallet": splitted[0], "proportion": splitted[1]})
            else:
                raise ValueError(f"Unable to convert {splitted[1]} to digit. Please check this value.")
    else:
        for line in lines:
            line = line.replace('\n',"")
            if " " in line:
                raise ValueError("Remove spaces from wallet lines")
            if "|" in line:
                raise ValueError("If using without proportional, remove | and values.")
            w.append({"wallet": line, "proportion": 1.0})
    return w
    

def transfer_tokens(contract: str, amount: int, address: str) -> str:
    contract = network.toChecksumAddress(contract)
    contract = network.eth.contract(contract, abi=default_ABI)
    # print(contract.all_functions())
    txn = contract.functions.transfer(address, amount).buildTransaction(
        {'chainId': chain_id, 
        'gas': gas_limit, 
        'nonce': network.eth.get_transaction_count(root_wallet)})
    signed_txn = network.eth.account.signTransaction(txn, private_key=root_secret)
    txn_hash = network.eth.sendRawTransaction(signed_txn.rawTransaction)
    return txn_hash


if __name__  == '__main__':
    try:
        path_to_wallets = config['Params']['path_to_wallets']
        is_proportionally = bool(int(config['Params']['is_proportionally']))
        is_amount_in_decimals = bool(int(config['Params']['is_amount_in_gwei']))

        provider = config['Wallet']['HTTPprovider']
        chain_id = config['Wallet']['chain_id']
        root_wallet = config['Wallet']['wallet']
        root_secret = config['Wallet']['secret']
        gas_limit = int(config['Wallet']['gas_limit'])

        contract = config['Token_to_split']['contract']
        amount = float(config['Token_to_split']['amount'])  
        
    except:
        raise ValueError("Some of parameters are not valid. Note that bool arguments (such as is_proportionally) are set by 0 or 1.")

    network = web3.Web3(web3.Web3.HTTPProvider(provider))
    if network.isConnected():
        print(f"== Successfully connected to {provider}")
    else: 
        print(f"== Failed to connect to {provider}")
        quit()
    
    if not is_amount_in_decimals:
        amount = network.toWei(amount, 'ether')
    else:
        amount = int(amount)
    
    root_wallet = network.toChecksumAddress(root_wallet)
    wallets = read_wallets_from_txt(path=path_to_wallets, proportionally=is_proportionally)
    total_parts = 0
    for elem in wallets:
        total_parts += elem["proportion"]
    one_part = int(amount / total_parts)
    for wallet in wallets:
        txn = transfer_tokens(contract=contract, amount=one_part * wallet['proportion'], address=wallet['wallet'])
        print(f"== Send to {wallet['wallet']}\nHash: {txn}\nAmount: {str(one_part * wallet['proportion'])}\n")
    