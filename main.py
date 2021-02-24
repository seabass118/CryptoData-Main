from flask import Flask, render_template, request, redirect
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel,db,login
from flask_socketio import SocketIO
from datetime import datetime
from flask_gravatar import Gravatar

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
db.init_app(app)
login.init_app(app)
login.login_view = 'login'

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


@app.before_first_request
def create_all():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/session')
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/session')
     
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/session')
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')
             
        user = UserModel(email=email, username=username, date_registered=datetime.now())
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/session')
@login_required
def sessions():
    return render_template('session.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True)
