#!/usr/bin/env python

import random
import pandas as pd
import matplotlib.pyplot as plt


# total deposits must grow faster than coffee expenses
# keeping a minimum for perks gives us time with that cash

# TWO BIG INDICATORS
# increase the amount of deposits
# decrease the spending of balances
# maximize the time with the cash 
# maximize average balance


YEARS_TO_SIMULATE =  1.5
MARKETING_SPEND_PER_DAY = 30
ADDITIONAL_MARKETING_SPEND_PER_DAY = 0.1
MARKETING_COST_PER_INSTALL = 3
FIRST_DEPOSIT_BONUS = 2.5

# INPUTS ==========================
REFERRAL_RATE_PER_MONTH = 0.2
MONTHLY_USERS_DEPOSIT_RATE = 0.8

MONTHLY_DEPOSIT_LIMIT = 2000
MONTHLY_COFFEE_EXPENSE_LIMIT = 250

FALLOUT_RATE = 0.1

MIN_COST_OF_COFFEE = 2.5
MAX_COST_OF_COFFEE = 20

MIN_COFFEES_PER_MONTH = 1
MAX_COFFEES_PER_MONTH = 19 

USER_TO_ADDON_CONVERSION_RATE = 0.15
ADDON_PRICE = 10 * 0.7
ADDON_DELAY_DAYS = 30 * 6

CORPORATE_USERS_CONVERSION_RATE = 0.1 / 10
CORPORATE_SUBSCRIPTION_PRICE_PER_USER_PER_MONTH = 5
AVERAGE_NUM_CORPORTATE_USERS = 5

NO_USERS_DAY =  0
NO_RE_DEPOSITS_DAY = 0
# INPUTS ==========================

DAYS_TO_SIMULATE = round(365 * YEARS_TO_SIMULATE)


MEAN_COST_OF_COFFEE = (MIN_COST_OF_COFFEE + MAX_COST_OF_COFFEE) / 2
MEAN_COFFEES_PER_MONTH = (MIN_COFFEES_PER_MONTH + MAX_COFFEES_PER_MONTH) / 2

# limit of 200 in account
# limit of 100 deposit a day
# limit of 20 dollar spend a day
# worst case is they are rewarded with 5 dollars a day for depositing 100 dollars 5 days
# 550 to spend for max reward, that is 27.5 days to spend that 500 of deposit
# if we watch for malicious users and at most they can spend in 27.5 days, then we can ban them easily
# stop them from taking the bonus to the extreme

# average 8 * 10 = 80 dollars a month

# DEPOSIT_OPTIONS = [
# 	{'amount': 5, 'bonus': 0, 'probability': 0.45},
# 	{'amount': 10, 'bonus': 0.25, 'probability': 0.33},
# 	{'amount': 25, 'bonus': 1, 'probability': 0.15},
# 	{'amount': 50, 'bonus': 2.5, 'probability': 0.06},
# 	{'amount': 100, 'bonus': 5, 'probability': 0.02},
# ]

DEPOSIT_OPTIONS = [
	{'amount': 25, 'bonus': 0.25, 'probability': 0.40},
	{'amount': 50, 'bonus': 1.25, 'probability': 0.30},
	{'amount': 100, 'bonus': 5, 'probability': 0.2},
	{'amount': 200, 'bonus': 15, 'probability': 0.07},
	{'amount': 500, 'bonus': 50, 'probability': 0.02},
	{'amount': 1000, 'bonus': 150, 'probability': 0.01},
	{'amount': 2000, 'bonus': 400, 'probability': 0.005},
]
REFILL_THRESHOLD = 20

CREDIT_CARD_FEE = 0.03

DAILY_DEPOSIT_RATE = MONTHLY_USERS_DEPOSIT_RATE / 30


STARTING_CASH = 20000
AVAILABLE_CREDIT = 0

CREDIT_INTEREST_RATE = 0.10


NUM_ADDONS = 1
ADDON_MIN_BALANCE = 25
USER_TO_MIN_BALANCE_ADDON_RATE = 0


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

return_20 = 0

interest_paid = 0

addon_revenue = 0
corporate_revenue = 0

total_coffee_expenses = 0

new_users_yesterday = 0

num_coporate_users = 0

