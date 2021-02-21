from flask import Flask,render_template,request,redirect
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel,db,login
import requests
 
app = Flask(__name__)
app.secret_key = 'xyz'
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///<sqlite db name>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
 
db.init_app(app)
login.init_app(app)
login.login_view = 'login'
 
@app.before_first_request
def create_all():
    db.create_all()
     
# @app.route('/blogs')
# @login_required
# def blog():
#     return render_template('blog.html')

@app.route("/blogs")
@login_required
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

    return render_template('blog.html', btc_gbp_data=btc_gbp_data, btc_eur_data=btc_eur_data, eth_gbp_data=eth_gbp_data, eth_eur_data=eth_eur_data, ltc_gbp_data=ltc_gbp_data, ltc_eur_data=ltc_eur_data)
 
 
@app.route('/', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/blogs')
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/blogs')
     
    return render_template('login.html')
 
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/blogs')
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
 
        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')
             
        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')
 
 
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/blogs')


@app.route("/prices")
@login_required
def prices():
    return render_template('prices.html')

@app.route("/exchanges")
@login_required
def exchanges():
    return render_template('exchanges.html')

@app.route("/about")
@login_required
def about():
    return render_template('about.html')

@app.route("/contact")
@login_required
def contact():
    return render_template('contact.html')