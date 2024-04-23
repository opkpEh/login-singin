from flask import Flask, redirect, render_template, url_for, request, flash
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")
db = client['users']
collections = db['data']

app = Flask(__name__)

app.secret_key = 'test123'


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        username = request.form.get('username')
        femail = request.form.get('femail')
        fpass = request.form.get('fpass')

        user_data = {'username': username, 'email': femail, 'fpass': fpass}
        collections.insert_one(user_data)

        return redirect(url_for('home'))

    return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        first_name = request.form.get('fname')
        last_name = request.form.get('lname')

        user = collections.find_one({'first_name': first_name, 'last_name': last_name})

        if user:
            flash('Logged in successfully!')
            user_data = user
            return render_template("index.html")

        else:
            flash('User not found')
            return render_template("sign_up.html")

    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)
