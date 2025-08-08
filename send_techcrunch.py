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
    
    # Find the first 3 headline blocks
    articles = soup.select('div.post-block')[:3]
    headlines = []
    
    for article in articles:
        title_tag = article.select_one('h2.post-block__title a')
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag['href']
            headlines.append(f"{title}\n{link}")
    
    return headlines

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
    if headlines:
        body = "\n\n".join(headlines)
    else:
        body = "No headlines found. TechCrunch structure might have changed."

    subject = f"Top TechCrunch Headlines - {datetime.now().strftime('%Y-%m-%d')}"
    send_email(subject, body)
