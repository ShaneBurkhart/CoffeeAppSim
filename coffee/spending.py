import random
import deposits
import constants as c

MONTHLY_SPENDING_THRESHOLDS_BY_TIERS = {
	c.MAXIMUM_TIER: 150,
	c.AVERAGE_TIER: 100,
	c.LIGHT_TIER: 50,
	c.MICRO_TIER: 25,
}

CC_FEES_RATE = 0.002
CC_FEES_FLAT = 0.2

MIN_COST_OF_COFFEE = 2.5
MAX_COST_OF_COFFEE = 20

MIN_COFFEES_PER_MONTH = 1
MAX_COFFEES_PER_MONTH = 19 

MEAN_COST_OF_COFFEE = (MIN_COST_OF_COFFEE + MAX_COST_OF_COFFEE) / 2
MEAN_COFFEES_PER_MONTH = (MIN_COFFEES_PER_MONTH + MAX_COFFEES_PER_MONTH) / 2

MIN_COST_OF_COFFEE = 2.5
MAX_COST_OF_COFFEE = 20

MIN_COFFEES_PER_MONTH = 1
MAX_COFFEES_PER_MONTH = 19 

DAILY_COFFEE_EXPENSE_LIMIT = 20
MONTHLY_COFFEE_EXPENSE_LIMIT = 250

def calculate_coffees_per_month():
	return max(random.normalvariate(MEAN_COFFEES_PER_MONTH, (MAX_COFFEES_PER_MONTH - MEAN_COFFEES_PER_MONTH) / 3), 0)

def coffee_spending(day, users):
	coffee_expenses = 0
	cc_fees = 0

	# people spending money on coffee
	for i, user in enumerate(users):
		if 'daily_coffee_expenses' not in user:
			users[i]['daily_coffee_expenses'] = 0
		if 'monthly_coffee_expenses' not in user:
			users[i]['monthly_coffee_expenses'] = 0
		if 'max_monthly_coffee_expenses' not in user:
			users[i]['max_monthly_coffee_expenses'] = 0

		# reset monthly coffee expenses
		if day % 30 == 1:
			users[i]['monthly_coffee_expenses'] = 0

		# reset daily coffee expenses
		users[i]['daily_coffee_expenses'] = 0

		coffees_per_month = users[i]['coffees_per_month']

		if random.random() < coffees_per_month / 30:
			cost_of_coffee = min(max(random.normalvariate(MEAN_COST_OF_COFFEE, (MAX_COST_OF_COFFEE - MEAN_COST_OF_COFFEE) / 3), 0), MAX_COST_OF_COFFEE)
			# add credit card fees
			cc_fees += cost_of_coffee * CC_FEES_RATE + CC_FEES_FLAT

			# can't buy if over the daily or monthly limit
			if cost_of_coffee + user['monthly_coffee_expenses'] > MONTHLY_COFFEE_EXPENSE_LIMIT or cost_of_coffee + user['daily_coffee_expenses'] > DAILY_COFFEE_EXPENSE_LIMIT:
				continue

			if user['balance'] >= cost_of_coffee:
				coffee_expenses += cost_of_coffee 
				users[i]['monthly_coffee_expenses'] += cost_of_coffee
				users[i]['daily_coffee_expenses'] += cost_of_coffee
				users[i]['balance'] -= cost_of_coffee 
			elif user['balance'] > 0:
				coffee_expenses += user['balance']
				users[i]['monthly_coffee_expenses'] += user['balance']
				users[i]['daily_coffee_expenses'] += user['balance']
				users[i]['balance'] = 0
		
		# upgrade tiers if they reach the spending thresholds
		if users[i]['max_monthly_coffee_expenses'] < users[i]['monthly_coffee_expenses']:
			users[i]['max_monthly_coffee_expenses'] = users[i]['monthly_coffee_expenses']

			if users[i]['max_monthly_coffee_expenses'] >= MONTHLY_SPENDING_THRESHOLDS_BY_TIERS[c.MAXIMUM_TIER]:
				users[i]['tier'] = c.MAXIMUM_TIER
			elif users[i]['max_monthly_coffee_expenses'] >= MONTHLY_SPENDING_THRESHOLDS_BY_TIERS[c.AVERAGE_TIER]:
				users[i]['tier'] = c.AVERAGE_TIER
			elif users[i]['max_monthly_coffee_expenses'] >= MONTHLY_SPENDING_THRESHOLDS_BY_TIERS[c.LIGHT_TIER]:
				users[i]['tier'] = c.LIGHT_TIER
			elif users[i]['max_monthly_coffee_expenses'] >= MONTHLY_SPENDING_THRESHOLDS_BY_TIERS[c.MICRO_TIER]:
				users[i]['tier'] = c.MICRO_TIER
	
	return coffee_expenses, cc_fees