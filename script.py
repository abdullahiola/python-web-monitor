import requests
import smtplib
from email.message import EmailMessage
import time
import os

# Configurations
URL = "https://google.com"
CHECK_INTERVAL_SECONDS = 60  # how often to check
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
TO_EMAIL = "recipient@example.com"

def send_email_alert(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Email alert sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_website():
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code != 200:
            send_email_alert(
                subject=f"Website Down: {URL}",
                body=f"Status code {response.status_code} received while accessing {URL}"
            )
        else:
            print(f"Website is up. Status code: {response.status_code}")
    except requests.RequestException as e:
        send_email_alert(
            subject=f"Website Unreachable: {URL}",
            body=f"An error occurred while checking {URL}: {e}"
        )

def main():
    print(f"Monitoring {URL} every {CHECK_INTERVAL_SECONDS} seconds...")
    while True:
        check_website()
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()