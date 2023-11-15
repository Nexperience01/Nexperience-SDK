from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk import transaction
import json
import base64

# Your Algorand node information
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""  # Replace with your Algod API token

# Load your account using a mnemonic
mnemonic_phrase = "only intact exhaust subject empower peanut cube island reform congress vanish wet design rhythm resource blade shop liquid oyster midnight swarm accident winter above quick"
sender_private_key = "2GTdnn6NpIeuZnaixYvime8d4/IWFzWW4DzHuO0FgJ8fhsQ0vZuSDP2BE0220yUL5mL7yHPZr7fS2jbXxJMSyw=="
sender_address = account.address_from_private_key(sender_private_key)

# Initialize an Algod client
algod_client = algod.AlgodClient(algod_token, algod_address)

# Read and compile the TEAL program
teal_program_path = "./approval2.teal"
with open(teal_program_path, "r") as f:
    teal_program_source = f.read()

compiled_program = algod_client.compile(teal_program_source)
program_bytes = base64.b64decode(compiled_program['result'])

# Define global and local state schemas
# Adjust these values as per your contract's requirements
global_schema = transaction.StateSchema(num_uints=1, num_byte_slices=0)
local_schema = transaction.StateSchema(num_uints=0, num_byte_slices=0)

# Get suggested transaction parameters
params = algod_client.suggested_params()

# Create an application transaction
app_txn = transaction.ApplicationCreateTxn(
    sender=sender_address,
    sp=params,
    on_complete=transaction.OnComplete.NoOpOC,
    approval_program=program_bytes,
    clear_program=program_bytes,  # Assuming same program for both approval and clear
    global_schema=global_schema,
    local_schema=local_schema,
    extra_pages=0  # Adjust if your contract requires more TEAL bytecode space
)

# Sign the transaction
signed_txn = app_txn.sign(sender_private_key)

# Send the transaction
tx_id = algod_client.send_transaction(signed_txn)
print(f"Contract deployed with transaction ID: {tx_id}")

# Helper function to wait for a transaction to be confirmed (as per your earlier script)
def wait_for_confirmation(client, txid, timeout):
     
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
            raise Exception('Error in transaction pool: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)
        current_round += 1
    raise Exception('Transaction {} not confirmed after {} rounds'.format(txid, timeout))

# Wait for the transaction to be confirmed
confirmed_txn = wait_for_confirmation(algod_client, tx_id, 4)  
print("TXID:", tx_id)
print("Result confirmed in round:", confirmed_txn['confirmed-round'])
