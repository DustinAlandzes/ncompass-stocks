from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt

ts = TimeSeries(key='JR5ZTCL3NVENVSNU', output_format='pandas')
tickers = [
	{'symbol':'.DJI', 'label':'Dow Jones'},
	{'symbol':'.IXIC', 'label':'Nasdaq'},
	{'symbol':'.INX', 'label':'S&P500'},
	{'symbol':'GLD', 'label': 'Gold'}
]

#fig, ax = plt.subplots()

print("{} - {} - {} - {}".format("label", "price", "difference", "percentage"))
	#data.plot(label=ticker['label'])

#plt.legend(loc='best')
#plt.title('Daily price of .DJI, .IXIC, .INX')
#plt.show()

from flask import Flask, render_template, request
app = Flask(__name__)

def fetch_ticker_data(tickers):
	for ticker in tickers:
        	data, meta_data = ts.get_daily(symbol=ticker['symbol'])
        	ticker["price"] = data["close"][-1]
        	ticker["difference"] = data["close"][-1] - data["close"][-2]
        	ticker["percentage"] = ticker["difference"] / data["close"][-1]
        	print("{} - {} - {} - {}".format(ticker['label'], ticker["price"], ticker["difference"], ticker["percentage"]))
	return tickers

@app.route("/")
def index():
	symbols = [symbol.strip() for symbol in request.args.get("symbols").split(',')]
	labels = [label.strip() for label in request.args.get("labels").split(',')]
	tickers = []
	
	for symbol, label in zip(symbols, labels):
		tickers.append({'symbol': symbol, 'label': label})
	tickers = fetch_ticker_data(tickers)
	return render_template("index.html", tickers=tickers)

if __name__ == "__main__":
	app.run(debug=True)
