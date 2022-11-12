# Account ID information
Account id is generated at startup. 

	account id = (sha256(user id + last 4 digits SS))[0:8]



# User PII - in Key vault
All of these data points need to be collected during sign up:
- account id: see above
- user id (object id)
- user SS
- user dob
- user address
- mother's maiden name

# User table
- user id - index (idx)
- account id - calculated once at sign up
- status flags ==== SEE BELOW 
- fmv (calculated, updated nightly)
- number of shares (calculated, updated nightly)
- number of shares from inherited
- transfer amount (depending on flag)
- last update (time stamp)

- DP of the user (calculated once a year) (could come from a json file - static and will change yearly)



# Transaction table
- user id - index
- account id (account 00000000 is savvly)
- date/time
- type (Investment, dividends will be recorded as management fee, savvly fee, sign up fee)
- amount deposited/ deducted in case of management fees, etc
- number of shares
- price per share (maybe?!)

(ammount deposited and number of shares is needed for rebalancing.  Ammount deposited is the cost basis)

# Inherited table (virtual pool)
 (after someone dies, his/her shares are redistributed)
- from user id - index
- to user id - index
- from account id
- date/time
- number of shares (+/-)
- price per share - cost basis


# Status flags
there will be a state machine like status flag for each user

- Pending: just signed up. no KYC
- Active: idle.  Nothing pending.  nothing on hold
- Transfer: incoming $ pending
- Transfer_complete: $ transfer compelete (in our bank account)
- purchase_pending: buying shares from the money in bank account
- withdrawal: $ leaving
- withdrawal_pending: $ money in our bank account from a sell
- Deceased: dead
- Closed: no activity allowed
- Transfer_cancel: ?? (time out?)

# State changes
- pending -> Active: manual.  Kyc compeleted
- Active -> transfer: API call.  user wants to transfer money
 - transfer -> transfer_complete: bank adaptor checks
- transfer_complete -> purchase_pending: trade submission
- purchase_pending -> Active: trade submission
- Active -> withdrawal: API call
- withdrawal -> withdrawal_pending: trade submission
- withdrawal_pending -> active: bank adapter (?) missing step here
- Active -> deceased: death check. manual
- Deceased -> closed: rebalancer





# System checks
(integration testing)

current price = retrived every 'n' min from the market
fmv = (# of shares from transaction table + # of shares from inherited table) * current price



