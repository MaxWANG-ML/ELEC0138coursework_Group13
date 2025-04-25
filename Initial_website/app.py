from flask import Flask, render_template, request, redirect, session
import sqlite3
#username = Kitty
#password = 234567
app = Flask(__name__)
app.secret_key = 'secret-key'

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_password = get_user(username)
        if user_password and user_password == password:
            session['user'] = username
            return redirect('/home')  
        else:
            return render_template('login.html', error="incorrect username or password")
    return render_template('login.html')

@app.route("/home")
def home():
    username = request.args.get("username")
    role = request.args.get("role")
    return render_template("home.html", username=username, role=role)

@app.route("/view_employee")
def view_employee():
    return "Viewing Employee Information"

@app.route("/view_manager")
def view_manager():
    return "Viewing Manager Information"

if __name__ == '__main__':
    app.run(debug=True)
