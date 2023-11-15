from pyteal import *

global_campaign_counter = Bytes("campaign_counter")
local_campaign_owner = Bytes("campaign_owner")
local_campaign_id = Bytes("campaign_id")

def ad_campaign_contract():
    # OnCreate Logic
    on_create = Seq([
        App.localPut(Int(0), local_campaign_owner, Int(0)),
        App.localPut(Int(0), local_campaign_id, Int(0)),
        App.localPut(Int(0), global_campaign_counter, Int(0)),
        Return(Int(1))
    ])

    # OnCall Logic
    handle_noop = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.application_args[0] == Bytes("create_campaign"), create_campaign()],
        [Txn.application_args[0] == Bytes("update_campaign"), update_campaign()],
        [Txn.application_args[0] == Bytes("cancel_campaign"), cancel_campaign()],
        [Txn.application_args[0] == Bytes("upload_creative"), upload_creative()]
    )

    return handle_noop

# External Methods
def create_campaign():
    # Assuming the second and third arguments are the owner's address and campaign ID, respectively
    owner = Txn.application_args[1]
    campaign_id = Btoi(Txn.application_args[2])

    return Seq([
        App.localPut(Int(0), global_campaign_counter, App.localGet(Int(0), global_campaign_counter) + Int(1)),
        App.localPut(Txn.application_id(), local_campaign_owner, owner),
        App.localPut(Txn.application_id(), local_campaign_id, campaign_id),
        Return(Int(1))
    ])

def update_campaign():
    # Similar to create_campaign, but updates existing entries
    new_owner = Txn.application_args[1]
    new_campaign_id = Btoi(Txn.application_args[2])

    return Seq([
        App.localPut(Txn.application_id(), local_campaign_owner, new_owner),
        App.localPut(Txn.application_id(), local_campaign_id, new_campaign_id),
        Return(Int(1))
    ])

def cancel_campaign():
    # Logic to reset the campaign details for the sender
    return Seq([
        App.localPut(Txn.application_id(), local_campaign_owner, Int(0)),
        App.localPut(Txn.application_id(), local_campaign_id, Int(0)),
        Return(Int(1))
    ])

def upload_creative():
    # This function can be customized based on how you want to handle creative uploads.
    # For now, it just logs that an upload was attempted.
    creative_data = Txn.application_args[1]  # Placeholder for creative data
    return Seq([
        Log(creative_data),
        Return(Int(1))
    ])

if __name__ == "__main__":
    compiled_teal = compileTeal(ad_campaign_contract(), mode=Mode.Application, version=5)
    print(compiled_teal)
