---
cover: ../.gitbook/assets/NEXperience Pitch Deck (4) (1).png
coverY: 129.2580287929125
---

# 📎 Smart Contracts

<details>

<summary>Advertiser Account Management Contract</summary>

* Functions: registerAdvertiser, updateAdvertiser, deactivateAdvertiser
* Data Structures: Local state for each advertiser with details
* Logic: Registration, updating, and deactivation of advertiser accounts
* API Endpoints: POST /advertisers, PUT /advertisers/{advertiserId}, DELETE /advertisers/{advertiserId}
* Interactions: Advertisers interact with this contract to manage their accounts on the NEXperience platform.

Contract deployed with transaction ID: QVLCGPZIZHUOU6LI3FAZ6QTFR53MSJN46XYTIV2HXCUEPJVUSDHQ TXID: QVLCGPZIZHUOU6LI3FAZ6QTFR53MSJN46XYTIV2HXCUEPJVUSDHQ Result confirmed in the round: 34598075&#x20;

[Testnet Link](https://testnet.algoexplorer.io/tx/QVLCGPZIZHUOU6LI3FAZ6QTFR53MSJN46XYTIV2HXCUEPJVUSDHQ)

</details>

<details>

<summary>Ad Delivery Contract</summary>

* Functions: deliverAd, recordImpression, recordClick
* Data Structures: Global state mapping for ad delivery details
* Logic: Recording and tracking of ad deliveries, impressions, and clicks
* API Endpoints: POST /ads/deliver, POST /ads/{adId}/impressions, POST /ads/{adId}/clicks
* Interactions: The contract interacts with the ad-matching engine to deliver targeted ads

Contract deployed with transaction ID: 3ROW7JDNUPAWYQX25PBF6UZ4D6F4FRXKNUZZHQY7UEGG5SSNBBTQ TXID: 3ROW7JDNUPAWYQX25PBF6UZ4D6F4FRXKNUZZHQY7UEGG5SSNBBTQ Result confirmed in the round: 34601780

[Testnet Link](https://testnet.algoexplorer.io/tx/3ROW7JDNUPAWYQX25PBF6UZ4D6F4FRXKNUZZHQY7UEGG5SSNBBTQ)

</details>

<details>

<summary>Campaign Management Contract</summary>

* Functions: createcampaign, updatecampaign, cancelCampaign, uploadAdCreative
* Data Structures: Global state counter for campaigns; Global state mapping for campaign details
* Logic: Creation, updating, cancellation, and management of ad campaigns
* API Endpoints: POST /campaigns, PUT /campaigns/{campaignId}, DELETE /campaigns/{campaignId}, POST /campaigns/{campaignId}/creative
* Interactions: Advertisers interact with this contract to manage their ad campaigns

Contract deployed with transaction ID: CXLJPOSCYEDHQB73L2OPA6JSLLHIVVYCBYBSSZD4FGHGNE63YIHQ TXID: CXLJPOSCYEDHQB73L2OPA6JSLLHIVVYCBYBSSZD4FGHGNE63YIHQ Result confirmed in the round: 34594511 App Id: 479654706&#x20;

[Testnet Link](https://testnet.algoexplorer.io/tx/CXLJPOSCYEDHQB73L2OPA6JSLLHIVVYCBYBSSZD4FGHGNE63YIHQ)

</details>

<details>

<summary>Ad Slot and Category Management Contract</summary>

* Functions: createAdSlot, updateAdSlot, removeAdSlot, createCategory, update Category, remove Category
* Data Structures: Global state counters for ad slots and categories; Global state mappings for ad slot and category details
* Logic: Creation, updating, and removal of ad slots and categories; Maintenance of unique identifiers for each ad slot and category
* API Endpoints: POST /ad-slots, PUT /ad-slots/{slotId}, DELETE /ad-slots/{slotId}, POST /categories, PUT /categories/{categoryId}, DELETE /categories/{categoryId}
* Interactions: DApp owners interact with this contract to manage ad slots and categories within their applications

Contract deployed with transaction ID: 5JPKNAQDJ2NAPPK65UI3YGD5UL7EJZTVT2TQOUZACW4574MC2XAA TXID: 5JPKNAQDJ2NAPPK65UI3YGD5UL7EJZTVT2TQOUZACW4574MC2XAA Result confirmed in the round: 34598321

[Testnet Link](https://testnet.algoexplorer.io/tx/5JPKNAQDJ2NAPPK65UI3YGD5UL7EJZTVT2TQOUZACW4574MC2XAA)

</details>

<details>

<summary>Ad Slot Auction Contract</summary>

* Functions: startAuction, placeBid, endAuction
* Data Structures: Global state mapping for auction details
* Logic: Management of the auction process for ad slots
* API Endpoints: POST /auctions/{slotId}, POST /auctions/{slotId}/bids, POST /auctions/{slotId}/end
* Interactions: Advertisers interact with this contract to bid on ad slots

Contract deployed with transaction ID: VFXSU2ADKJVOJFQEYUGE2MUVWPECKRYXITVNKAAPQGD6CTIYIQUA TXID: VFXSU2ADKJVOJFQEYUGE2MUVWPECKRYXITVNKAAPQGD6CTIYIQUA Result confirmed in the round: 34598986&#x20;

[Testnet Link](https://testnet.algoexplorer.io/tx/VFXSU2ADKJVOJFQEYUGE2MUVWPECKRYXITVNKAAPQGD6CTIYIQUA)

</details>

<details>

<summary>Token Transfer and Reward Mechanism Contract</summary>

* Functions: transferTokens, allocateRewards, claimReward
* Data Structures: Local state for each account with reward balances
* Logic: Transfer of tokens for payments and rewards; Allocation and claiming of rewards
* API Endpoints: POST /tokens/transfer, POST /rewards/allocate, POST /rewards/claim
* Interactions: Users, DApp owners, and advertisers interact with this contract for token-related transactions

Contract deployed with transaction ID: ZY5BUCJXE5UKPO4HG4K7HHCPBCU2HMK6OVO6BR5IRRQ7XLMYTD4Q TXID: ZY5BUCJXE5UKPO4HG4K7HHCPBCU2HMK6OVO6BR5IRRQ7XLMYTD4Q Result confirmed in the round: 34601344&#x20;

[Testnet Link](https://testnet.algoexplorer.io/tx/ZY5BUCJXE5UKPO4HG4K7HHCPBCU2HMK6OVO6BR5IRRQ7XLMYTD4Q)

</details>

<details>

<summary>User Data Privacy and Verification Contract</summary>

* Functions: submitPreferences, updateConsent, verifyData
* Data Structures: Local state for each user with preferences and consent status
* Logic: Submission and updating of user preferences; Verification of user data privacy using Zero-Knowledge Proofs
* API Endpoints: POST /users/{userId}/preferences, POST /users/{userId}/consent, POST /verify-data
* Interactions: Users interact with this contract to manage their preferences and consent; The contract interacts with off-chain ZKP services for data verification

Contract deployed with transaction ID: OEQ6OWCX4UVNS32RACVHCQIUVTY3AUXB7YUJKW5MBXC7VYHSHY6A TXID: OEQ6OWCX4UVNS32RACVHCQIUVTY3AUXB7YUJKW5MBXC7VYHSHY6A Result confirmed in the round: 34599355

[Testnet Link](https://testnet.algoexplorer.io/tx/OEQ6OWCX4UVNS32RACVHCQIUVTY3AUXB7YUJKW5MBXC7VYHSHY6A)

</details>

<details>

<summary>Ad Display Logic Contract</summary>

Functions: createDisplayRule, updateDisplayRule, removeDisplayRule, evaluateDisplayRules

* Data Structures: Global state mapping for display rules
* Logic: Creation, updating, and removal of display rules; Evaluation of display rules based on user preferences and ad data
* API Endpoints: POST /display-rules, PUT /display-rules/{ruleId}, DELETE /display-rules/{ruleId}, GET /display-rules/evaluate
* Interactions: The contract interacts with user data to determine ad display logic

Contract deployed with transaction ID: OM7OEDDX62ZXAHUJEFJSNJSDKH25URS2ZHWLBQMAZN6CJNPCMM4A TXID: OM7OEDDX62ZXAHUJEFJSNJSDKH25URS2ZHWLBQMAZN6CJNPCMM4A Result confirmed in the round: 34603087&#x20;

[Testnet Link](https://testnet.algoexplorer.io/tx/OM7OEDDX62ZXAHUJEFJSNJSDKH25URS2ZHWLBQMAZN6CJNPCMM4A)

</details>
