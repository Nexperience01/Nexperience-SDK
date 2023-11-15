from algosdk.v2client import indexer

# Initialize an Indexer client
indexer_address = "<YOUR_INDEXER_API_ENDPOINT>"
indexer_token = "<YOUR_INDEXER_API_TOKEN>"
indexer_client = indexer.IndexerClient(indexer_token, indexer_address)

# Wait for the previous transaction to be confirmed (you can implement a waiting mechanism)
confirmed_tx_info = None
while not confirmed_tx_info:
    try:
        confirmed_tx_info = algod_client.pending_transaction_info(tx_id)
    except Exception:
        pass

# Get the smart contract address from the confirmed transaction
contract_address = confirmed_tx_info["txn"]["txn"]["apid"]

# Create an Application Call transaction to call the 'on_create_campaign' function
app_call_txn = transaction.ApplicationCallTxn(
    sender_address,
    confirmed_tx_info["confirmed-round"],
    contract_address,
    0,  # The index of the function you want to call (0 for 'on_create_campaign')
    [],  # Arguments for the function (if any)
)

# Sign the application call transaction
signed_app_call_txn = app_call_txn.sign(mnemonic.from_private_key("<YOUR_PRIVATE_KEY>"))

# Send the application call transaction
app_call_tx_id = algod_client.send_transaction(signed_app_call_txn)
print(f"Campaign creation transaction ID: {app_call_tx_id}")
