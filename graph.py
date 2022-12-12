#!/usr/bin/env python
import matplotlib.pyplot as plt
import pandas as pd
import os

import data as d
import indicators as ind

# load file from data.py
tlt_5m, nom, tips = d.get_data()
print("Done loading data.")

tlt_5m_raw = tlt_5m

wins = 0
days = []

for num in range(200, len(tlt_5m_raw)):
	tlt_5m = tlt_5m_raw.iloc[num-200:num].copy()

	is_b = ind.is_buy(tlt_5m)

	if is_b:
		wins += 1

		# add the day to the list if it doesn't exist
		day = tlt_5m.index[-1].strftime("%Y-%m-%d %H:%M:%S")
		if day not in days:
			days.append(day)

for day in sorted(days):
	print(day)

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

# plot the two graphs above and below to compare
fig3, (ax, ax2) = plt.subplots(2, 1, figsize=(20,16))

# remove inner padding of ax and ax2
ax.margins(x=0)
ax2.margins(x=0)

# change top padding to .5
fig3.subplots_adjust(top=0.95, bottom=0.15, left=0.05, right=0.95, hspace=0, wspace=0)

ax.plot(tlt_5m.index, tlt_5m["Close"], label="Close")

# plot moving average with color yellow
ax.plot(tlt_5m.index, ma_20, label="MA 20", color="red", alpha=1)
ax.plot(tlt_5m.index, ma_50, label="MA 50", color="red", alpha=0.5)
ax.plot(tlt_5m.index, ma_100, label="MA 100", color="orange", alpha=1)
ax.plot(tlt_5m.index, ma_200, label="MA 200", color="orange", alpha=0.5)

ticklabels = ax.get_xticklabels()

# set all labels to invisible
for label in ticklabels:
	label.set_visible(False)

# # add vertical line to the plot on the start of every monday. only the first 5 min interval
# for day_str in tlt_5m.index:
# 		day = pd.to_datetime(day_str)
# 		if day.weekday() == 0 and day.hour == 9 and day.minute == 30:
# 				ax.axvline(day_str, color="black", alpha=0.5)
# 		elif day.hour == 9 and day.minute == 30:
# 				ax.axvline(day_str, color="black", alpha=0.1)

#     # set visible label if it is 9:30am
# 		if day.hour == 9 and day.minute == 30:
# 			label = ticklabels[tlt_5m.index.get_loc(day_str)]
# 			label.set_visible(True)

ax.legend(loc="upper left")
ax.set_title("TLT 5m Prices and Moving Averages")

# calculate and plot macd using 18 and 39 day ema
macd = ema_18 - ema_39
ax2.plot(tlt_5m.index, macd, label="MACD", color="red", alpha=1)

# calculate and plot signal line using 9 day ema
signal = macd.ewm(span=9, adjust=False).mean()
ax2.plot(tlt_5m.index, signal, label="Signal", color="blue", alpha=1)

# plot the difference between macd and signal line as a bar
ax2.bar(tlt_5m.index, macd - signal, label="MACD - Signal", color="green", alpha=0.5)

ticklabels2 = ax2.get_xticklabels()

# set all labels to invisible
for label in ticklabels2:
	label.set_visible(False)

# # add vertical line to the plot on the start of every monday. only the first 5 min interval
# for day_str in tlt_5m.index:
# 		day = pd.to_datetime(day_str)
# 		if day.weekday() == 0 and day.hour == 9 and day.minute == 30:
# 				ax2.axvline(day_str, color="black", alpha=0.5)
# 		elif day.hour == 9 and day.minute == 30:
# 				ax2.axvline(day_str, color="black", alpha=0.1)

#     # set visible label if it is 9:30am
# 		if day.weekday() == 0 and day.hour == 9 and day.minute == 30:
# 			label = ticklabels2[tlt_5m.index.get_loc(day_str)]
# 			label.set_visible(True)

for day_str in days:
	ax.axvline(day_str, color="green", alpha=1)
	ax2.axvline(day_str, color="green", alpha=1)

ax2.legend(loc="upper left")
ax2.set_title("TLT 5m MACD", y=0.95)


# when to buy
# macd has to be moving up and above/near zero
# is_macd_up_and_crossing = macd[-12:].mean() > 0 and abs(macd[-1]) < 0.05
# print("is_macd_up_and_crossing", is_macd_up_and_crossing)

# # is ma_20 above ma_50 or slope of ma_20 is greater than slope of ma_50
# is_ma_20_crossing_ma_50 = ma_20[-1] - ma_20[-2] > (ma_50[-1] - ma_50[-2]) * 1.5 and abs(ma_20[-1] - ma_50[-1]) < 0.05
# print("is_ma_20_crossing_ma_50", is_ma_20_crossing_ma_50)

# is_buy = is_macd_up_and_crossing and is_ma_20_crossing_ma_50
# print("is_buy", is_buy)




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

# # when to sell
# macd is making a peak above zero
# moving average ribbon is near or crossing downwards

# when to short
# macd has to be moving down and below/near zero
# moving average ribbon is crossing downwards and maintaining

# when to cover short
# macd is making a trough below zero
# moving average ribbon is near or crossing upwards



# add text to the bottom of the plot
fig3.text(0.1, 0.095, "TLT 5m Prices and Moving Averages", ha="left", va="bottom", fontsize=16)
fig3.text(0.1, 0.07, "TLT 5m Prices and Moving Averages", ha="left", va="bottom", fontsize=16)
fig3.text(0.1, 0.045, "TLT 5m Prices and Moving Averages", ha="left", va="bottom", fontsize=16)

fig3.text(0.4, 0.095, "TLT 5m Prices and Moving Averages", ha="left", va="bottom", fontsize=16)
fig3.text(0.4, 0.07, "TLT 5m Prices and Moving Averages", ha="left", va="bottom", fontsize=16)
fig3.text(0.4, 0.045, "TLT 5m Prices and Moving Averages", ha="left", va="bottom", fontsize=16)

fig3.text(0.7, 0.095, "TLT 5m Prices and Moving Averages", ha="left", va="bottom", fontsize=16)
fig3.text(0.7, 0.07, "TLT 5m Prices and Moving Averages", ha="left", va="bottom", fontsize=16)
fig3.text(0.7, 0.045, "TLT 5m Prices and Moving Averages", ha="left", va="bottom", fontsize=16)

# save the plot
plt.savefig("output/TLT_5m.png")
