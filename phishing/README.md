Email phishing attack and defense  
Attack: run app.py, then run email_sending.py (The target mailbox in this file can be modified)  
You will receive an email with a link. If you click on it, you will be directed to an interface the same as the normal login interface  
Defense: Modify the email account and dedicated password in email_filter.py(here we use gmail as an example)and then run. The suspicious link will be added to the blacklist.db
Note that: if you want to train the URL classifer, please put the database_email filter.py under the defence folder.
