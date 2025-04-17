class Network:
    def __init__(self,
                 name,
                 chain_id,
                 rpc_url,
                 explorer,
                 symbol,
                 decimals
                 ):
        self.name = name
        self.chain_id = chain_id
        self.rpc_url = rpc_url
        self.explorer = explorer
        self.symbol = symbol
        self.decimals = decimals


Sepolia = Network(
    name='Sepolia',
    chain_id=11155111,
    rpc_url='https://ethereum-sepolia-rpc.publicnode.com/',
    explorer='https://sepolia.etherscan.io/',
    symbol='ETH',
    decimals=18
)

Abstract = Network(
    name='Abstract',
    chain_id=11124,
    rpc_url='https://api.testnet.abs.xyz',
    explorer='https://explorer.testnet.abs.xyz/',
    symbol='ETH',
    decimals=18
)
