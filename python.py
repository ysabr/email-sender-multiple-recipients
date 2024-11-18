import smtplib
from email.message import EmailMessage
import os
import time
def send_emails(smtp_server, smtp_port, sender_email, sender_password, recipients_file, subject, body, attachments, delay):
    # Read recipients from file
    try:
        with open(recipients_file, 'r') as file:
            recipients = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Recipients file not found!")
        return

    # Setup SMTP connection
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
    except Exception as e:
        print("Failed to connect to SMTP server:", e)
        return

    for recipient in recipients:
        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient
            msg.set_content(body)

            for attachment in attachments:
                if os.path.isfile(attachment):
                    with open(attachment, 'rb') as f:
                        file_data = f.read()
                        file_name = os.path.basename(attachment)
                        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
                else:
                    print(f"Attachment {attachment} not found, skipping.")

            server.send_message(msg)
            print(f"Email sent successfully to {recipient}")
            time.sleep(delay)
        except Exception as e:
            print(f"Failed to send email to {recipient}: {e}")

    server.quit()

# Configuration
smtp_server = 'smtp.gmail.com'  # Correct SMTP server for Gmail
smtp_port = 587
sender_email = 'youssefsabr57@gmail.com'
sender_password = 'your_password'  # Replace with your app-specific password
recipients_file = 'emails.txt'
subject = 'Application for Software Engineering Internship'
body = '''
Dear Hiring Team,

I hope this message finds you well. Attached is my resume and cover letter. I am very interested in applying for the software engineering internship position and would love the opportunity to contribute to your team.

Please let me know if you need any further information.

Best regards,
Youssef Sabr
'''
attachments = ['resume_software_engineer.pdf', 'Cover_letter.pdf']
delay = 120
# Send emails
send_emails(smtp_server, smtp_port, sender_email, sender_password, recipients_file, subject, body, attachments, delay)
