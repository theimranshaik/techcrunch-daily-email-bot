import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

def get_techcrunch_headlines():
    url = 'https://techcrunch.com/'
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return ["Failed to fetch TechCrunch page."]

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select("h2.post-block__title a.post-block__title__link")
    headlines = []

    for link in links[:3]:
        title = link.get_text(strip=True)
        url = link.get('href')
        headlines.append(f"{title}\n{url}")
    
    if not headlines:
        return ["No headlines found. TechCrunch structure might have changed."]
    
    return headlines

def send_email(subject, body):
    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECIPIENT")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body, "plain")
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
