from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk import transaction

import base64

# Algorand node information and client initialization
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""  # Replace with your Algod API token
algod_client = algod.AlgodClient(algod_token, algod_address)

# Your account (same as used for deployment)
mnemonic_phrase = "only intact exhaust subject empower peanut cube island reform congress vanish wet design rhythm resource blade shop liquid oyster midnight swarm accident winter above quick"
sender_private_key = mnemonic.to_private_key(mnemonic_phrase)
sender_address = account.address_from_private_key(sender_private_key)

# Your smart contract's application ID
app_id = '479654706'  # Replace with your app's ID

def wait_for_confirmation(client, txid, timeout):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(txid)
        except Exception:
            return None
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn.get("pool-error"):
            raise Exception('Error in pool: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)
        current_round += 1
    raise Exception('Transaction {} not confirmed after {} rounds'.format(txid, timeout))

def opt_in_to_app(client, sender_address, sender_private_key, app_id):
    params = client.suggested_params()
    txn = transaction.ApplicationOptInTxn(sender_address, params, app_id)

    signed_txn = txn.sign(sender_private_key)
    tx_id = client.send_transaction(signed_txn)
    print(f"Opt-in Transaction ID: {tx_id}")

    confirmed_txn = wait_for_confirmation(client, tx_id, 4)
    print(f"Opt-in confirmed in round: {confirmed_txn['confirmed-round']}")


# Function to call a contract method
def call_contract_function(function_name, args):
    print(f"Preparing to call function: {function_name} with arguments: {args}")
    params = algod_client.suggested_params()
    note = f"Calling {function_name}".encode()

    app_args = [function_name.encode()] + [arg.encode() for arg in args]

    txn = transaction.ApplicationCallTxn(
        sender=sender_address,
        sp=params,
        index=app_id,
         on_complete=transaction.OnComplete.NoOpOC,
        app_args=app_args,
        note=note
    )

    signed_txn = txn.sign(sender_private_key)
    tx_id = algod_client.send_transaction(signed_txn)
    print(f"Transaction ID: {tx_id}")

    # Wait for confirmation (using the wait_for_confirmation function from your deployment script)
    confirmed_txn = wait_for_confirmation(algod_client, tx_id, 4)
    print(f"Called {function_name}, confirmed in round: {confirmed_txn['confirmed-round']}")


# Opt-in to the app
opt_in_to_app(algod_client, sender_address, sender_private_key, app_id)
# Example calls (for demonstration purposes only)
# In a real application, uncomment and use these as needed based on your application logic

# Example calls (for demonstration purposes only)
# Uncomment and use these as needed based on your application logic

# To create a new campaign:
# Arguments: Owner's Address (str), Campaign ID (int)
call_contract_function("create_campaign", [sender_address, 11])


# To update an existing campaign:
# Arguments: New Owner's Address (str), Campaign ID (int)
# call_contract_function("update_campaign", ["<new_owner_address>", "<campaign_id>"])

# To cancel a campaign:
# Arguments: Campaign ID (int)
# call_contract_function("cancel_campaign", ["<campaign_id>"])

# To upload creative to a campaign:
# Arguments: Creative Data (str), Campaign ID (int)
# call_contract_function("upload_creative", ["<creative_data>", "<campaign_id>"])


