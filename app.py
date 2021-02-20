from flask import Flask, render_template
import requests
app = Flask(__name__)

@app.route("/")
def index():
    btc_gbp = requests.get("https://api.blockchain.com/v3/exchange/tickers/BTC-GBP")
    btc_eur = requests.get("https://api.blockchain.com/v3/exchange/tickers/BTC-EUR")

    btc_gbp_data = btc_gbp.json()
    btc_eur_data = btc_eur.json()

    eth_gbp = requests.get("https://api.blockchain.com/v3/exchange/tickers/ETH-GBP")
    eth_eur = requests.get("https://api.blockchain.com/v3/exchange/tickers/ETH-EUR")

    eth_gbp_data = eth_gbp.json()
    eth_eur_data = eth_eur.json()

    ltc_gbp = requests.get("https://api.pro.coinbase.com/products/LTC-GBP/stats")
    ltc_eur = requests.get("https://api.pro.coinbase.com/products/LTC-EUR/stats")

    ltc_gbp_data = ltc_gbp.json()
    ltc_eur_data = ltc_eur.json()

    return render_template('index.html', btc_gbp_data=btc_gbp_data, btc_eur_data=btc_eur_data, eth_gbp_data=eth_gbp_data, eth_eur_data=eth_eur_data, ltc_gbp_data=ltc_gbp_data, ltc_eur_data=ltc_eur_data)

@app.route("/prices")
def prices():
    return render_template('prices.html')

@app.route("/exchanges")
def exchanges():
    return render_template('exchanges.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run()