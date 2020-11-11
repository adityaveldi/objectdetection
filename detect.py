from flask import Flask, redirect, url_for, session, render_template, request, jsonify, make_response, Response
from authlib.integrations.flask_client import OAuth
import os
import smtplib
from datetime import timedelta
import random
import object_detection_webcam

app=Flask(__name__)

#Oauth configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="yours Secret ID",
    client_secret="yours secret KEY",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)

# Session config
app.secret_key = "asadfnaksdjhf"
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


@app.route('/display')
def display():
    email = dict(session)['profile']['email']
    print(email)
    if email:
        return render_template('select.html')
    return f'Hello, you are logged in as {email}!'

# If Clicks on the Google Api signin
@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

# To authorize through google api
@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/display')

@app.route('/video_feed')
def video_feed():
    print('control is in this function')
    return Response(object_detection_webcam.video(),mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/select')
def select():
    return render_template('select.html')
@app.route('/click')
def click():
    return render_template('click.html')

@app.route('/final')
def final():
    return render_template('final.html')

if __name__=='__main__':
    app.run()
