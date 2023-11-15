import pyteal as pt
import beaker

class AdCampaignState:
    # Define global state variables
    global_campaign_counter = beaker.GlobalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
        descr="Global counter for campaigns"
    )

    # Define local state variables
    local_campaign_owner = beaker.LocalStateValue(
        stack_type=pt.TealType.bytes,
        default=pt.Bytes(""),
        descr="Owner of the campaign"
    )
    local_campaign_id = beaker.LocalStateValue(
        stack_type=pt.TealType.uint64,
        default=pt.Int(0),
        descr="ID of the campaign"
    )

app = beaker.Application(
    "AdCampaign",
    state=AdCampaignState(),
)

@app.external
def create_campaign(
    owner: pt.abi.Address, 
    campaign_id: pt.abi.Uint64
) -> pt.Expr:
    return pt.Seq(
        app.state.global_campaign_counter.increment(),
        app.state.local_campaign_owner.set(owner.encode()),  # Convert Address to bytes
        app.state.local_campaign_id.set(campaign_id),
        pt.Return(pt.Int(1))
    )


@app.external
def update_campaign(
    new_owner: pt.abi.Address, 
    new_campaign_id: pt.abi.Uint64
) -> pt.Expr:
    return pt.Seq(
        app.state.local_campaign_owner.set(new_owner),
        app.state.local_campaign_id.set(new_campaign_id),
        pt.Return(pt.Int(1))
    )

@app.external
def cancel_campaign(campaign_id: pt.abi.Uint64) -> pt.Expr:
    # Simple logic to reset the owner and ID of a specific campaign
    return pt.Seq(
        pt.Assert(app.state.local_campaign_id == campaign_id),
        app.state.local_campaign_owner.set(pt.Bytes("")),
        app.state.local_campaign_id.set(pt.Int(0)),
        pt.Return(pt.Int(1))
    )

@app.external
def upload_creative(campaign_id: pt.abi.Uint64, creative_data: pt.abi.DynamicArray[pt.abi.Byte]) -> pt.Expr:
    # Example logic to handle creative data for a specific campaign
    return pt.Seq(
        pt.Assert(app.state.local_campaign_id == campaign_id),
        # Process the creative_data here as per your requirements
        # For now, just logging the creative data length
        pt.Log(pt.Itob(pt.Len(creative_data))),
        pt.Return(pt.Int(1))
    )

if __name__ == "__main__":
    # Instantiate and build the application
     ad_campaign_app = app.build()
     ad_campaign_app.export("./artifacts_campaign")
