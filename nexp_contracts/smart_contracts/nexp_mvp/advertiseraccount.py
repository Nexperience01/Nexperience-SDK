import beaker
import pyteal as pt
from pyteal import *

app = beaker.Application("advertiser_account")

# Define the Advertiser Account Management contract
def advertiser_account_logic():
    # Define the contract's state storage
    on_initialization_state = pt.Seq([
        pt.App.localPut(pt.Int(0), pt.Bytes("account_counter"), pt.Int(1)),
        pt.Return(pt.Int(1))
    ])

    on_create_account = pt.Seq([
        # Check if the sender is not an existing advertiser
        pt.If(pt.App.localGet(pt.Int(0), pt.Bytes("advertiser", pt.App.sender())).hasValue()),
        pt.Then(
            pt.Return(pt.Int(0))  # Account creation failed, advertiser already exists
        ),
        pt.Else(
            pt.Local.put(pt.Bytes("account_id"), pt.App.localGet(pt.Int(0), pt.Bytes("account_counter"))),
            pt.App.localPut(pt.Int(0), pt.Bytes("advertiser", pt.App.sender()), pt.Bytes("active")),
            pt.App.localPut(pt.Int(0), pt.Bytes("account_counter"), pt.Add(pt.App.localGet(pt.Int(0), pt.Bytes("account_counter")), pt.Int(1))),
            pt.Return(pt.Int(1))  # Account created successfully
        )
    ])

    # Define the contract's approval program
    program = pt.Cond(
        [pt.Txn.application_id() == pt.Int(0), on_initialization_state],
        [pt.Txn.application_id() == pt.Int(1), on_create_account]
    )

    return program

# Define the contract's approval program and state storage


if __name__ == "__main__":
     app.build().export("./artifacts")