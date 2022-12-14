import random
import spending
import constants as c

DEPOSIT_TIERS = {}
DEPOSIT_TIERS[c.MAXIMUM_TIER] = [
	{'amount': 500, 'bonus': 0, 'probability': 0.65},
	{'amount': 1000, 'bonus': 25, 'probability': 0.30},
	{'amount': 2000, 'bonus': 150, 'probability': 0.05},
]
DEPOSIT_TIERS[c.AVERAGE_TIER] = [
	{'amount': 200, 'bonus': 0, 'probability': 0.60},
	{'amount': 500, 'bonus': 10, 'probability': 0.30},
	{'amount': 1000, 'bonus': 75, 'probability': 0.09},
	{'amount': 2000, 'bonus': 300, 'probability': 0.01},
]
DEPOSIT_TIERS[c.LIGHT_TIER] = [
	{'amount': 100, 'bonus': 0, 'probability': 0.60},
	{'amount': 200, 'bonus': 4, 'probability': 0.30},
	{'amount': 500, 'bonus': 25, 'probability': 0.09},
	{'amount': 1000, 'bonus': 75, 'probability': 0.01},
]
DEPOSIT_TIERS[c.MICRO_TIER] = [
	{'amount': 50, 'bonus': 0, 'probability': 0.60},
	{'amount': 100, 'bonus': 2, 'probability': 0.30},
	{'amount': 200, 'bonus': 10, 'probability': 0.09},
	{'amount': 500, 'bonus': 50, 'probability': 0.01},
]
DEPOSIT_TIERS[c.STARTER_TIER] = [
	{'amount': 50, 'bonus': 0, 'probability': 0.50},
	{'amount': 100, 'bonus': 1, 'probability': 0.30},
	{'amount': 200, 'bonus': 4, 'probability': 0.15},
	{'amount': 500, 'bonus': 20, 'probability': 0.04},
	{'amount': 1000, 'bonus': 50, 'probability': 0.009},
	{'amount': 2000, 'bonus': 150, 'probability': 0.001},
]

THROTTLE_DEPOSIT_TIERS = {}
THROTTLE_DEPOSIT_TIERS[c.MAXIMUM_TIER] = [
	{'amount': 1000, 'bonus': 10, 'probability': 0.30},
	{'amount': 2000, 'bonus': 50, 'probability': 0.05},
]
THROTTLE_DEPOSIT_TIERS[c.AVERAGE_TIER] = [
	{'amount': 500, 'bonus': 0, 'probability': 0.30},
	{'amount': 1000, 'bonus': 25, 'probability': 0.09},
	{'amount': 2000, 'bonus': 100, 'probability': 0.01},
]
THROTTLE_DEPOSIT_TIERS[c.LIGHT_TIER] = [
	{'amount': 200, 'bonus': 0, 'probability': 0.30},
	{'amount': 500, 'bonus': 15, 'probability': 0.09},
	{'amount': 1000, 'bonus': 50, 'probability': 0.01},
]
THROTTLE_DEPOSIT_TIERS[c.MICRO_TIER] = [
	{'amount': 100, 'bonus': 0, 'probability': 0.30},
	{'amount': 200, 'bonus': 5, 'probability': 0.09},
	{'amount': 500, 'bonus': 25, 'probability': 0.01},
]
THROTTLE_DEPOSIT_TIERS[c.STARTER_TIER] = [
	{'amount': 100, 'bonus': 0, 'probability': 0.30},
	{'amount': 200, 'bonus': 2, 'probability': 0.15},
	{'amount': 500, 'bonus': 10, 'probability': 0.04},
	{'amount': 1000, 'bonus': 30, 'probability': 0.009},
	{'amount': 2000, 'bonus': 80, 'probability': 0.001},
]

# DEPOSIT_TIERS = THROTTLE_DEPOSIT_TIERS

# **** INPUTS ****
REFERRAL_RATE_PER_MONTH = 0.1
MONTHLY_USERS_DEPOSIT_RATE = 0.5

THROTTLE_BONUS_DAY = 0
THROTTLE_RE_DEPOSIT_RATE = 0.7
THROTTLE_REFERRAL_RATE = 0.25
# ================


# MARKETING_SPEND_PER_DAY = 0
ADDITIONAL_MARKETING_SPEND_PER_DAY = 0
MARKETING_SPEND_PER_DAY = 30
# ADDITIONAL_MARKETING_SPEND_PER_DAY = 0.1
FIRST_DAY_USERS = 100
MARKETING_COST_PER_INSTALL = 3
FIRST_DEPOSIT_BONUS = 2.5