for day in range(DAYS_TO_SIMULATE):
	last_history = history[-1] if history else None
	if last_history and cash_balance != 0:
		print(f'Day {day} of {DAYS_TO_SIMULATE}, users: {len(users)}, cash: {cash_balance}, profit: {last_history["unrealized profit"]}, profit / cash: { last_history["unrealized profit"] / cash_balance * 100:.2f}%')

	if day % 30 == 0:
		for user in users:
			user['monthly_deposits'] = 0
			user['monthly_coffee_expenses'] = 0

	new_deposits = 0
	coffee_expenses = 0
	recurring_deposits = 0
	new_addons = 0
	new_bonus = 0

	if NO_RE_DEPOSITS_DAY <= 0 or day < NO_RE_DEPOSITS_DAY:
		# re deposits
		for i, user in enumerate(users):
			should_refill = user['balance'] <= REFILL_THRESHOLD and random.random() < DAILY_DEPOSIT_RATE
			should_maintain_balance = user['balance'] < ADDON_MIN_BALANCE and random.random() < USER_TO_MIN_BALANCE_ADDON_RATE / 30

			if should_maintain_balance or should_refill:
				deposit = random.choices(DEPOSIT_OPTIONS, weights=[x['probability'] for x in DEPOSIT_OPTIONS])[0]
				amount = deposit['amount']
				bonus = deposit['bonus']

				if user['monthly_deposits'] + amount > MONTHLY_DEPOSIT_LIMIT:
					continue

				users[i]['balance'] += amount + bonus
				users[i]['monthly_deposits'] += amount 

				new_deposits += amount
				recurring_deposits += amount
				total_deposits += amount
				new_bonus += bonus
				total_bonus += bonus

	if NO_USERS_DAY <= 0 or day < NO_USERS_DAY:
		# new users
		referral_rate = REFERRAL_RATE_PER_MONTH / 30
		if day > 900:
			referral_rate = REFERRAL_RATE_PER_MONTH / 30 * 0.2

		new_referrals = round(len(users) * referral_rate)
		total_referrals += new_referrals
		marketing_spend = MARKETING_SPEND_PER_DAY + ADDITIONAL_MARKETING_SPEND_PER_DAY * day
		marketing_installs = round(marketing_spend / MARKETING_COST_PER_INSTALL)
		new_users = marketing_installs + new_referrals
		num_coporate_users += round(new_users * CORPORATE_USERS_CONVERSION_RATE)
		marketing_cost = marketing_spend
		total_marketing += marketing_cost
		for i in range(new_users):
			deposit = random.choices(DEPOSIT_OPTIONS, weights=[x['probability'] for x in DEPOSIT_OPTIONS])[0]
			amount = deposit['amount'] + FIRST_DEPOSIT_BONUS
			bonus = deposit['bonus'] + FIRST_DEPOSIT_BONUS

			if day == ADDON_DELAY_DAYS:
				for i in range(NUM_ADDONS):
					if random.random() < USER_TO_ADDON_CONVERSION_RATE:
						cash_balance += ADDON_PRICE
						addon_revenue += ADDON_PRICE
						new_addons += ADDON_PRICE

			if day > ADDON_DELAY_DAYS:
				for i in range(NUM_ADDONS):
					if random.random() < USER_TO_ADDON_CONVERSION_RATE:
						cash_balance += ADDON_PRICE
						addon_revenue += ADDON_PRICE
						new_addons += ADDON_PRICE
				
			users.append({ 'balance': amount + bonus, 'monthly_deposits': amount, 'monthly_coffee_expenses': 0 })
			new_deposits += amount
			total_deposits += amount
			total_bonus += bonus
			new_bonus += bonus

		if credit_balance > marketing_cost:
			credit_balance -= marketing_cost
		else:
			cash_balance -= marketing_cost

	
	# people spending money on coffee
	for i, user in enumerate(users):
		coffees_per_month = max(random.normalvariate(MEAN_COFFEES_PER_MONTH, (MAX_COFFEES_PER_MONTH - MEAN_COFFEES_PER_MONTH) / 3), 0)

		if random.random() < coffees_per_month / 30:
			# random float between min and max
			cost_of_coffee = min(max(random.normalvariate(MEAN_COST_OF_COFFEE, (MAX_COST_OF_COFFEE - MEAN_COST_OF_COFFEE) / 3), 0), MAX_COST_OF_COFFEE)
			if cost_of_coffee + user['monthly_coffee_expenses'] > MONTHLY_COFFEE_EXPENSE_LIMIT:
				continue

			if user['balance'] >= cost_of_coffee:
				users[i]['balance'] -= cost_of_coffee 
				coffee_expenses += cost_of_coffee 
				users[i]['monthly_coffee_expenses'] += cost_of_coffee
			elif user['balance'] > 0:
				coffee_expenses += user['balance']
				users[i]['monthly_coffee_expenses'] += user['balance']
				users[i]['balance'] = 0
	
	credit_card_fees = coffee_expenses * CREDIT_CARD_FEE

	new_corporate_revenue = num_coporate_users * CORPORATE_SUBSCRIPTION_PRICE_PER_USER_PER_MONTH / 30 * AVERAGE_NUM_CORPORTATE_USERS
	corporate_revenue += new_corporate_revenue
	cash_balance += new_corporate_revenue

	cash_balance += new_deposits
	# pay for stuff
	if credit_balance > coffee_expenses:
		credit_balance -= coffee_expenses
		credit_balance -= credit_card_fees
	else:
		cash_balance -= coffee_expenses
		cash_balance -= credit_card_fees

	total_cc_fees += credit_card_fees

	return_20 = return_20 + cash_balance * 0.2 / 365

	interest_cost = (AVAILABLE_CREDIT - credit_balance) * CREDIT_INTEREST_RATE / 365
	interest_paid += interest_cost

	total_coffee_expenses += coffee_expenses

	new_users_yesterday = new_users

	fallout_num = round(len(users) * FALLOUT_RATE / 365)
	for i in range(fallout_num):
		user = users.pop(random.randint(0, len(users) - 1))


	history.append({
		'day': day,
		'cash_balance': cash_balance,
		'coffee_expenses': coffee_expenses,
		'total_coffee_expenses': total_coffee_expenses,
		'credit_card_fees': credit_card_fees,
		'new_deposits': new_deposits,
		'total_deposits': total_deposits,
		'total_deposits - total_coffee_expenses': total_deposits - total_coffee_expenses,
		'cashflow': new_deposits - coffee_expenses - credit_card_fees + new_addons,
		'credit_balance': AVAILABLE_CREDIT - credit_balance,
		'remaining_credit': credit_balance,
		'total_bonus': total_bonus,
		'new_bonus': new_bonus,
		'remaining_balances': sum([x['balance'] for x in users]),
		'20_return': return_20,
		'total_marketing': total_marketing,
		'interest_cost': interest_cost,
		'interest_paid': interest_paid,
		'cost of cash': interest_paid + total_bonus + total_cc_fees + total_marketing,
		'cost of cash %': (interest_paid + total_bonus + total_cc_fees + total_marketing) / cash_balance,
		'loss / cash': ((interest_paid + total_cc_fees + total_bonus + total_marketing - addon_revenue)) / cash_balance,
		'loss / 12 mo recurring cashflow': (interest_paid + total_cc_fees + total_bonus + total_marketing - addon_revenue) / (recurring_deposits * 12) if recurring_deposits > 0 else 0,
		'users': len(users),
		'new_users': new_users,
		'recurring_deposits': recurring_deposits,
		'new_corporate_revenue': new_corporate_revenue,
		'corporate_revenue': corporate_revenue,
		'unrealized profit': addon_revenue + corporate_revenue - (interest_paid + total_cc_fees + total_bonus + total_marketing),
		'addon_revenue': addon_revenue,
		'addon_revenue + return_20': addon_revenue + return_20,
		'total_referrals': total_referrals,
		'average account balance': sum([x['balance'] for x in users]) / len(users) if len(users) > 0 else 0,
		'cost / user': (interest_paid + total_cc_fees + total_bonus + total_marketing) / len(users) if len(users) > 0 else 0,
	})

