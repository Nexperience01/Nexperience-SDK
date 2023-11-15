from pyteal import *

def ad_display_logic():
    # Initialization of global state
    on_create = Seq([
        App.globalPut(Bytes("init"), Int(1)),  # Initialize a dummy global state
        Return(Int(1))
    ])

    # Logic for Ad Request (remains the same as your original logic)
    user_preferences_key = Bytes("user_preferences")
    preferences = ScratchVar(TealType.bytes)
    on_ad_request = Seq([
        preferences.store(App.localGet(Txn.sender(), user_preferences_key)),
        If(
            preferences.load() == Bytes("interested"),
            Return(Int(1)),
            Return(Int(0))
        )
    ])

    # Approval Program Logic
    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.NoOp, on_ad_request]
    )

    return program

def clear_state_program():
    return Return(Int(1))

# Compile the contract
if __name__ == "__main__":
    approval_teal = compileTeal(ad_display_logic(), mode=Mode.Application, version=5)
    clear_teal = compileTeal(clear_state_program(), mode=Mode.Application, version=5)

    with open("approval.teal", "w") as f:
        f.write(approval_teal)

    with open("clear.teal", "w") as f:
        f.write(clear_teal)
