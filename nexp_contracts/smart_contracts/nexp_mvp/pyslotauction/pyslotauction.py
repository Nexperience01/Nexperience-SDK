from pyteal import *

def ad_slot_auction_logic():
    # Define state keys
    auction_counter_key = Bytes("auction_counter")
    dapp_owner_key = lambda sender: Concat(Bytes("dapp_owner_"), sender)
    ad_auction_key = lambda owner, auction_id: Concat(Bytes("ad_auction_"), owner, Bytes("_"), Itob(auction_id))
    highest_bid_key = lambda auction_id: Concat(Bytes("highest_bid_"), Itob(auction_id))
    highest_bidder_key = lambda auction_id: Concat(Bytes("highest_bidder_"), Itob(auction_id))
    balance_key = lambda account: Concat(Bytes("balance_"), account)

    # OnCreate Logic
    on_create = Seq([
        App.globalPut(auction_counter_key, Int(1)),
        Return(Int(1))
    ])

    # OnCall Logic - Create Auction
    on_create_auction = Seq([
        # Check if the sender is an existing DApp owner
        If(
            App.globalGet(dapp_owner_key(Txn.sender())) == Bytes(""),
            Return(Int(0)),  # Auction creation failed, DApp owner not found
            Seq([
                App.globalPut(auction_counter_key, App.globalGet(auction_counter_key) + Int(1)),
                App.globalPut(ad_auction_key(Txn.sender(), App.globalGet(auction_counter_key)), Bytes("active")),
                Return(Int(1))  # Auction created successfully
            ])
        )
    ])

    # OnCall Logic - Start Auction
    on_start_auction = Seq([
        App.globalPut(Bytes("current_auction"), App.globalGet(auction_counter_key)),
        Return(Int(1))
    ])

    # OnCall Logic - Place Bid
    on_place_bid = Seq([
        # Check if the auction is active
        If(
            App.globalGet(ad_auction_key(Txn.sender(), App.globalGet(Bytes("current_auction")))) != Bytes("active"),
            Return(Int(0)),  # Bid placement failed, auction not active
            Seq([
                # Check if the bidder has sufficient balance
                If(
                    App.globalGet(balance_key(Txn.sender())) < Txn.amount(),
                    Return(Int(0)),  # Bid placement failed, insufficient balance
                    Seq([
                        App.globalPut(highest_bid_key(App.globalGet(Bytes("current_auction"))), Txn.amount()),
                        App.globalPut(highest_bidder_key(App.globalGet(Bytes("current_auction"))), Txn.sender()),
                        # Optionally update bidder's balance here
                        Return(Int(1))  # Bid placed successfully
                    ])
                )
            ])
        )
    ])

    # Approval Program Logic
    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.NoOp, on_create_auction],
        [Txn.on_completion() == OnComplete.NoOp, on_start_auction],
        [Txn.on_completion() == OnComplete.NoOp, on_place_bid]
    )

    return program

def clear_state_program():
    return Return(Int(1))

# Compile the contract
if __name__ == "__main__":
    approval_teal = compileTeal(ad_slot_auction_logic(), mode=Mode.Application, version=5)
    clear_teal = compileTeal(clear_state_program(), mode=Mode.Application, version=5)

    with open("approval.teal", "w") as f:
        f.write(approval_teal)

    with open("clear.teal", "w") as f:
        f.write(clear_teal)
