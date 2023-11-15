import beaker
import pyteal as pt
from pyteal import *
from algokit_utils import Auction

app = beaker.Application("ad_slot_auction")

# Define the Ad Slot Auction Management contract
def ad_slot_auction_logic():
    # Define the contract's state storage
    on_initialization_state = pt.Seq([
        pt.App.localPut(pt.Int(0), pt.Bytes("auction_counter"), pt.Int(1)),
        pt.Return(pt.Int(1))
    ])

    on_create_auction = pt.Seq([
        # Check if the sender is an existing DApp owner
        pt.If(pt.Not(pt.App.localGet(pt.Int(0), pt.Bytes("dapp_owner", pt.App.sender())).hasValue())),
        pt.Then(
            pt.Return(pt.Int(0))  # Auction creation failed, DApp owner not found
        ),
        pt.Else(
            pt.Local.put(pt.Bytes("auction_id"), pt.App.localGet(pt.Int(0), pt.Bytes("auction_counter"))),
            pt.App.localPut(pt.Int(0), pt.Bytes("ad_auction", pt.App.sender(), pt.App.localGet(pt.Int(0), pt.Bytes("auction_id"))), pt.Bytes("active")),
            pt.App.localPut(pt.Int(0), pt.Bytes("auction_counter"), pt.Add(pt.App.localGet(pt.Int(0), pt.Bytes("auction_counter")), pt.Int(1))),
            pt.Return(pt.Int(1))  # Auction created successfully
        )
    ])

    on_start_auction = pt.Seq([
        pt.App.localPut(pt.Int(0), pt.Bytes("current_auction"), pt.App.localGet(pt.Int(0), pt.Bytes("auction_id"))),
        pt.Return(pt.Int(1))
    ])

    on_place_bid = pt.Seq([
        # Check if the auction is active
        pt.If(pt.Not(pt.App.localGet(pt.Int(0), pt.Bytes("ad_auction", pt.App.localGet(pt.Int(0), pt.Bytes("current_auction")))).hasValue())),
        pt.Then(
            pt.Return(pt.Int(0))  # Bid placement failed, auction not found or not active
        ),
        # Check if the bidder is the sender and sender has sufficient funds to place the bid
        pt.If(pt.Or(
            pt.Not(pt.App.localGet(pt.Int(0), pt.Bytes("bidder", pt.App.sender())).hasValue()),
            pt.App.localGet(pt.Int(0), pt.Bytes("balance", pt.App.sender())) < pt.App.localGet(pt.Int(0), pt.Bytes("bid_amount"))
        )),
        pt.Then(
            pt.Return(pt.Int(0))  # Bid placement failed, bidder not found or insufficient balance
        ),
        pt.Else(
            # Update the highest bid and bidder for the current auction
            pt.App.localPut(pt.Int(0), pt.Bytes("highest_bid", pt.App.localGet(pt.Int(0), pt.Bytes("current_auction"))), pt.App.localGet(pt.Int(0), pt.Bytes("bid_amount"))),
            pt.App.localPut(pt.Int(0), pt.Bytes("highest_bidder", pt.App.localGet(pt.Int(0), pt.Bytes("current_auction"))), pt.App.sender()),
            # Deduct the bid amount from the bidder's balance
            pt.App.localPut(pt.Int(0), pt.Bytes("balance", pt.App.sender()), pt.Sub(pt.App.localGet(pt.Int(0), pt.Bytes("balance", pt.App.sender())), pt.App.localGet(pt.Int(0), pt.Bytes("bid_amount"))))
        )
    ])

    # Define the contract's approval program
    program = pt.Cond(
        [pt.Txn.application_id() == pt.Int(0), on_initialization_state],
        [pt.Txn.application_id() == pt.Int(1), on_create_auction],
        [pt.Txn.application_id() == pt.Int(2), on_start_auction],
        [pt.Txn.application_id() == pt.Int(3), on_place_bid]
    )

    return program

# Define the contract's approval program and state storage


if __name__ == "__main__":
     app.build().export("./artifacts")