from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a secure random key in production

oauth = OAuth(app)
oauth.register(
    name='oidc',
    authority='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_oMzrCDluY',
    client_id='3d1a60lu6thi31glo11h0gkgbg',
    client_secret='<client secret>',
    server_metadata_url='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_oMzrCDluY/.well-known/openid-configuration',
    client_kwargs={'scope': 'phone openid email'}
)

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f'Hello, {user["email"]}. <a href="/logout">Logout</a>'
    else:
        return f'Welcome! Please <a href="/login">Login</a>.'

@app.route('/login')
def login():
    return oauth.oidc.authorize_redirect('https://d84l1y8p4kdic.cloudfront.net')

@app.route('/authorize')
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = token['userinfo']
    session['user'] = user
    return redirect(url_for('upload'))  # Redirecting to upload page after login

@app.route('/upload')
def upload():
    return "Welcome to the Upload Page! Here you can upload your files."

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)