from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, json
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import create_engine
from parse_and_save import parse_and_save
import pandas as pd
import dxfgrabber
import models

import numpy as np

app = Flask(__name__)
app.secret_key = "^A%DJAJU^JJ123"

# Config MySQL-SQLAchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/_bucketlist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Config Debug
app.debug = True
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/editor')
def editor():
    return render_template('editor.html')


# import mysql.connector
@app.route('/readDB', methods=['GET', 'POST'])
def readDB():
    if request.method == 'POST':
        user = session['username']
        print(user)
        # engine = create_engine('mysql+pymysql://bucketuser:dencopc@localhost/bucketlist')

        connection = mysql.connector.connect(host='192.168.1.10',
                                             database='bucketlist',
                                             user='bucketuser',
                                             password='dencopc')
        nod = pd.read_sql("SELECT * from nodes WHERE user_id='" + user + "'", connection)
        elm = pd.read_sql("SELECT * from elements WHERE user_id='" + user + "'", connection)
        return nod.to_json(orient='table') + '|' + elm.to_json(orient='table')


@app.route('/readDXF', methods=['GET', 'POST'])
def readDXF():
    from dxfin import DXFin
    from io import StringIO
    from createdb import createDB
    if request.method == 'POST':
        fl = (request.get_data()).decode('UTF-8')
        stream = StringIO(fl)
        dxf = dxfgrabber.read(stream)
        nod, elm = DXFin(dxf)
        proj_code = 125  # TEMP
        proj_id = createDB(proj_code, nodes=nod, elements=elm)
        # print (proj_id)
        connection = mysql.connector.connect(host='192.168.1.10'
                                             , database='proj_id'
                                             , user='root'
                                             , password='password')
        user = 'akosmop'  # CAUTION!!!
        nod = pd.read_sql("SELECT * from nodes" + str(proj_id) + " WHERE user_id='" + user + "'", connection)
        elm = pd.read_sql("SELECT * from elements" + str(proj_id) + " WHERE user_id='" + user + "'", connection)
        return nod.to_json(orient='table') + '|' + elm.to_json(orient='table')
    # rsp =(nod.to_json(orient='values')+ '|' + elm.to_json(orient='values'))
    # return rsp
    else:
        return 'Could not read DXF file'


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        usr = models.User(username=username, password=password)
        db.session.add(usr)
        db.session.commit()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Get user by username
        result = models.User.query.filter_by(username=username).first()

        if result is not None:
            # Get stored hash
            password = result.password

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('about'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cursor.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'sucess')
    return redirect(url_for('login'))


# yellow run

@app.route('/save', methods=["GET", "POST"])
def post_req():
    if request.method == 'POST':
        print('yellooooow')
        # engine = create_engine('mysql+pymysql://bucketuser:dencopc@localhost/bucketlist')
        data = request.get_json()
        user_id = session['username']
        print(user_id)
        proj_code = 'bucketlist'
        parse_and_save(proj_code, data)

    return render_template('editor.html')


if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True)

'''
		
		'''
