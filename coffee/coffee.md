- In App Purchases
	- wordle is free
	- $20 for boggle & weekly crossword

- Deposits
	- new users get $2.50 when depositing at least $5
	- $5, $10, $20 give no bonuses
	- $50 gets $2.5, $100 gets
	{'amount': 5, 'bonus': 0, 'probability': 0.4},
	{'amount': 10, 'bonus': 0, 'probability': 0.3},
	{'amount': 20, 'bonus': 0, 'probability': 0.15},
	{'amount': 50, 'bonus': 1, 'probability': 0.05},
	{'amount': 100, 'bonus': 5, 'probability': 0.05},
	{'amount': 200, 'bonus': 15, 'probability': 0.05},
]

- use phone number to verify account. login via a code that is text.

- restrict to only food and drink places
- $20 limit / day but the charge can go to $25
- stripe has a built in daily limit and category limit functions

- in app chat is shockingly difficult
- start with a 4 digit code for initial sign ups to keep them private
- enable balance notifications

=================
- make it a website only right now
=================

SIGN UP/IN FLOW
- download and open the app
- enter phone number
- if it exists, then we send a verification to login
- if it doesn't exist, we ask for the secret code
- if they provide the code, then we send a verification to login

NEW USER FLOW
- after the first login, we ask for name
- we prompt to connect a card, but it is skippable

EXISTING USER FLOW
- after login, we see the balance page
- top is a bar with coffee rewards
- then balance in big letters
- then a pic of the card, the card can be added to apply pay here
- then a few recent transactions

DEPOSITING FLOW
- select deposit to show a popup
- the popup includes deposit options w/ rewards (radio buttons)
- the bottom has pay with card or apple pay button

PAYMENT FLOW
- user adds card like any other card
- user opens apple pay and pays with card
- automatic stripe limits ($20 and category)
- use real-time hook to keep from overdrafting
- no need to auto deposit right now, just cancel




To Build
- Login w Phone Number
- Depositing and Connecting Cards/Apple Pay
- Issue Digital CC and Add to Apple Pay
- Transaction Hook w Limit/Restriction

Data Structures
- User
	- phoneNumber
	- email
	- name
	- authToken
- UserPaymentMethod
	- type
	- stripeId
	- extras (type, last4, etc)
- UserBalance
	- coffeeCardNumber
	- stripeCardHolderId
	- settledAmount
	- unsettledAmount
- Deposits
	- amount
	- bonus
- Transaction
	- amount
	- details (name, etc)
- DeniedTransaction
	- amount
	- details (name, etc)