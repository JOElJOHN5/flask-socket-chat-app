from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO
app = Flask(__name__)
#app config
app.config["SECRET_KEY"] = "mysecret"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app, manage_session=False)
from socketIOApp import routes