
from algosdk.v2client import algod, dryrun
from algosdk import transaction

# Algorand node information and client initialization
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""  # Replace with your Algod API token
algod_client = algod.AlgodClient(algod_token, algod_address)

# Your account (same as used for deployment)
sender_address = "D6DMINF5TOJAZ7MBCNG3NUZFBPTGF66IOPM27N6S3I3NPRETCLFUB33FTQ"  # Replace with your sender's address
sender_private_key = "2GTdnn6NpIeuZnaixYvime8d4/IWFzWW4DzHuO0FgJ8fhsQ0vZuSDP2BE0220yUL5mL7yHPZr7fS2jbXxJMSyw=="  # Replace with your sender's private key

# Your smart contract's application ID
app_id = 479654706  # Replace with your app's ID

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

# Define your compiled Teal code here
compiled_teal_code = b"""
#pragma version 5
txn ApplicationID
int 0
==
bnz main_l12
txn OnCompletion
int NoOp
==
bnz main_l3
err
main_l3:
txna ApplicationArgs 0
byte "create_campaign"
==
bnz main_l11
txna ApplicationArgs 0
byte "update_campaign"
==
bnz main_l10
txna ApplicationArgs 0
byte "cancel_campaign"
==
bnz main_l9
txna ApplicationArgs 0
byte "upload_creative"
==
bnz main_l8
err
main_l8:
txna ApplicationArgs 1
log
int 1
return
main_l9:
txn Sender
byte "campaign_owner"
byte ""
app_local_put
txn Sender
byte "campaign_id"
int 0
app_local_put
int 1
return
main_l10:
txn Sender
byte "campaign_owner"
txna ApplicationArgs 1
app_local_put
txn Sender
byte "campaign_id"
txna ApplicationArgs 2
btoi
app_local_put
int 1
return
main_l11:
byte "campaign_counter"
byte "campaign_counter"
app_global_get
int 1
+
app_global_put
txn Sender
byte "campaign_owner"
txna ApplicationArgs 1
app_local_put
txn Sender
byte "campaign_id"
txna ApplicationArgs 2
btoi
app_local_put
int 1
return
main_l12:
byte "campaign_counter"
int 0
app_global_put
int 1
return

"""

# Create a DryrunRequest to simulate the execution of the smart contract
source = dryrun.DryrunSource(
    round=algod_client.status()["last-round"],
    sources=[dryrun.DryrunSource.source.dryrun_source_transaction],
    txns=[dryrun.DryrunSource.txn(transaction=compiled_teal_code)],
)

request = dryrun.DryrunRequest(
    mode=dryrun.DryrunRequest.mode.application,
    app_id=app_id,
    src=source,
    accounts=[sender_address],
)

# Perform the dry run
dryrun_results = algod_client.dryrun(request)

# Display dry run results
print("Dry Run Results:")
print(dryrun_results)

# Optionally, you can access detailed information about the dry run results as needed
# For example, to access global state changes:
# global_state_changes = dryrun_results["dryrun-delta"]["global-state-delta"]
# For local state changes, you can iterate through accounts in accounts_delta

# Example calls (for demonstration purposes only)
# Uncomment and use these as needed based on your application logic

# To create a new campaign:
# Arguments: Owner's Address (str), Campaign ID (int)
# call_contract_function("create_campaign", [sender_address, 11])

# To update an existing campaign:
# Arguments: New Owner's Address (str), Campaign ID (int)
# call_contract_function("update_campaign", ["<new_owner_address>", "<campaign_id>"])

# To cancel a campaign:
# Arguments: Campaign ID (int)
# call_contract_function("cancel_campaign", ["<campaign_id>"])

# To upload creative to a campaign:
# Arguments: Creative Data (str), Campaign ID (int)
# call_contract_function("upload_creative", ["<creative_data>", "<campaign_id>"])
