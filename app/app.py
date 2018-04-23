from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy

import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)

class History(db.Model):
	id = db.Column('id', db.Integer, primary_key=True)
	message = db.Column('message', db.String(500))
	time = db.Column('time', db.String(80))

@socketio.on('message')
def handleMessage(msg):
	now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
	print('Message: ' + msg + now)


	message = History(message=msg, time=now)
	db.session.add(message)
	db.session.commit()

	send(msg+now, broadcast=True)

@app.route('/')
def index():
	messages = History.query.all()
	return render_template('index.html', messages=messages)

if __name__ == '__main__':
	socketio.run(app)
