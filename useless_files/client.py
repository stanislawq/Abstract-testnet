from web3 import Web3
import os
import sys
from Network import Network
from utils import read_json, TokenAmount
from typing import Optional
from pathlib import Path


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()



TOKEN_ABI = os.path.join("/abi1/erc20.json")


class Client:
    default_abi = read_json(TOKEN_ABI)
    contract_address = Web3.to_checksum_address('0x35A54c8C757806eB6820629bc82d90E056394C92')

    def __init__(self, private_key: str, network: Network):
        self.private_key = private_key
        self.network = network
        self.w3 = Web3(Web3.HTTPProvider(endpoint_uri=self.network.rpc_url))
        self.address = Web3.to_checksum_address(self.w3.eth.account.from_key(self.private_key).address)

    def get_symbol(self, token_address: str):
        return str(self.w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=Client.default_abi
        ).functions.symbol().call())

    def get_decimals(self, token_address: str) -> int:
        return int(self.w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=Client.default_abi
        ).functions.decimals().call())

    def get_balance(self, token_address: Optional[str] = None) -> int:
        if token_address:
            return int(self.w3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=Client.default_abi
            ).functions.balanceOf(self.address).call())
        return self.w3.eth.get_balance(self.address)

    def bridge_eth(self, chain, value):
        print(f'{self.address} | start bridge Abstract_ETH to Sepolia_ETH')
        value = TokenAmount(
            amount=value,
            decimals=18,
            wei=0
        )

        contract = self.w3.eth.contract(
            address=Client.contract_address,
            abi=Client.default_abi
        )
        data = contract.encode_abi("requestL2TransactionDirect", args=[(chain.chain_id, 500000000000000 + value.Wei, self.address, value.Wei, b'0x', 500000, 800, [], self.address)])
        return self.send_transaction(
            to=Client.contract_address,
            data=data,
            value=TokenAmount(amount=value.Wei + 500000000000000, decimals=18, wei=1)
        )

    def send_transaction(self, to, data=None, from_=None, value: Optional[TokenAmount] = None):
        if not from_:
            from_ = self.address

        tx_params = {
            'chainId': self.network.chain_id,
            'nonce': self.w3.eth.get_transaction_count(self.address),
            'from': Web3.to_checksum_address(from_),
            'to': Web3.to_checksum_address(to)
        }

        if data:
            tx_params['data'] = data

        last_block = self.w3.eth.get_block('latest')
        max_priority_fee_per_gas = self.w3.eth.max_priority_fee
        base_fee = int(last_block['baseFeePerGas'] * 1.125)
        max_fee_per_gas = base_fee + max_priority_fee_per_gas

        tx_params['maxPriorityFeePerGas'] = max_priority_fee_per_gas
        tx_params['maxFeePerGas'] = max_fee_per_gas

        if value:
            tx_params['value'] = value.Wei

        try:
            tx_params['gas'] = self.w3.eth.estimate_gas(tx_params)
        except Exception as err:
            print(f'{self.address} | unable to estimate gas | {err}')
            tx_params['gas'] = 240000
        signed_tx = self.w3.eth.account.sign_transaction(tx_params, self.private_key)
        return self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)


    def verify_tx(self, tx_hash) -> bool:
        if not tx_hash:
            return False
        try:
            if self.w3.eth.wait_for_transaction_receipt(tx_hash).status:
                print(f'{self.address} | transaction was submitted | {tx_hash.hex()}')
                return True
            else:
                print(f'{self.address} | transaction failed')
        except Exception as err:
            print(f'{self.address} | unexpected error | {err}')
        return False
