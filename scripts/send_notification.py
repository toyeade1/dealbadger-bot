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
        email2 = os.getenv('EMAIL2')
        password = os.getenv('EMAIL_PASSWORD')

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email2
        msg['Subject'] = "Arbitrage Opportunity"

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.zoho.com', 587)
        server.starttls()
        server.login(email, password)

        text = msg.as_string()
        server.sendmail(email, email2, text)

        server.quit()

        return {"success": True}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

# def send_notification_email(message):
#     message = Mail(
#         from_email=os.getenv('EMAIL'),
#         to_emails=os.getenv('EMAIL'),
#         subject='Arbitrage Opportunity',
#         html_content=message)
#     try:
#         sg = SendGridAPIClient(os.getenv('EMAIL_API_KEY'))
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         return {"success": True}
#     except Exception as e:
#         return {"success": False, "error": str(e)}
    

# exmaple usage
print(send_notification_email("Hello from DealBadger!"))