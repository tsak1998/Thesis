from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from sqlalchemy import create_engine
from parser_ import parser
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
import dxfgrabber
import models
import numpy as np
from computations import main
from save_db import save_db

app = Flask(__name__)
app.secret_key = "^A%DJAJU^JJ123"

# Config MySQL-SQLAchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/yellow'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Config Debug
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# set global engine
engine = create_engine('mysql+pymysql://root:password@localhost/yellow')


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/editor')
def editor():
    if 'logged_in' in session:
        return render_template('editor.html')
    else:
        flash('Unauthorized, Please login', 'danger')
        return redirect(url_for('login'))


@app.route('/getUsername', methods=['POST'])
def get_username():
    if 'logged_in' in session:
        data = {'user': session['username']}
        return jsonify(session['username'])


# import mysql.connector
@app.route('/load', methods=['GET', 'POST'])
def load():
    if request.method == 'POST':
        user = session['username']
        nodes = pd.read_sql("SELECT * from nodes WHERE user_id='" + user + "'", engine)
        del nodes['id'], nodes['user_id']
        elements = pd.read_sql("SELECT * from elements WHERE user_id='" + user + "'", engine)
        del elements['id'], elements['user_id']
        point_loads = pd.read_sql("SELECT * from point_loads WHERE user_id='" + user + "'", engine)
        del point_loads['id'], point_loads['user_id']
        dist_loads = pd.read_sql("SELECT * from dist_loads WHERE user_id='" + user + "'", engine)
        del dist_loads['id'], dist_loads['user_id']
        materials = pd.read_sql("SELECT * from materials WHERE user_id='" + user + "'", engine)
        del materials['id'], materials['user_id']
        sections = pd.read_sql("SELECT * from sections WHERE user_id='" + user + "'", engine)
        del sections['id'], sections['user_id']
        elements.rename(columns={'number': 'en'}, inplace=True)
        nodes.rename(columns={'number': 'nn'}, inplace=True)
        point_loads.rename(columns={'number': 'nn'}, inplace=True)
        # materials.rename(columns={'en': 'number'}, inplace=True)
        dist_loads.rename(columns={'number': 'en'}, inplace=True)

        mqn = pd.read_sql("SELECT * from mqn WHERE user_id='" + user+ "'", engine)
        group = mqn.groupby('number').apply(lambda x: x.to_json(orient='records'))
        return nodes.to_json(orient='table', index=False) + '|' + elements.to_json(orient='table',
                                                                                   index=False) + '|' + point_loads.to_json(
            orient='table', index=False)+ '|' + dist_loads.to_json(orient='table', index=False)+ '|' + materials.to_json(orient='table', index=False)+ '|' + sections.to_json(orient='table', index=False)+ '|' + group.to_json(orient='table', index='False')


@app.route('/readDXF', methods=['GET', 'POST'])
def readDXF():
    from dxf_import import dxf_import
    from io import StringIO
    if request.method == 'POST':
        fl = (request.get_data()).decode('UTF-8')
        stream = StringIO(fl)
        dxf = dxfgrabber.read(stream)
        nod, elm = dxf_import(dxf)
        user = session['username']

        return nod.to_json(orient='table') + '|' + elm.to_json(orient='table')
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
            session['logged_in'] = True
            session['username'] = username
            password = result.password

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('editor'))
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


# yellow save
@app.route('/save', methods=["GET", "POST"])
def save():
    if request.method == 'POST':
        data = request.get_json()

        user_id = session['username']
        elements, nodes, point_loads, sections, materials, dist_loads = parser(user_id, data, engine)

        save_db(user_id, engine, elements=elements, nodes=nodes, point_loads=point_loads, sections=sections, materials=materials, dist_loads=dist_loads)
    return render_template('editor.html')


# yellow save
@app.route('/autosave', methods=["GET", "POST"])
def autosave():
    if request.method == 'POST':
        print('yellooooow')
        # engine = create_engine('mysql+pymysql://bucketuser:dencopc@localhost/bucketlist')
        data = request.get_json()
        user_id = session['username']
        elements, nodes, point_loads, sections, materials, dist_loads = parser(user_id, data, engine)
        save_db(user_id, engine, elements=elements, nodes=nodes, point_loads=point_loads, sections=sections, materials=materials, dist_loads=dist_loads)



@app.route('/yellow', methods=["GET", "POST"])
def run_analysis():
    if request.method == 'POST':
        data = request.get_json()
        user_id = session['username']
        main(user_id, engine)

        # get results
        mqn = pd.read_sql("SELECT * from mqn WHERE user_id='" + user_id + "'", engine)
        group = mqn.groupby('number')
        elements_results = {}
        for index, g in group:
            elements_results[index] = {'x': list(g.x.get_values()),
                                       'Fx': list(g.Fx.get_values()),
                                       'Fy': list(g.Fy.get_values()),
                                       'Fz': list(g.Fz.get_values()),
                                       'Mx': list(g.Fx.get_values()),
                                       'My': list(g.Fy.get_values()),
                                       'Mz': list(g.Fz.get_values())}

        displacements = pd.read_sql("SELECT * from displacements WHERE user_id='" + user_id + "'", engine)
        group = displacements.groupby('number')

        displacements_results = {}
        for index, g in group:
            displacements_results[index] = {'x': list(g.x.get_values()),
                                            'uy': list(g.uy.get_values()),
                                            'uz': list(g.uz.get_values())}


    return jsonify({'mqn': elements_results, 'displ' : displacements_results}) #jsonify(elements_results)+ '|' + jsonify(displacements_results)
    #render_template('editor.html')



@app.route('/getReactions', methods=["POST"])
def get_reactions():
    if request.method == 'POST':
        data = pd.DataFrame(columns=['nn', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
        user_id = session['username']
        #reactions = pd.read_sql("SELECT * from reactions WHERE user_id='" + user_id + "'", engine)
        mqn = pd.read_sql("SELECT * from mqn WHERE user_id='" + user_id + "'", engine)
        print(mqn.to_json(orient='table', index=False))
        print('')
        print('alooooo')
    return mqn.to_json(orient='table', index=False)


if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True)