USER_REFILL_THRESHOLD = 15
# DAILY_DEPOSIT_RATE = MONTHLY_USERS_DEPOSIT_RATE / 30
DAILY_DEPOSIT_RATE = MONTHLY_USERS_DEPOSIT_RATE

CREDIT_CARD_FEE_RATE = 0.029
CREDIT_CARD_FEE_FLAT = 0.3

NO_RE_DEPOSITS_DAY = 0
NO_USERS_DAY = 0

# everyone starts with the starter tier
# they can deposit as much as they would like
# as soon as they hit the spending threshold for one month, they get upgraded to the next tier
# they can deposit as much as they would like

def recurring_deposits(day, users):
	if NO_RE_DEPOSITS_DAY > 0 and day >= NO_RE_DEPOSITS_DAY:
		return 0, 0, 0

	recurring_deposits = 0
	new_bonus = 0
	cc_fees = 0

	is_throttle = day >= THROTTLE_BONUS_DAY if THROTTLE_BONUS_DAY > 0 else False

	# re deposits
	for i, user in enumerate(users):
		if 'no_refill' in user and user['no_refill']:
			continue

		# double throttle the rate
		deposit_rate = DAILY_DEPOSIT_RATE * THROTTLE_RE_DEPOSIT_RATE if is_throttle else DAILY_DEPOSIT_RATE
		will_refill = random.random() < deposit_rate
		is_low = user['balance'] <= USER_REFILL_THRESHOLD

		if will_refill and is_low:
			deposit_options = DEPOSIT_TIERS[user['tier']] if not is_throttle else THROTTLE_DEPOSIT_TIERS[user['tier']]
			deposit = random.choices(deposit_options, weights=[x['probability'] for x in deposit_options])[0]

			amount = deposit['amount']
			# single throttle the bonus
			bonus = deposit['bonus'] 

			users[i]['balance'] += amount + bonus
			users[i]['total_deposits'] += amount
			users[i]['total_bonus'] += bonus

			recurring_deposits += amount
			new_bonus += bonus
			cc_fees += amount * CREDIT_CARD_FEE_RATE + CREDIT_CARD_FEE_FLAT
		elif not will_refill and is_low:
			users[i]['no_refill'] = True
		
	return recurring_deposits, new_bonus, cc_fees

def new_user_deposits(day, users):
	if NO_USERS_DAY > 0 and day >= NO_USERS_DAY:
		return 0, 0, 0, 0, 0, 0, 0
	
	is_throttle = day >= THROTTLE_BONUS_DAY if THROTTLE_BONUS_DAY > 0 else False

	# new users
	referral_rate = REFERRAL_RATE_PER_MONTH * THROTTLE_REFERRAL_RATE / 30 if is_throttle else REFERRAL_RATE_PER_MONTH / 30

	new_referrals = round(len(users) * referral_rate)

	marketing_spend = MARKETING_SPEND_PER_DAY + ADDITIONAL_MARKETING_SPEND_PER_DAY * day if not is_throttle else 0
	marketing_installs = round(marketing_spend / MARKETING_COST_PER_INSTALL)

	# if day == 0:
		# marketing_installs = FIRST_DAY_USERS

	new_users = marketing_installs + new_referrals

	new_deposits = 0
	new_bonus = 0
	cc_fees = 0

	for i in range(new_users):
		deposit_options = DEPOSIT_TIERS[c.STARTER_TIER]
		deposit = random.choices(deposit_options, weights=[x['probability'] for x in deposit_options])[0]

		amount = deposit['amount'] 
		bonus = deposit['bonus'] if is_throttle else deposit['bonus'] + FIRST_DEPOSIT_BONUS

		coffees_per_month = spending.calculate_coffees_per_month()
		tier = c.STARTER_TIER

		# tiers of 10	5	2.5	1.25 for each tier
		if coffees_per_month > 0 and coffees_per_month <= 1.25:
			tier = c.MICRO_TIER
		elif coffees_per_month > 1.25 and coffees_per_month <= 2.5:
			tier = c.LIGHT_TIER
		elif coffees_per_month > 2.5 and coffees_per_month <= 5:
			tier = c.AVERAGE_TIER
		elif coffees_per_month > 5:
			tier = c.MAXIMUM_TIER

		users.append({ 
			'tier': tier,
			'balance': amount + bonus, 
			'total_deposits': amount,
			'total_bonus': bonus,
			'coffees_per_month': coffees_per_month,
		})

		new_deposits += amount
		new_bonus += bonus
		cc_fees += amount * CREDIT_CARD_FEE_RATE + CREDIT_CARD_FEE_FLAT

	return new_deposits, new_bonus, new_users, new_referrals, marketing_installs, marketing_spend, cc_fees
