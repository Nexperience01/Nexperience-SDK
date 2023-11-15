from algosdk.v2client import algod

# Replace with the appropriate node address and port
algod_address = "http://localhost"
algod_port = 4001

# Initialize the AlgodClient
algod_token = ""
algod_client = algod.AlgodClient(algod_token, algod_address, algod_port)
