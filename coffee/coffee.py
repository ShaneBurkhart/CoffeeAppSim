#!/usr/bin/env python

import random
import pandas as pd
import matplotlib.pyplot as plt

import deposits as d
import spending 


# total deposits must grow faster than coffee expenses
# keeping a minimum for perks gives us time with that cash

# TWO BIG INDICATORS
# increase the amount of deposits
# decrease the spending of balances
# maximize the time with the cash 
# maximize average balance

YEARS_TO_SIMULATE =  2
DAYS_TO_SIMULATE = round(365 * YEARS_TO_SIMULATE)

FALLOUT_RATE = 0.1


# limit of 200 in account
# limit of 100 deposit a day
# limit of 20 dollar spend a day
# worst case is they are rewarded with 5 dollars a day for depositing 100 dollars 5 days
# 550 to spend for max reward, that is 27.5 days to spend that 500 of deposit
# if we watch for malicious users and at most they can spend in 27.5 days, then we can ban them easily
# stop them from taking the bonus to the extreme

# average 8 * 10 = 80 dollars a month

STARTING_CASH = 20000
AVAILABLE_CREDIT = 0

CREDIT_INTEREST_RATE = 0.10

ADDON_CONVERSION_RATE = 0

users = []
total_referrals = 0
credit_balance = AVAILABLE_CREDIT
cash_balance = STARTING_CASH
total_deposits = 0
total_bonus = 0
total_cc_fees = 0
total_marketing = 0
unused_funds = 0

history = []

interest_paid = 0

total_coffee_expenses = 0

new_users_yesterday = 0

total_addon_revenue = 0

for day in range(DAYS_TO_SIMULATE):
	last_history = history[-1] if history else None
	if last_history and cash_balance != 0:
		print(f'Day {day} of {DAYS_TO_SIMULATE}, users: {len(users)}, cash: {cash_balance}, profit: {last_history["unrealized profit"]:.2f} less marketing: {last_history["unrealized profit less marketing"]:.2f}, apr: { last_history["apr"] * 100:.2f}%, cost / cash: {last_history["cost of cash %"] * 100:.2f}, cost / user: {last_history["cost / user"]} ')



	deposits = 0
	bonus = 0
	deposit_cc_fees = 0
	spending_cc_fees = 0


	# recurring deposits
	recurring_deposits, reccuring_bonus, reccurring_cc_fees = d.recurring_deposits(day, users)
	deposits += recurring_deposits
	bonus += reccuring_bonus
	deposit_cc_fees += reccurring_cc_fees


	# new deposits
	new_deposits, new_bonus, new_users, new_referrals, marketing_installs, marketing_spend, cc_fees = d.new_user_deposits(day, users)
	deposits += new_deposits
	bonus += new_bonus
	deposit_cc_fees += cc_fees

	total_deposits += deposits

	total_marketing += marketing_spend
	if credit_balance > marketing_spend:
		credit_balance -= marketing_spend
	else:
		cash_balance -= marketing_spend


	# addons
	addon_revenue = new_users * 10 * 0.7 * ADDON_CONVERSION_RATE
	total_addon_revenue += addon_revenue
	cash_balance += addon_revenue

	# people spending money on coffee
	coffee_expenses, coffee_cc_fees = spending.coffee_spending(day, users)
	total_coffee_expenses += coffee_expenses
	spending_cc_fees += cc_fees

	credit_card_fees = deposit_cc_fees + spending_cc_fees


	# add deposits
	cash_balance += deposits


	# pay for stuff
	if credit_balance > coffee_expenses:
		credit_balance -= coffee_expenses
		credit_balance -= credit_card_fees
	else:
		cash_balance -= coffee_expenses
		cash_balance -= credit_card_fees

	total_cc_fees += credit_card_fees

	interest_cost = (AVAILABLE_CREDIT - credit_balance) * CREDIT_INTEREST_RATE / 365
	interest_paid += interest_cost


	# user churn
	fallout_num = round(len(users) * FALLOUT_RATE / 365)
	for i in range(fallout_num):
		index = random.randint(0, len(users) - 1)
		user = users.pop(index) if users[index]['balance'] < 10 else None


	# random stuff
	total_bonus += bonus
	total_referrals += new_referrals

	apr = 0
	if cash_balance and day and day > 365:
		apr = ((total_bonus + total_cc_fees) * 365 / day) / (cash_balance - STARTING_CASH)
	elif day and day <= 365:
		apr = ((total_bonus + total_cc_fees)) / (cash_balance - STARTING_CASH)

	history.append({
		'day': day,
		'cash_balance': cash_balance,

		'apr': apr,

		'coffee_expenses': coffee_expenses,
		'total_coffee_expenses': total_coffee_expenses,

		'recurring_deposits': recurring_deposits,
		'deposits': deposits,
		'total_deposits': total_deposits,
		'bonus': bonus,
		'total_bonus': total_bonus,

		'deposit_cc_fees': deposit_cc_fees,
		'coffee_cc_fees': coffee_cc_fees,
		'credit_card_fees': credit_card_fees,
		'total_cc_fees': total_cc_fees,

		# should match cash_balance
		'total_deposits - total_coffee_expenses - total_cc': total_deposits - total_coffee_expenses - total_cc_fees,

		'cashflow': deposits - coffee_expenses - credit_card_fees,

		'credit_balance': AVAILABLE_CREDIT - credit_balance,
		'remaining_credit': credit_balance,

		'users': len(users),
		'new_users': new_users,
		'total_referrals': total_referrals,
		'remaining_balances': sum([x['balance'] for x in users]),

		'total_marketing': total_marketing,
		'total_addon_revenue': total_addon_revenue,

		'interest_cost': interest_cost,
		'interest_paid': interest_paid,

		'unrealized profit': total_addon_revenue - interest_paid - total_bonus - total_cc_fees - total_marketing,
		'unrealized profit less marketing': total_addon_revenue - interest_paid - total_bonus - total_cc_fees, 
		'cost of cash %': (interest_paid + total_bonus + total_cc_fees + total_marketing) / cash_balance,

		'average account balance': sum([x['balance'] for x in users]) / len(users) if len(users) > 0 else 0,
		'cost / user': (interest_paid + total_cc_fees + total_bonus + total_marketing) / len(users) if len(users) > 0 else 0,
	})

print('graphs')

# turn history into a pandas dataframe
df = pd.DataFrame(history)

# plot the cash balance on the top graph and the rest on the below graph then save to ./output/coffee.png
fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(7, 1, figsize=(10, 20))
df.plot(x='day', y=['cash_balance', 'remaining_credit', 'unrealized profit'], ax=ax1)
df.plot(x='day', y=['remaining_balances', 'total_bonus'], ax=ax2)
df.plot(x='day', y=['coffee_expenses', 'bonus', 'credit_card_fees', 'deposits', 'recurring_deposits', 'total_marketing', 'total_addon_revenue'], ax=ax3)
df.plot(x='day', y=['interest_cost', 'cashflow'], ax=ax4)
df.plot(x='day', y=['total_deposits', 'total_coffee_expenses', 'remaining_balances'], ax=ax5)
df.plot(x='day', y=['users', 'total_referrals'], ax=ax6)
df.plot(x='day', y=['apr', 'cost of cash %'], ax=ax7)
ax7.set_ylim(0, 0.5)
plt.savefig('./output/coffee.png')

print("Done!")