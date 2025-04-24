
from flask import Flask, render_template, request, redirect, session
import time
import sqlite3

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

login_attempts = {}

MAX_ATTEMPTS = 5
LOCKOUT_TIME = 300  # 5 minutes

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        ip_address = request.remote_addr
        track_key = f"{ip_address}_{username}"

        current_time = time.time()
        if track_key in login_attempts:
            if login_attempts[track_key]["attempts"] >= MAX_ATTEMPTS:
                if current_time - login_attempts[track_key]["timestamp"] < LOCKOUT_TIME:
                    remaining_time = int(LOCKOUT_TIME - (current_time - login_attempts[track_key]["timestamp"]))
                    return render_template("login.html",
                                           error=f"Account locked. Try again in {remaining_time} seconds."), 429
                else:
                    login_attempts[track_key] = {"attempts": 0, "timestamp": current_time}

        user_password = get_user(username)
        if user_password and user_password == password:
            session['user'] = username
            if track_key in login_attempts:
                login_attempts[track_key] = {"attempts": 0, "timestamp": current_time}
            return redirect('/home')
        else:
            if track_key not in login_attempts:
                login_attempts[track_key] = {"attempts": 1, "timestamp": current_time}
            else:
                login_attempts[track_key]["attempts"] += 1
                login_attempts[track_key]["timestamp"] = current_time

            if login_attempts[track_key]["attempts"] >= MAX_ATTEMPTS:
                response = render_template("login.html",
                                           error=f"Too many failed attempts. Account locked for {LOCKOUT_TIME // 60} minutes.")
                return response, 429
            else:
                remaining_attempts = MAX_ATTEMPTS - login_attempts[track_key]["attempts"]
                return render_template("login.html",
                                       error=f"Invalid username or password. {remaining_attempts} attempts left."), 401
    return render_template('login.html')

@app.route("/home")
def home():
    if 'user' not in session:
        return redirect('/')

    username = request.args.get("username")
    role = request.args.get("role")

    return render_template("home.html", username=username, role=role)

@app.route("/view_employee")
def view_employee():
    if 'user' not in session:
        return redirect('/')

    return "Viewing Employee Information"

@app.route("/view_manager")
def view_manager():
    if 'user' not in session:
        return redirect('/')

    return "Viewing Manager Information"

@app.route("/login_attempts")
def view_login_attempts():
    if "user" not in session:
        return redirect("/")

    current_time = time.time()
    active_locks = {}

    for key, data in login_attempts.items():
        if data["attempts"] >= MAX_ATTEMPTS and current_time - data["timestamp"] < LOCKOUT_TIME:
            time_left = int(LOCKOUT_TIME - (current_time - data["timestamp"]))
            active_locks[key] = {
                "attempts": data["attempts"],
                "time_left": time_left
            }

    return render_template("login_attempts.html", active_locks=active_locks, all_attempts=login_attempts)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
