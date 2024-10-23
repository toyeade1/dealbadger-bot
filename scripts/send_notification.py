import os
from dotenv import load_dotenv
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

def send_notification_sms(message):
    url = "https://textbelt.com/text"
    data = {
        "message": message,
        "phone": os.getenv('PHONE'),
        "key": os.getenv('SMS_API_KEY')
    }
    response = requests.post(url, data)
    return response.json()


def send_notification_email(message):
    try: 
        email = os.getenv('EMAIL')
        password = os.getenv('EMAIL_PASSWORD')

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = "Arbitrage Opportunity"

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)

        text = msg.as_string()
        server.sendmail(email, email, text)

        server.quit()

        return {"success": True}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


