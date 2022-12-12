#!/usr/bin/env python
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import random


def is_buy(tlt_5m_raw):
	# copy the tlt_5m and change the index to string
	tlt_5m = tlt_5m_raw.copy()
	tlt_5m.index = tlt_5m.index.strftime("%Y-%m-%d %H:%M:%S")

	# calculate 20 day moving average 
	ma_20 = tlt_5m["Close"].rolling(20).mean()
	ma_50 = tlt_5m["Close"].rolling(50).mean()
	ma_100 = tlt_5m["Close"].rolling(100).mean()
	ma_200 = tlt_5m["Close"].rolling(200).mean()

	# calculate 18 day exponential moving average 
	ema_18 = tlt_5m["Close"].ewm(span=18, adjust=False).mean()
	ema_39 = tlt_5m["Close"].ewm(span=39, adjust=False).mean()

	macd = ema_18 - ema_39

	# when to buy
	# macd has to be moving up and above/near zero
	# 12 day slope
	is_macd_up_and_crossing = macd.rolling(72).mean().diff()[-1] > 0 and abs(macd[-1]) < 0.05

	# is ma_20 above ma_50 or slope of ma_20 is greater than slope of ma_50
	is_ma_20_crossing_ma_50 = ma_20[-1] - ma_20[-2] > (ma_50[-1] - ma_50[-2]) * 1.25 and abs(ma_20[-1] - ma_50[-1]) < 0.05

	is_ma_50_slope_above_zero = ma_50.diff()[-1] > 0

	is_buy = is_macd_up_and_crossing and is_ma_20_crossing_ma_50 and is_ma_50_slope_above_zero

	return is_buy




# # slope of ma_20 of rolling 12 has to be greater than slope of ma_50 of rolling 12
# is_ma_slope_up = ma_20[-12:].mean() > ma_50[-12:].mean()
# is_near_cross = abs(ma_20[-1] - ma_50[-1]) < 0.05
# print("is_ma_slope_up", is_ma_slope_up)
# print("is_near_cross", is_near_cross)

# # moving average ribbon is crossing upwards and maintaining
# is_ma_up = ma_20 > ma_50 and ma_50 > ma_100 and ma_100 > ma_200
# # second moving average is crossing upwards. indicating a longer up trend
# if macd[-1] > 0 and macd[-1] > signal[-1] and macd[-2] < signal[-2] and ma_20[-1] > ma_50[-1] and ma_50[-1] > ma_100[-1] and ma_100[-1] > ma_200[-1]:
# 		print("BUY")

# when to sell
# macd is making a peak above zero
# moving average ribbon is near or crossing downwards

# when to short
# macd has to be moving down and below/near zero
# moving average ribbon is crossing downwards and maintaining

# when to cover short
# macd is making a trough below zero
# moving average ribbon is near or crossing upwards




# use yahoo finance to get tlt ticker prices by 5m frequency
tlt = yf.Ticker("TLT")
# get tlt prices by 5m frequency for 60 days
tlt_5m_raw = tlt.history(period="45d", interval="5m")
print('received data from yahoo finance')

wins = 0
days = []

print(len(tlt_5m_raw))

for num in range(200, len(tlt_5m_raw)):
	tlt_5m = tlt_5m_raw.iloc[num-200:num].copy()

	is_b = is_buy(tlt_5m)

	if is_b:
		wins += 1

		# add the day to the list if it doesn't exist
		day = tlt_5m.index[-1].strftime("%Y-%m-%d %H:%M:%S")
		if day not in days:
			days.append(day)

for day in sorted(days):
	print(day)

print("wins", wins, 'percent', wins / 1000)