from flask import Flask, render_template, request, redirect, session
import time
import smtplib
import random
from email.mime.text import MIMEText
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret-key'
# === Basic Config ===
# valid_users = {
#     'admin': '123456',
#     'Kitty': '234567'
# }

# Email settings (Gmail example)
EMAIL_SENDER = "zhengzhuowang030128@gmail.com"
EMAIL_PASSWORD = "hqrlbntcleoyvrzx"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# User email map
# user_emails = {
#     "admin": "uceez14@ucl.ac.uk",
#     "Kitty": "uceez14@ucl.ac.uk"
# }

# Login attempt limitation
login_attempts = {}
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 600  # 10 minutes

# MFA verification code store
mfa_codes = {}  # {username: {code: '123456', expires: timestamp}}
MFA_EXPIRE_SECONDS = 60

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password, email FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"password": result[0], "email": result[1]}
    return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ip_address = request.remote_addr
        track_key = f"{ip_address}_{username}"
        current_time = time.time()

        # Lock check
        if track_key in login_attempts:
            record = login_attempts[track_key]
            # 如果还在10分钟窗口内
            if current_time - record['first_attempt_time'] < LOCKOUT_TIME:
                if record['attempts'] >= MAX_ATTEMPTS:
                    remaining = int(LOCKOUT_TIME - (current_time - record['first_attempt_time']))
                    return render_template("login.html", error=f"Account locked. Try again in {remaining} seconds."), 429
            else:
                # 超过时间窗口，重置
                login_attempts[track_key] = {'attempts': 0, 'first_attempt_time': current_time}

        # 验证用户名和密码
        user = get_user(username)
        if user and user["password"] == password:
            session['pending_user'] = username

            code = f"{random.randint(100000, 999999)}"
            mfa_codes[username] = {"code": code, "expires": current_time + MFA_EXPIRE_SECONDS}

            recipient = user["email"]
            if recipient:
                send_verification_email(recipient, code)
                return redirect('/verify_mfa')
            else:
                return "No email configured for this user.", 500



        # 登录失败逻辑
        if track_key not in login_attempts:
            login_attempts[track_key] = {'attempts': 1, 'first_attempt_time': current_time}
        else:
            login_attempts[track_key]['attempts'] += 1

        record = login_attempts[track_key]
        if record['attempts'] >= MAX_ATTEMPTS and current_time - record['first_attempt_time'] < LOCKOUT_TIME:
            return render_template("login.html", error="Too many failed attempts. Account locked for 10 minutes."), 429
        else:
            left = MAX_ATTEMPTS - record['attempts']
            return render_template("login.html", error=f"Invalid credentials. {left} attempts left."), 401

    return render_template("login.html")


@app.route('/verify_mfa', methods=['GET', 'POST'])
def verify_mfa():
    if 'pending_user' not in session:
        return redirect('/')

    username = session['pending_user']
    if request.method == 'POST':
        input_code = request.form['code']
        code_info = mfa_codes.get(username)

        if code_info and time.time() < code_info['expires'] and input_code == code_info['code']:
            session.pop('pending_user')
            session['user'] = username
            mfa_codes.pop(username, None)
            return redirect('/home')
        else:
            return render_template("verify_mfa.html", error="Invalid or expired verification code.")

    return render_template("verify_mfa.html")


@app.route("/home")
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template("home.html", username=session['user'])



def send_verification_email(to_email, code):
    subject = "Your Login Verification Code"
    body = f"Your verification code is: {code}"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)


if __name__ == '__main__':
    app.run(debug=True)