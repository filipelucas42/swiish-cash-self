from web3 import Web3
from eth_account import Account
import secrets

# Connect to Avalanche C-Chain
rpc_url = "https://sepolia.drpc.org"
w3 = Web3(Web3.HTTPProvider(rpc_url))

def create_wallet():
    # Generate a private key
    private_key = "0x" + secrets.token_hex(32)
    
    # Create account from private key
    account = Account.from_key(private_key)
    print("address " + account.address)
    print("private " + private_key)
    
    return {
        "address": account.address,
        "private_key": private_key
    }

def get_balance(address: str) -> str:
    """
    Get ETH balance for an address
    Returns balance in ETH (not Wei)
    """
    try:
        # Get balance in Wei
        balance_wei = w3.eth.get_balance(address)
        # Convert Wei to ETH (18 decimals)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return balance_eth
    except Exception as e:
        print(f"Error getting balance: {e}")
        return 0

def estimate_gas_for_transfer(from_address: str, to_address: str, amount_avax: float):
    """
    Estimate gas needed to send ETH
    Returns estimated gas in wei
    """
    try:
        # Convert ETH amount to Wei
        amount_wei = w3.to_wei(amount_avax, 'ether')
        
        # Prepare transaction parameters
        tx_params = {
            'from': from_address,
            'to': to_address,
            'value': amount_wei,
            'nonce': w3.eth.get_transaction_count(from_address),
            'chainId': w3.eth.chain_id
        }
        
        # Estimate gas
        estimated_gas = w3.eth.estimate_gas(tx_params)
        
        # Get current gas price
        gas_price = w3.eth.gas_price
        
        # Calculate total cost in ETH
        total_cost_wei = estimated_gas * gas_price
        total_cost_avax = w3.from_wei(total_cost_wei, 'ether')
        
        return {
            'estimated_gas': estimated_gas,
            'gas_price_wei': gas_price,
            'total_cost_avax': total_cost_avax
        }
    except Exception as e:
        print(f"Error estimating gas: {e}")
        return None

def send_transaction(from_address: str, to_address: str, amount_avax: float, private_key: str):
    """
    Send ETH from one address to another
    """
    gas_for_transfer = estimate_gas_for_transfer(from_address, to_address, amount_avax)
    try:
        # Convert ETH amount to Wei
        amount_wei = w3.to_wei(amount_avax, 'ether')
        
        # Get the nonce
        nonce = w3.eth.get_transaction_count(from_address)
        
        # Prepare the transaction
        tx = {
            'nonce': nonce,
            'to': to_address,
            'value': amount_wei,
            'gas': int(gas_for_transfer['estimated_gas']*1.1),
            'gasPrice': w3.eth.gas_price,
            'chainId': w3.eth.chain_id
        }
        
        # Sign the transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        
        # Send the transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        return tx_hash
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None
def main():
    wallet = create_wallet()
    print(f"New Avalanche C-Chain Address: {wallet['address']}")
    print(f"Private Key: {wallet['private_key']}")
    
    # Verify connection
    print(f"Connected to Avalanche: {w3.is_connected()}")
    
if __name__ == "__main__":
    main()