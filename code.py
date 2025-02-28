import cv2
import smtplib
import os
import time
import win32evtlog
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def check_failed_logins():
    server = "Security"
    hand = win32evtlog.OpenEventLog(None, server)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    
    for event in events:
        if event.EventID == 4625:
            return True
    return False

# Function to capture image
def capture_image():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    if ret:
        timestamp = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
        image_path = f"Intruder_{timestamp}.jpg"
        cv2.imwrite(image_path, frame)
        print(f"Image captured: {image_path}")
        camera.release()
        cv2.destroyAllWindows()
        return image_path
    return None

def send_email(image_path):
    sender_email = "sender@gmail.com"
    receiver_email = "receiver@gmail.com"
    password = ""  # App password of sender email

    subject = "Someone's trying to open your PC!"
    body = "Someone tried to login to your laptop.\nTime: " + datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(image_path)}")
            msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully with the image!")
    except Exception as e:
        print("Error:", e)

print("Monitoring failed login attempts...")

while True:
    if check_failed_logins():
        print("Unauthorized login attempt detected!")
        image_path = capture_image()
        send_email(image_path)
        time.sleep(60)
    else:
        time.sleep(5)