print('graphs')

# turn history into a pandas dataframe
df = pd.DataFrame(history)

# plot the cash balance on the top graph and the rest on the below graph then save to ./output/coffee.png
fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(7, 1, figsize=(10, 20))
df.plot(x='day', y=['cash_balance', 'remaining_credit', 'unrealized profit'], ax=ax1)
df.plot(x='day', y=['remaining_balances', 'total_bonus', '20_return', 'corporate_revenue', 'addon_revenue', 'cost of cash', 'total_deposits - total_coffee_expenses'], ax=ax2)
df.plot(x='day', y=['coffee_expenses', 'new_bonus', 'new_corporate_revenue', 'credit_card_fees', 'new_deposits', 'recurring_deposits', 'total_marketing'], ax=ax3)
df.plot(x='day', y=['interest_cost', 'cashflow'], ax=ax4)
df.plot(x='day', y=['total_deposits', 'total_coffee_expenses', 'remaining_balances', 'total_deposits - total_coffee_expenses'], ax=ax5)
df.plot(x='day', y=['users', 'total_referrals'], ax=ax6)
df.plot(x='day', y=['average account balance', 'new_users', 'cost / user'], ax=ax7)
ax7.set_ylim(0, 100)
plt.savefig('./output/coffee.png')

print("Done!")