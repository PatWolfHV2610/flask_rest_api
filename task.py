import os
import requests
import jinja2
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")
template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(context)


def send_simple_message(to, subject, body, html):
    domain = os.getenv("MAILGUN_DOMAIN")
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "Excited Hoang Viet <mailgun@YOUR_DOMAIN_NAME>",
              "to": [to],
              "subject": subject,
              "text": body,
              "html": html})


def send_user_registration(email, username):
    return send_simple_message(
        email,
        "Successfully Signed Up",
        f"Hi {username}",
        render_template("email/action.html", username=username)
    )
