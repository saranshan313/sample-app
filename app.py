# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from os import environ
# from flask_mysqldb import MySQL,MySQLdb
# import MySQLdb.cursors
import re
import mysql.connector
import json

app = Flask(__name__)


app.secret_key = 'your secret key'

dbCreds = 0
with open('db_creds.json', 'r') as f:
    dbCreds = json.load(f)
    config = {
        'user': dbCreds['DB_USER'],
        'password': dbCreds['DB_PASSWORD'],
        'host': dbCreds['DB_HOST'],
        'port': dbCreds['DB_PORT'],
        'database': dbCreds['DB_NAME']
    }
f.close()
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'geekprofile'

# config = {
#     'user': environ.get('DB_USER'),
#     'password': environ.get('DB_PASSWORD'),
#     'host': environ.get('DB_HOST'),
#     'port': environ.get('DB_PORT'),
#     'database': environ.get('DB_NAME')
# }

# mysql = MySQL(app)
connection = mysql.connector.connect(**config)


@app.route('/healthcheck')
def healthcheck():
    return 'Health is Ok'


@app.route('/')
def initialise():
    print("Creating database tabel")
#    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS accounts \
                   (id int(11) NOT NULL AUTO_INCREMENT, \
                   username varchar(50) NOT NULL, \
                   password varchar(255) NOT NULL, \
                   email varchar(100) NOT NULL, \
                   organisation varchar(100) NOT NULL, \
                   address varchar(100) NOT NULL, \
                   city varchar(100) NOT NULL, \
                   state varchar(100) NOT NULL, \
                   country varchar(100) NOT NULL, \
                   postalcode varchar(100) NOT NULL, \
                   PRIMARY KEY(`id`))')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if (request.method == 'POST' and
            'username' in request.form and
            'password' in request.form):
        username = request.form['username']
        password = request.form['password']

#        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password, ))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():

    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if (request.method == 'POST' and
        'username' in request.form and
        'password' in request.form and
        'email' in request.form and
        'address' in request.form and
        'city' in request.form and
        'country' in request.form and
        'postalcode' in request.form and
            'organisation' in request.form):
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        organisation = request.form['organisation']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']

#        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO accounts VALUES \
                           (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (username, password, email, organisation, address, city, state, country, postalcode, ))
            connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))


@app.route("/display")
def display():
    if 'loggedin' in session:
        #        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
#        print(session['id'])
        cursor.execute('SELECT * FROM accounts WHERE id = %s',
                       (session['id'], ))
        account = cursor.fetchone()
#        print(account)
        return render_template("display.html", account=account)
    return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if (request.method == 'POST' and
            'username' in request.form and
            'password' in request.form and
            'email' in request.form and
            'address' in request.form and
            'city' in request.form and
            'country' in request.form and
            'postalcode' in request.form and
                'organisation' in request.form):
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            organisation = request.form['organisation']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postalcode = request.form['postalcode']
#            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM accounts WHERE username = %s', (username, ))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE accounts SET \
                               username = %s, password = %s, email = %s, \
                               organisation = %s, address = %s, city = %s, \
                               state = %s, country = %s, postalcode = %s \
                               WHERE id = %s', (username, password, email, organisation,
                                                address, city, state, country, postalcode, session['id'], ))
                connection.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="localhost", port=int("80"))
