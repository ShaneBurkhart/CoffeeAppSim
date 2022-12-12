#!/usr/bin/env python
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import os

def download_data():
	# create the directory ./data/bonds and ./data/stocks if they don't exist
	os.makedirs("./data/bonds", exist_ok=True)
	os.makedirs("./data/stocks", exist_ok=True)

	# download the 5m data for TLT for 60d and save to ./data/bonds/tlt_5m.csv
	tlt_5m = yf.download("TLT", period="60d", interval="5m")
	tlt_5m.to_csv("./data/stocks/tlt_5m.csv")

	# download the daily long term yield curve and tips long term yield curve
	tips_url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2022/all?type=daily_treasury_real_long_term&field_tdr_date_value=2022&page&_format=csv"
	nom_url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2022/all?type=daily_treasury_long_term_rate&field_tdr_date_value=2022&page&_format=csv"
	nom = pd.read_csv(nom_url, index_col="Date", parse_dates=True)
	tips = pd.read_csv(tips_url, index_col="Date", parse_dates=True)

	# save to ./data/bonds/long_term_yield_curve.csv and ./data/bonds/tips_long_term_yield_curve.csv
	nom.to_csv("./data/bonds/long_term_yield_curve.csv")
	tips.to_csv("./data/bonds/tips_long_term_yield_curve.csv")

def get_data():
	# get the 5m data for TLT from ./data/bonds/tlt_5m.csv
	tlt_5m = pd.read_csv("./data/stocks/tlt_5m.csv", index_col="Datetime", parse_dates=True)

	# get the long term yield curve and tips long term yield curve from ./data/bonds/long_term_yield_curve.csv and ./data/bonds/tips_long_term_yield_curve.csv
	nom = pd.read_csv("./data/bonds/long_term_yield_curve.csv", index_col="Date", parse_dates=True)
	tips = pd.read_csv("./data/bonds/tips_long_term_yield_curve.csv", index_col="Date", parse_dates=True)

	return tlt_5m, nom, tips