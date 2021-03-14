from web3 import Web3, HTTPProvider
from solcx import compile_source


def compile_source_contract(contract_file_path):
    with open(contract_file_path, 'r') as f:
        source = f.read()

    compiled_sol = compile_source(source)
    contract_id, contract_interface = compiled_sol.popitem()
    return contract_interface


def get_contract(w3, contract_interface, address):
    return w3.eth.contract(address=address,
                           abi=contract_interface['abi'])


def deploy_contract(w3, contract_interface, from_account):
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'], bytecode=contract_interface['bin']).constructor().transact(
        {'from': from_account})

    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address


if __name__ == '__main__':
    blockchain_address = 'http://127.0.0.1:8545'
    w3 = Web3(HTTPProvider(blockchain_address))

    # compile contract
    contract_source_path = 'contracts/Prescription.sol'
    contract_interface = compile_source_contract(contract_source_path)

    # obtain address of deployed contract
    address = deploy_contract(w3, contract_interface, w3.eth.accounts[0])

    # interact with contract from blockchain
    print(get_contract(w3, contract_interface, address).functions.medicineName().call())

