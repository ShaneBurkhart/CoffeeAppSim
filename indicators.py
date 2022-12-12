import matplotlib.pyplot as plt

def is_buy(tlt_5m_raw):
	# copy the tlt_5m and change the index to string
	tlt_5m = tlt_5m_raw
	tlt_5m.index = tlt_5m.index.strftime("%Y-%m-%d %H:%M:%S")

	# calculate 20 day moving average 
	ma_20 = tlt_5m["Close"].rolling(20).mean()
	ma_50 = tlt_5m["Close"].rolling(50).mean()
	ma_100 = tlt_5m["Close"].rolling(100).mean()
	ma_200 = tlt_5m["Close"].rolling(200).mean()
	ma_500 = tlt_5m["Close"].rolling(500).mean()

	# calculate 18 day exponential moving average 
	ema_18 = tlt_5m["Close"].ewm(span=18, adjust=False).mean()
	ema_39 = tlt_5m["Close"].ewm(span=39, adjust=False).mean()

	macd = ema_18 - ema_39

	# when to buy
	# macd has to be moving up and above/near zero
	is_macd_up_and_crossing = macd.rolling(150).mean().diff()[-1] > 0 and abs(macd[-1]) < 0.05

	# is ma_20 above ma_50 or slope of ma_20 is greater than slope of ma_50
	is_ma_20_crossing_ma_50 = ma_20[-1] - ma_20[-2] > (ma_50[-1] - ma_50[-2]) * 1.25 and abs(ma_20[-1] - ma_50[-1]) < 0.05

	is_ma_20_slope_above_zero = ma_20.diff()[-1] > 0 and ma_20.diff()[-1] < 0.07
	is_ma_50_slope_above_zero = ma_50.diff()[-1] > 0 and ma_50.diff()[-1] < 0.03
	is_ma_200_slope_above_zero = ma_200.diff()[-1] > 0
	is_ma_500_slope_above_zero = ma_500.diff()[-1] > 0.005 #-0.005

	is_short_term_slope_above_zero = is_ma_20_slope_above_zero and is_ma_50_slope_above_zero

	is_steep_down_ma_50 = ma_50.diff()[-1] < -0.03 and abs((ma_100.diff() - ma_50.diff())[-1]) < 0.03 and ma_50[-1] < ma_100[-1]

	is_up_buy_tmp_down = is_ma_500_slope_above_zero and abs((ma_100.diff() - ma_50.diff())[-1]) > 0 and ma_50[-1] < ma_100[-1]

	is_buy = is_steep_down_ma_50  or is_up_buy_tmp_down
	# is_buy = is_up_buy_tmp_down

	return is_buy


