import re
import email
import requests
import base64
from urllib.parse import urlparse
import sqlite3
import datetime
import imaplib
from DGA_test import DGA_detect

# Path to the database file
DB_PATH = "blacklist.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blacklist (
            domain TEXT PRIMARY KEY,
            added_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def is_domain_in_blacklist(domain):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT domain FROM blacklist WHERE domain = ?", (domain,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_domain_to_blacklist(domain):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    cursor.execute("INSERT OR IGNORE INTO blacklist (domain, added_time) VALUES (?, ?)", (domain, now))
    conn.commit()
    conn.close()

def query_virustotal(url, api_key):
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    vt_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    headers = {'x-apikey': api_key}
    response = requests.get(vt_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        stats = data['data']['attributes']['last_analysis_stats']
        if stats.get('malicious', 0) > 0 or stats.get('suspicious', 0) > 0:
            return True
    return False

def extract_urls(email_content):
    url_regex = r'(https?://[^\s]+)'
    return re.findall(url_regex, email_content)

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset() or "utf-8"
                body += part.get_payload(decode=True).decode(charset, errors="ignore")
    else:
        charset = msg.get_content_charset() or "utf-8"
        body = msg.get_payload(decode=True).decode(charset, errors="ignore")
    return body

def scan_email_for_phishing(msg, api_key, threshold=3):
    email_body = get_email_body(msg)
    urls = extract_urls(email_body)
    flagged_urls = []
    for url in urls:
        domain = urlparse(url).netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        # If the domain already exists in the database, flag it as suspicious
        if is_domain_in_blacklist(domain):
            flagged_urls.append(url)
            # print('database')
        elif query_virustotal(url, api_key):
            add_domain_to_blacklist(domain)
            flagged_urls.append(url)
            # print('virus')
        elif DGA_detect(url) == 1:
            add_domain_to_blacklist(domain)
            flagged_urls.append(url)
            # print('DGA')
    return flagged_urls

def fetch_unread_emails(imap_server, email_user, email_pass):
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_user, email_pass)
    mail.select("inbox")
    typ, data = mail.search(None, 'UNSEEN')
    email_ids = data[0].split()
    emails = []
    for e_id in email_ids:
        typ, msg_data = mail.fetch(e_id, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        emails.append(msg)
    mail.logout()
    return emails

if __name__ == "__main__":
    # Initialize the database
    init_db()

    # Replace with your own VirusTotal API key
    api_key = "f883b63eab2479d1ef0faf4ac23014da7eaab38f0eaf9e2d380b84bb86811892"

    # IMAP email configuration (e.g., for Gmail)
    imap_server = "imap.gmail.com"
    email_user = "wen.chen.020328@gmail.com"
    email_pass = "qtzv afuw jeoa entc"  # It is recommended to use an app-specific password

    # Fetch unread emails
    emails = fetch_unread_emails(imap_server, email_user, email_pass)
    print(f"Received a total of  {len(emails)}  unread email.")

    # Scan each email
    for idx, msg in enumerate(emails):
        flagged = scan_email_for_phishing(msg, api_key, threshold=3)
        if flagged:
            print(f"Email {idx+1} detected suspicious link:")
            for url in flagged:
                print("  ", url)
        else:
            print(f"Email {idx+1} did not detect any suspicious links.")
