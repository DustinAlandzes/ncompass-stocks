from alpha_vantage.timeseries import TimeSeries
from flask import Flask, render_template, request
import json

app = Flask(__name__)

# load config file
# just api key for now
with open("config.json") as config_file:
	config = json.load(config_file)

# init TimeSeries object with api key
# outputs pandas dataframes
ts = TimeSeries(key=config["api_key"], output_format='pandas')

def fetch_ticker_data(tickers):
	# fetch daily price for each ticker
	for ticker in tickers:
		print(ticker['symbol'])
		data, meta_data = ts.get_daily(symbol=ticker['symbol'])
		# round to two decimal places
		data = data.round(2)
		ticker["price"] = data["close"][-1]
		ticker["difference"] = round(data["close"][-1] - data["close"][-2], 2)
		# round to 4 decimal places
		ticker["percentage"] = round(ticker["difference"] / data["close"][-1], 4)
		#print("{} - {} - {} - {}".format(ticker['label'], ticker["price"], ticker["difference"], ticker["percentage"]))
	return tickers

@app.route("/")
def index():
	# get style parameters
	style = {"background": request.args.get("background"),
		"font-size": request.args.get("font-size"),
		"font-color": request.args.get("font-color"),
		"font-weight": request.args.get("font-weight")
	}
	# get symbol & label parameters
	symbols = [symbol.strip() for symbol in request.args.get("symbols").split(',')]
	labels = [label.strip() for label in request.args.get("labels").split(',')]

	# combine symbol & tlabels into ticker list
	# in order to pass to fetch_ticker_data
	tickers = []
	for symbol, label in zip(symbols, labels):
		tickers.append({'symbol': symbol, 'label': label})

	# fetch data
	tickers = fetch_ticker_data(tickers)

	# pass data to jinja2/html
	return render_template("index.html", tickers=tickers, style=style)

if __name__ == "__main__":
	app.run(host='127.0.0.1', port=8000, debug=True)
