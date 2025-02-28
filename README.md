# Intruder Alert System

This Python script monitors failed login attempts on a Windows system. If an unauthorized login attempt is detected, it captures an image using the webcam, sends an email alert with the image attached, and then deletes the image.

## Features
- Monitors **Windows Event Logs** for failed login attempts.
- Captures an image of the intruder using **OpenCV**.
- Sends an email notification with the captured image as an attachment.
- Deletes the captured image after mailing.
- Runs in an infinite loop to continuously monitor failed login attempts.
- Can be set up to run automatically on system startup.

## Requirements
- Windows OS (since it relies on Windows Event Logs)
- A webcam for capturing images
- A Gmail account with **App Password** enabled
- Install the libraries opencv-python and pywin32
