1.HTTP flooding attack and defense  
Attack: first run the local Flask server (app.py), then launch HTTP_flooding.py to simulate the attack.  
Defense: run app_http_def.py, which includes rate-limiting defense and run HTTP_flooding.py again.  
Use Wireshark to compare server responses—if 200 OK responses are limited and some are replaced by 429 Too Many Requests, the defense is effective.


2.SYN flooding attack and defense  
Attack: run the Flask server(app.py) and simulate the attack using either hping3 from a virtual machine  
or the local script SYN_flooding.py.  
Defense: run anti_ddos.py with administrator privileges to activate the defense.  
The effectiveness can be verified by checking whether the script drops connections that do not complete the TCP handshake (i.e., no ACK received).
