#!/usr/bin/env python
import matplotlib.pyplot as plt
import pandas as pd
import os

import data as d
import indicators as ind

d.download_data()

# load file from data.py
tlt_5m, nom, tips = d.get_data()
print("Done loading data.")

DAYS = 21

tlt_5m_raw = tlt_5m.iloc[-(12*8*DAYS):]

ma_200 = tlt_5m["Close"].rolling(50).mean()

# normal distribution of ma_200 slopes magnitudes to it's own plot and save to a png in output/ma_200_slopes.png
ma_200_slope = ma_200.diff()
ma_200_slope_magnitude = ma_200_slope
fig, (ax) = plt.subplots(1, 1, figsize=(20,12))
ax.hist(ma_200_slope_magnitude, bins=100)
ax.set_title("ma_200_slope_magnitude")
ax.set_xlabel("ma_200_slope_magnitude")
ax.set_ylabel("count")
plt.savefig("output/ma_200_slope_magnitude.png")

print("Last slope: ", ma_200_slope[-1])

wins = 0
days = []

offset = 200
r = 1000

for num in range(offset, len(tlt_5m_raw)):
	if num % 5 != 0:
		continue

	tlt_5m = tlt_5m_raw.iloc[max(0,num-r):num].copy()

	is_b = ind.is_buy(tlt_5m)

	if is_b:
		wins += 1

		# add the day to the list if it doesn't exist
		day = tlt_5m.index[-1]#.strftime("%Y-%m-%d %H:%M:%S")
		if day not in days:
			days.append(day)

for day in sorted(days):
	print(day)

# copy the tlt_5m and change the index to string
tlt_5m = tlt_5m_raw.copy()
tlt_5m.index = tlt_5m.index.strftime("%Y-%m-%d %H:%M:%S")

# plot the two graphs above and below to compare
fig3, (ax) = plt.subplots(1, 1, figsize=(20,12))

# remove inner padding of ax and ax2
ax.margins(x=0)

# change top padding to .5
fig3.subplots_adjust(top=0.95, bottom=0.15, left=0.05, right=0.95, hspace=0, wspace=0)

ax.plot(tlt_5m.index, tlt_5m["Close"], label="Close")

ticklabels = ax.get_xticklabels()

# set all labels to invisible
for label in ticklabels:
	label.set_visible(False)

# # add vertical line to the plot on the start of every monday. only the first 5 min interval
for day_str in tlt_5m.index:
		day = pd.to_datetime(day_str)
		if day.weekday() == 0 and day.hour == 9 and day.minute == 30:
				ax.axvline(day_str, color="black", alpha=1)
		elif day.hour == 9 and day.minute == 30:
				ax.axvline(day_str, color="black", alpha=0.1)

#     # set visible label if it is 9:30am
# 		if day.hour == 9 and day.minute == 30:
# 			label = ticklabels[tlt_5m.index.get_loc(day_str)]
# 			label.set_visible(True)

ax.legend(loc="upper left")
ax.set_title("TLT 5m Prices and Moving Averages")

# set all labels to invisible
for label in ticklabels:
	label.set_visible(False)

# add vertical line to the plot on the start of every monday. only the first 5 min interval
for day_str in tlt_5m.index:
		day = pd.to_datetime(day_str)

    # set visible label if it is 9:30am
		if day.weekday() == 0 and day.hour == 9 and day.minute == 30:
			label = ticklabels[tlt_5m.index.get_loc(day_str)]
			label.set_visible(True)

for day_str in days:
	ax.axvline(day_str, color="green", alpha=1)

# save the plot
plt.savefig("output/TLT_5m_buys.png")

print("Done plotting.")
