from pyteal import *

def ad_delivery_logic():
    # Define local state keys
    ad_slots_key = Bytes("ad_slots")

    # Declare ScratchVar
    ad_slot_info = ScratchVar(TealType.uint64)

    # OnCreate Logic
    on_create = Seq([
        App.globalPut(ad_slots_key, Int(0)),  # Initialize the global state for ad slots
        Return(Int(1))
    ])

    # OnCall Logic - Deliver Ad
    on_deliver_ad = Seq([
        ad_slot_info.store(App.globalGet(ad_slots_key)),
        
        # Check if the ad slot is available
        If(
            ad_slot_info.load() == Int(0),
            # Ad slot is available, proceed with delivery
            Seq([
                App.globalPut(ad_slots_key, Int(1)),  # Update ad slot status as occupied
                Return(Int(1))  # Ad delivered successfully
            ]),
            Return(Int(0))  # Ad delivery failed, slot not available
        )
    ])

    # Approval Program Logic
    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.NoOp, on_deliver_ad]
    )

    return program

def clear_state_program():
    return Return(Int(1))

# Compile the contract
if __name__ == "__main__":
    approval_teal = compileTeal(ad_delivery_logic(), mode=Mode.Application, version=5)
    clear_teal = compileTeal(clear_state_program(), mode=Mode.Application, version=5)

    with open("approval.teal", "w") as f:
        f.write(approval_teal)

    with open("clear.teal", "w") as f:
        f.write(clear_teal)
