from pyteal import *

def advertiser_account_logic():
    # Define state keys
    account_counter_key = Bytes("account_counter")
    advertiser_key_prefix = Bytes("advertiser_")

    # Function to create a key for each advertiser in the global state
    def advertiser_key(sender: Expr) -> Expr:
        return Concat(advertiser_key_prefix, sender)

    # OnCreate Logic
    on_create = Seq([
        App.globalPut(account_counter_key, Int(1)),
        Return(Int(1))
    ])

    # OnCall Logic - Create Account
    on_create_account = Seq([
        # Check if the sender is an existing advertiser
        If(
            App.globalGet(advertiser_key(Txn.sender())) == Bytes(""),  # Check if the key is not set
            Seq([
                # Increment the account counter
                App.globalPut(account_counter_key, App.globalGet(account_counter_key) + Int(1)),

                # Store the new advertiser's data
                App.globalPut(advertiser_key(Txn.sender()), Bytes("active")),
                Return(Int(1))  # Account created successfully
            ]),
            Return(Int(0))  # Account creation failed, advertiser already exists
        )
    ])

    # Approval Program Logic
    program = Cond(
        [Txn.application_id() == Int(0), on_create],  # On contract creation
        [Txn.on_completion() == OnComplete.NoOp, on_create_account]  # On standard call
    )

    return program

def clear_state_program():
    return Return(Int(1))

# Compile the contract
if __name__ == "__main__":
    approval_teal = compileTeal(advertiser_account_logic(), mode=Mode.Application, version=5)
    clear_teal = compileTeal(clear_state_program(), mode=Mode.Application, version=5)

    with open("approval.teal", "w") as f:
        f.write(approval_teal)

    with open("clear.teal", "w") as f:
        f.write(clear_teal)
