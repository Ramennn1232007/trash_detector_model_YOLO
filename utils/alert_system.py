import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables for Twilio credentials
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
RECIPIENT_NUMBER = os.getenv("RECIPIENT_NUMBER")

# Initialize the Twilio client with the correct variables
client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_whatsapp_alert(message):
    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=RECIPIENT_NUMBER
        )
        print(f"WhatsApp message sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")

def check_trash_threshold(current_count):
    if current_count >= int(os.getenv("TRASH_THRESHOLD", 5)):  # Get threshold from env or use default
        send_whatsapp_alert(f"Alert: The trash collector has detected {current_count} item(s) of trash.")
        return True
    return False