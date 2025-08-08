import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

def get_techcrunch_headlines():
    url = 'https://techcrunch.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('a', class_='post-block__title__link', limit=3)
    return [f"{h.get_text(strip=True)}\n{h['href']}" for h in headlines]

def send_email(subject, body):
    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECIPIENT")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)

if __name__ == "__main__":
    headlines = get_techcrunch_headlines()
    body = "\n\n".join(headlines)
    subject = f"Top TechCrunch Headlines - {datetime.now().strftime('%Y-%m-%d')}"
    send_email(subject, body)
