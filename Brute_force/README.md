Brute-force attack and defense simulation  
Attack: run the app.py and click the http://127.0.0.1:5005. Then run the brute_force.py to  
simulate the attack. If the password for a given name is found. The password will be displayed.  

Defense1: run the app_rate-limitation.py and the brute_force.py. When you continue to try to  
login, the account will be locked.  
Defense2: run the app_MFA and enter the correct username Kitty and password 234567, you will   
be redirected to the MFA interface. And you can change the corresponding email address for a   username in the initialise_database.py to receive an email with the verification code in real.
