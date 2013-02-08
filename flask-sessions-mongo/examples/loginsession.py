from flask import Flask, session, redirect, url_for, escape, request
from flask_pymongo import PyMongo
from flask_sessions_mongo import sessions_mongo

app = Flask(__name__)

# set up flask-pymongo
app.config['MONGO_DBNAME'] = 'exampledb'
mongo = PyMongo(app)

# set up flask-sessions-mongo
app.config['SESSION_MONGO_PREIX'] = 'MONGO'
app.config['SESSION_MONGO_COLLECTION'] = 'sessions'
sessions_mongo(app) 


@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as %s. <a href="logout">Logout</a>' % escape(session['username'])
    return '''
        You are not logged in.</br>
        <form action="login" method="post">
            <input type="text" name="username" /><br/>
            <input type="submit" value="Login" /><br/>
        </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    session['username'] = request.form['username']
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.run()
