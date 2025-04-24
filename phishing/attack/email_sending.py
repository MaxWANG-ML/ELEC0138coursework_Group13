import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generate_phishing_link():

    return "http://ELEC0138-group13.com:5005/"

def send_phishing_email(target_email, sender_email, sender_password, smtp_server, smtp_port=587):
    phishing_link = generate_phishing_link()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Important: Your account requires verification"
    msg['From'] = sender_email
    msg['To'] = target_email

    text = f"Please click the following link to verify your account:\n{phishing_link}"
    html = f"""\
    <html>
      <head></head>
      <body>
        <p>Please <a href="{phishing_link}">click here</a> to verify your account.</p>
      </body>
    </html>
    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, target_email, msg.as_string())
        server.quit()
        print("Phishing email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)

if __name__ == "__main__":
    target_email = "chenwen_cuc@163.com"
    sender_email = "wen.chen.020328@gmail.com"
    sender_password = "qtzv afuw jeoa entc"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    send_phishing_email(target_email, sender_email, sender_password, smtp_server, smtp_port)

