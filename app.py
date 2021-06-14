import os
import requests
from flask import Flask, request, render_template, abort, redirect, session

app = Flask(__name__)

app.secret_key = str(os.urandom(16))

api_key = os.getenv("API_KEY")


@app.route("/admin/products")
def admin_products():
    session["api_key"] = api_key
    if session.get("api_key", "") == api_key or True:
        try:
            response = requests.get("http://127.0.0.1:5005/product", headers={"API-Key": session.get("api_key")})

        except requests.exceptions.ConnectionError:
            abort(503)
            
        if response.status_code != 200:
            abort(503)

        response = response.json()

        if response["code"] == 403:
            return redirect("/admin")
        
        return render_template("admin_products.html", products=response["products"], api_key=session.get("api_key"))

    else:
        return redirect("/admin")


@app.route("/admin")
def home():
    return "hello world"


if __name__ == '__main__':
    app.run()
