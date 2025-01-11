#%%

import os
from flask import Flask, redirect, Response, session, url_for
import subprocess
import _google_oauth
import _tools


app = Flask(__name__)
app.secret_key = os.urandom(42)
app.register_blueprint(_google_oauth.gauth_bp)

AUTHORIZED_USERS = os.getenv('AUTHORIZED_USERS', '*')
GIT_BRANCH = os.getenv('GIT_BRANCH', 'main')


#%% Flask App
    
@app.route('/home')
def home():
    return redirect('/')


@app.route('/auth_verify')
def auth_verify():
    if session.get("user_logged_in"):
        return Response(status=200)
    if 'user_email' in session:
        if _tools.check_authorized_user(authorized_users=AUTHORIZED_USERS):
            return Response(status=200)
        return Response(status=403)
    return Response(status=401)


@app.route('/unauthorized')
def unauthorized():
    return 'Yikes, looks like you are unauthorized!', 403


@app.route('/git_pull', methods=['GET'])
def git_pull():
    if _tools.check_authorized_user(authorized_users=AUTHORIZED_USERS):
        os.chdir('/app/git_repo')
        command = ["git", "fetch", "origin", f"{GIT_BRANCH}"]
        subprocess.call(command)
        command = ["git", "reset", "--hard", f"origin/{GIT_BRANCH}"]
        subprocess.call(command)
        command = ["pip", "install", "-r", "requirements.txt"]
        subprocess.call(command)
        return 'Boom, done!', 200
    return redirect(url_for('unauthorized'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)


#%%