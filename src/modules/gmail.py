# This module is used to send emails through Gmail using the Gmail API.
#Command: gmail send [to] [subject] [body]
#Command: gmail send_with_attachment [to] [subject] [body] [attachment_path]

import os
import base64
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# --- Environment Setup ---
load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    """Authenticate and return Gmail service object."""
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('src/utils/gmail_token.json'):
        creds = Credentials.from_authorized_user_file('src/utils/gmail_token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # You need to download credentials.json from Google Cloud Console
            if os.path.exists('src/utils/gmail_credentials.json'):
                flow = InstalledAppFlow.from_client_secrets_file(
                    'src/utils/gmail_credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            else:
                return None, "gmail_credentials.json file not found. Please download it from Google Cloud Console."

        # Save the credentials for the next run
        with open('src/utils/gmail_token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service, None
    except Exception as e:
        return None, f"Failed to build Gmail service: {str(e)}"

def create_message(to, subject, body, attachment_path=None):
    """Create a message for an email."""
    if attachment_path:
        message = MIMEMultipart()
    else:
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    
    message['to'] = to
    message['subject'] = subject
    
    # Add body
    message.attach(MIMEText(body, 'plain'))
    
    # Add attachment if provided
    if attachment_path and os.path.exists(attachment_path):
        content_type, encoding = mimetypes.guess_type(attachment_path)
        
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        
        main_type, sub_type = content_type.split('/', 1)
        
        with open(attachment_path, 'rb') as fp:
            attachment = MIMEBase(main_type, sub_type)
            attachment.set_payload(fp.read())
        
        encoders.encode_base64(attachment)
        
        filename = os.path.basename(attachment_path)
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}',
        )
        message.attach(attachment)
    
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, message):
    """Send an email message."""
    try:
        message = service.users().messages().send(userId="me", body=message).execute()
        return f"Message sent successfully. Message ID: {message['id']}"
    except HttpError as error:
        return f"An error occurred: {error}"
    except Exception as e:
        return f"Failed to send message: {str(e)}"

def execute(args):
    if args is None or len(args) == 0:
        return "No command provided."
    
    action = args.get("action", "").lower()
    
    # Authenticate Gmail
    service, error = authenticate_gmail()
    if error:
        return error
    
    if "send" in action and "attachment" not in action:
        # Send regular email
        to = args.get("to")
        subject = args.get("subject", "")
        body = args.get("body", "")
        
        if not to:
            return "No recipient email address provided."
        
        message = create_message(to, subject, body)
        return send_message(service, message)
    
    elif "send_with_attachment" in action or "attachment" in action:
        # Send email with attachment
        to = args.get("to")
        subject = args.get("subject", "")
        body = args.get("body", "")
        attachment_path = args.get("attachment_path")
        
        if not to:
            return "No recipient email address provided."
        
        if not attachment_path:
            return "No attachment path provided."
        
        if not os.path.exists(attachment_path):
            return f"Attachment file not found: {attachment_path}"
        
        message = create_message(to, subject, body, attachment_path)
        return send_message(service, message)
    
    else:
        return f"Unknown Gmail action: {action}. Available actions: send, send_with_attachment"
