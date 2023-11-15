from pyteal import *

def ad_slot_management_logic():
    # Define state keys
    slot_counter_key = Bytes("slot_counter")
    dapp_owner_key = lambda sender: Concat(Bytes("dapp_owner_"), sender)
    ad_slot_key = lambda owner, slot_id: Concat(Bytes("ad_slot_"), owner, Bytes("_"), Itob(slot_id))

    # OnCreate Logic
    on_create = Seq([
        App.globalPut(slot_counter_key, Int(1)),
        Return(Int(1))
    ])

    # OnCall Logic - Create Ad Slot
    on_create_ad_slot = Seq([
        # Check if the sender is an existing DApp owner
        If(
            App.globalGet(dapp_owner_key(Txn.sender())) == Bytes(""),
            Return(Int(0)),  # Ad slot creation failed, DApp owner not found
            Seq([
                # Increment the slot counter
                App.globalPut(slot_counter_key, App.globalGet(slot_counter_key) + Int(1)),

                # Store the new ad slot's data
                App.globalPut(ad_slot_key(Txn.sender(), App.globalGet(slot_counter_key)), Bytes("active")),
                Return(Int(1))  # Ad slot created successfully
            ])
        )
    ])

    # Approval Program Logic
    program = Cond(
        [Txn.application_id() == Int(0), on_create],  # On contract creation
        [Txn.on_completion() == OnComplete.NoOp, on_create_ad_slot]  # On standard call
    )

    return program

def clear_state_program():
    return Return(Int(1))

# Compile the contract
if __name__ == "__main__":
    approval_teal = compileTeal(ad_slot_management_logic(), mode=Mode.Application, version=5)
    clear_teal = compileTeal(clear_state_program(), mode=Mode.Application, version=5)

    with open("approval.teal", "w") as f:
        f.write(approval_teal)

    with open("clear.teal", "w") as f:
        f.write(clear_teal)
