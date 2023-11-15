import beaker
import pyteal as pt
from pyteal import *

app = beaker.Application("ad_slot_management")

# Define the Ad Slot Management contract
def ad_slot_management_logic():
    # Define the contract's state storage
    on_initialization_state = pt.Seq([
        pt.App.localPut(pt.Int(0), pt.Bytes("slot_counter"), pt.Int(1)),
        pt.Return(pt.Int(1))
    ])

    on_create_ad_slot = pt.Seq([
        # Check if the sender is an existing DApp owner
        pt.If(pt.Not(pt.App.localGet(pt.Int(0), pt.Bytes("dapp_owner", pt.App.sender())).hasValue())),
        pt.Then(
            pt.Return(pt.Int(0))  # Ad slot creation failed, DApp owner not found
        ),
        pt.Else(
            pt.Local.put(pt.Bytes("slot_id"), pt.App.localGet(pt.Int(0), pt.Bytes("slot_counter"))),
            pt.App.localPut(pt.Int(0), pt.Bytes("ad_slot", pt.App.sender(), pt.App.localGet(pt.Int(0), pt.Bytes("slot_id"))), pt.Bytes("active")),
            pt.App.localPut(pt.Int(0), pt.Bytes("slot_counter"), pt.Add(pt.App.localGet(pt.Int(0), pt.Bytes("slot_counter")), pt.Int(1))),
            pt.Return(pt.Int(1))  # Ad slot created successfully
        )
    ])

    # Define the contract's approval program
    program = pt.Cond(
        [pt.Txn.application_id() == pt.Int(0), on_initialization_state],
        [pt.Txn.application_id() == pt.Int(1), on_create_ad_slot]
    )

    return program

# Define the contract's approval program and state storage


if __name__ == "__main__":
    app.build().export("./artifacts")