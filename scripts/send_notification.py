import smtplib
from email.mime.text import MIMEText

def send_email_alert(item_name, profit_margin):
    sender = 'your_email@gmail.com'
    recipient = 'your_phone_or_email@gmail.com'
    subject = f'Arbitrage Opportunity: {item_name}'
    body = f'The item "{item_name}" has a profit margin of {profit_margin}%.'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, 'your_password')
        server.sendmail(sender, recipient, msg.as_string())

# # Example usage
# if profit_margin and profit_margin >= 30:
#     send_email_alert("ZINUS Brock Metal And Wood Platform Bed Frame", profit_margin)
