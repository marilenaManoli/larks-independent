# from flask import request, render_template, flash, redirect, url_for
import werkzeug
from flask import Flask, render_template, Response, request, flash, redirect, url_for, session, jsonify
from app import app, models, bcrypt, db
import datetime
import time
import os
import sys
import json
import base64
# import numpy as np
from threading import Thread
from .models import User_Login, User_Login_Test
from .forms import LoginForm, RegisterForm  # for testing login and register
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta, timezone

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "comp3931-larks"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

#############################################################
# BEGINNING OF GLOBAL VARIABLES
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# keeps track of whether we are in testing mode, passed to functions that want to have different behaviour when testing
testing = False # default should be False, explictly change to True whenever you want to run in Test mode

#############################################################
# BEGINNING OF HTTP ERROR HANDLERS
# ^^^^^^^^^^^^^^^^^^^^^^^

#############################################################
# REGISTER 400 ERROR
# ^^^^^^^^^^^^^^^^^^^^^^^
# HTTP Error for bad request is specifically No. 400


@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
def handle_bad_request(e):
    # Need to figure out how to request the "400Error" page on the React frontend
    return 'bad request!', 400

#############################################################
# GETTER AND SETTER METHODS
# ^^^^^^^^^^^^^^^^^^^^^^^


def set_testing(setting):
    if (bool(setting)):
        testing = setting
    return testing


def get_testing():
    return testing

#############################################################
# ROUTE FOR LANDING PAGE
# ^^^^^^^^^^^^^^^^^^^^^^^


@app.route('/', methods=['GET', 'POST'])
def index():
    response = {"Larks App": "Welcome"}
    return jsonify(response)


############################################################
# ROUTE FOR LOGIN - FOR TESTING
# ^^^^^^^^^^^^^^^^^^^^^^^
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        print("Request is POST!")
        print(request.data)
        # to convert byte data into utf characters
        data = json.loads(request.data.decode('utf-8'))

        print(data)
        print(data.get('credentials'))

        # flash(request)
        # return {"type": "POST"}
        if (testing):
            u = models.User_Login_Test.query.filter_by(
                email=data['credentials']['email']).first()
        else:
            u = models.User_Login.query.filter_by(
                email=data['credentials']['email']).first()
        # check username and password
        if u:
            if bcrypt.check_password_hash(u.password, data['credentials']['password']):
                # response = {"token": "test123"}
                print('Login Successful!', 'success')
                access_token = create_access_token(
                    identity=data['credentials']['email'])
                print(access_token)
                response = {"token": access_token}
                return jsonify(response), 200
            else:
                print("Wrong Password")
                response = {"msg": "Bad Password"}
                return jsonify(response), 401

        else:
            print("Wrong username")
            response = {"msg": "Bad Username"}
            return jsonify(response), 401

    elif request.method == "GET":
        return {"type": "GET"}, 405
    else:
        # app.logger.info(u.email + " unsuccesfull login at " + now)
        flash(f'Login unsuccessful. Please check email and password', 'danger')
        print(f'Login unsuccessful. Please check email and password!')
        response = {"msg": "Login unsuccessful"}
        return jsonify(response), 401


############################################################
# ROUTE FOR REGISTER - FOR TESTING
# ^^^^^^^^^^^^^^^^^^^^^^^
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        print("Request is post")
        print(request.data)
        data = json.loads(request.data.decode('utf-8'))
        print(data['email'])
        if (testing):
            username_database_check = models.User_Login_Test.query.filter_by(
                email=data['email']).first()
        else:
            username_database_check = models.User_Login.query.filter_by(
                email=data['email']).first()
        if username_database_check:
            print("Username already exists!")
            return {"msg": "Username taken"}, 401
        else:
            print("Valid!")
            hashed_password = bcrypt.generate_password_hash(
                data['password']).decode('utf-8')
            # check if we're in testing mode
            if (testing):
                new_user = User_Login_Test(
                    email=data['email'], password=hashed_password)
            else:
                new_user = User_Login(
                    email=data['email'], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return {"msg": "New User Added!"}, 200


#############################################################
# ROUTE SIMPLY PROVIDING A PROOF OF CONCEPT OF UPLOADING IMAGES TO SERVER
# CURRENTLY SAVES IMAGE TO SHOTS FOLDER, BUT I IMAGINE WE DONT WANT TO DO THAT AND ONLY WANT TO PROCESS IMAGES
# ^^^^^^^^^^^^^^^^^^^^^^^
@app.route('/upload', methods=['POST'])
def upload():
    image = request.form['image']
    # if frontend sends no image return error
    if image == "null":
        return {"msg": "No image sent!"}, 415

    # removes header of base 64 encoded string i.e. first 22 chars and decodes the rest
    image = image[22:]
    image_decoded = base64.b64decode(image)

    # gets string of curr time and names file that
    timestamp = str(int(time.time()))
    filename = timestamp+".png"

    # saves decoded base 64 string to that image
    with open(os.path.join("shots", filename), "wb") as f:
        f.write(image_decoded)
    return {"msg": "image successfully saved in server!"}, 200


#############################################################
# ROUTE FOR ALEX'S APP
# ^^^^^^^^^^^^^^^^^^^^^^^
@app.route('/alex', methods=['GET', 'POST'])
def alex():
    if request.method == 'POST':
        print("Alex App Requested")


#############################################################
# ROUTE FOR KEVIN'S APP
# ^^^^^^^^^^^^^^^^^^^^^^^
@app.route('/kevin', methods=['GET', 'POST'])
def kevin():
    if request.method == 'POST':
        print("Kevin App Requested")


#############################################################
# ROUTE FOR LANRE'S APP
# ^^^^^^^^^^^^^^^^^^^^^^^
@app.route('/lanre', methods=['GET', 'POST'])
def lanre():
    if request.method == 'POST':
        print("Lanre App Requested")


#############################################################
# ROUTE FOR RAMAT'S APP
# ^^^^^^^^^^^^^^^^^^^^^^^
@app.route('/ramat', methods=['GET', 'POST'])
def ramat():
    if request.method == 'POST':
        print("Ramat App Requested")


#############################################################
# ROUTE FOR SHREYAS' APP
# ^^^^^^^^^^^^^^^^^^^^^^^
@app.route('/shreyas', methods=['GET', 'POST'])
def shreyas():
    if request.method == 'POST':
        print("Shreyas App Requested")
