import requests
import smtplib
from dotenv import load_dotenv, dotenv_values
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

def send_notification_sms(message):
    url = "https://textbelt.com/text"
    data = {
        "message": message,
        "phone": dotenv_values('.env')['PHONE'],
        "key": dotenv_values('.env')['SMS_API_KEY']
    }
    response = requests.post(url, data)
    return response.json()


def send_notification_email(message):
    try: 
        email = dotenv_values('.env')['EMAIL']
        password = dotenv_values('.env')['EMAIL_PASSWORD']

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


