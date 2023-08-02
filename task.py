import os
import requests
from dotenv import  load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")


def send_simple_message(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "Excited Hoang Viet <mailgun@YOUR_DOMAIN_NAME>",
              "to": [to],
              "subject": subject,
              "text": body})


def send_user_registration(email, username):
    return  send_simple_message(
        email,
        "Successfully Signed Up",
        f"Hi {username}"
    )