import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP server configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587  # For TLS
sender_email = "redhatdivesh@gmail.com"  # Replace with your email address
receiver_email = "runadiveshjha@gmail.com"  # Replace with your friend's email address
password = "Redhat@123#!"  # Use App Password if 2FA is enabled

# Email content
subject = "Test"
body = "test email"

# Set up the MIME
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attach the body with the msg instance
message.attach(MIMEText(body, "plain"))

try:
    # Set up the server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, password)  # Login to your email account
        text = message.as_string()  # Convert the message to string
        server.sendmail(sender_email, receiver_email, text)  # Send the email
        print("Email sent successfully!")

except Exception as e:
    print(f"Error: {e}")

