from algosdk import transaction
from algosdk.v2client import algod
import json

# Your Algorand node information
algod_address = "https://testnet-api.algonode.cloud"
algod_token = ""  # Replace with your Algod API token

# Teal file paths
approval_program_path = "../artifacts/approval.teal"
clear_program_path = "../artifacts/clear.teal"

# Load your account using a mnemonic or provide a funded address
mnemonic_phrase = "only intact exhaust subject empower peanut cube island reform congress vanish wet design rhythm resource blade shop liquid oyster midnight swarm accident winter above quick"
sender_private_key = "2GTdnn6NpIeuZnaixYvime8d4/IWFzWW4DzHuO0FgJ8fhsQ0vZuSDP2BE0220yUL5mL7yHPZr7fS2jbXxJMSyw=="
sender_address = "D6DMINF5TOJAZ7MBCNG3NUZFBPTGF66IOPM27N6S3I3NPRETCLFUB33FTQ"

# Initialize an Algod client
algod_client = algod.AlgodClient(algod_token, algod_address)

# Read application parameters from application.json
with open("../artifacts/application.json", "r") as f:
    app_params = json.load(f)

# Compile approval program
with open(approval_program_path, "r") as f:
    approval_program_source = f.read()

compiled_approval_program = algod_client.compile(approval_program_source)
base64_encoded_approval_program = compiled_approval_program['result']

# Compile clear program
with open(clear_program_path, "r") as f:
    clear_program_source = f.read()

compiled_clear_program = algod_client.compile(clear_program_source)
base64_encoded_clear_program = compiled_clear_program['result']

# Get suggested transaction parameters
params = algod_client.suggested_params()

# Create global and local state schemas
global_schema = transaction.StateSchema(num_uints=app_params['state']['global']['num_uints'], num_byte_slices=0)
local_schema = transaction.StateSchema(num_uints=app_params['state']['local']['num_uints'], num_byte_slices=0)

# Create an application transaction
app_txn = transaction.ApplicationCreateTxn(
    sender_address,
    params,
    global_schema,
    local_schema,
    base64_encoded_approval_program,
    base64_encoded_clear_program,
    1000,  # The approval program must have at least 1,000 microAlgos in the sender's account
    1001,  # The clear program can have 1 microAlgo as a minimum balance
)

# Sign the transaction
signed_txn = app_txn.sign(sender_private_key)

# Send the transaction
tx_id = algod_client.send_transaction(signed_txn)
print(f"Contract deployed with transaction ID: {tx_id}")
