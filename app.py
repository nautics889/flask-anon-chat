from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, 'messages.db')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Message(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    message = db.Column('message', db.String(500))
    time = db.Column('time', db.String(80))

    def __repr__(self):
        return '<Message %r>' % self.message

@app.route('/')
def flood():
    return render_template('flood.html')

@app.route("/receiveMessage", methods=["POST"])
def receiveMessage():
    message_text = request.form['chatText']
    time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    if message_text.strip() != '':
        message = Message(message=message_text, time=time)
        db.session.add(message)
        db.session.commit()
    return ('', 204)

@app.route("/sendMessages")
def sendMessage():
    data = renderMessages()
    return data

def renderMessages():
    structure = '''{% for msg in messages %}
                        <p>{{msg.message}} - {{msg.time}}</p>
                   {% endfor %}'''

    messages = Message.query.order_by('-id').limit(3).all()
    messages.reverse()
    return render_template_string(structure, messages=messages)

if __name__ == '__main__':
    app.run(debug=True)