# Business Logic 


## Money Transfer
User requests money transfer in.  The request needs to be recorded in the database with a reference #

The reference # (or ID string) is used by the customer when wiring money

We check to the ID string to mark the status flag as transfer complete

## Transfer Deductions
There is "charge" for every transfer. This transfer cost (say $1.00) is deducted from the total $ transferred in

## Trades
Once transfer is completed, a trade is sumbmitted.  
What is recorded in the user accounting is the number of shares purchased.
The amount left over is left in the account (the custodian account)


## Dividends
This is a quarterly event.  The fund pays dividents

All dividents are transferred to Savvly


## Someone Dies
5% of the shares are liquidated, and money is transferred to Savvly

95% is distributed

### Distribution Logic
Goes into a separete pool for each person. 

The cost basis for original shares and the gain are treated the same BUT separately.  



## Someone exits - surrenderes

25% of the base cost is given back.  

5% of the shares are liquidated and money is transferred to Savvly

Rest is distributed









