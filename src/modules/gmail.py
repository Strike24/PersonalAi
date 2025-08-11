# This module is used to send emails through Gmail using the Gmail API.
#Command: gmail send [to] [subject] [body]
#Command: gmail send_with_attachment [to] [subject] [body] [attachment_path]
#Command: gmail get [count] - Get the last (count) emails

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
# Note: If you get "insufficient authentication scopes" error after adding new scopes,
# delete src/utils/gmail_token.json to force re-authentication with new permissions.
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']

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

def get_emails(service, count=10):
    """Get the last (count) emails from the inbox."""
    try:
        # Get list of messages from inbox only
        results = service.users().messages().list(userId='me', maxResults=count, labelIds=['INBOX']).execute()
        messages = results.get('messages', [])
        
        if not messages:
            return "No emails found."
        
        email_list = []
        for message in messages:
            # Get full message details
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = format_email_data(msg)
            email_list.append(email_data)
        
        return format_email_list(email_list)
    
    except HttpError as error:
        if "insufficientPermissions" in str(error) or "insufficient authentication scopes" in str(error):
            # Delete the token file to force re-authentication
            token_path = 'src/utils/gmail_token.json'
            if os.path.exists(token_path):
                os.remove(token_path)
                return ("Insufficient permissions detected. The authentication token has been cleared. "
                       "Please run the Gmail get command again to re-authenticate with the required permissions.")
            else:
                return ("Insufficient permissions. Please ensure you have the required Gmail scopes and "
                       "re-authenticate by running the command again.")
        return f"An error occurred while fetching emails: {error}"
    except Exception as e:
        return f"Failed to get emails: {str(e)}"

def format_email_data(message, truncate=True):
    """Format email data for display.

    Args:
        message: Gmail API message resource.
        truncate: When True, trims body to a short preview.
    """
    payload = message.get('payload', {}) if isinstance(message, dict) else {}
    headers = payload.get('headers', []) if isinstance(payload, dict) else []

    # Extract relevant headers
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
    date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')

    # Extract body text
    body = extract_body(payload)
    if truncate and len(body) > 200:
        body = body[:200] + '...'

    return {
        'id': message.get('id', ''),
        'subject': subject,
        'from': sender,
        'date': date,
        'body': body
    }

def extract_body(payload):
    """Extract body text from email payload.

    Prefers text/plain; falls back to text/html if needed. Handles nested parts recursively.
    """
    def decode_part(part):
        try:
            data = part.get('body', {}).get('data')
            if not data:
                return ""
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')
        except Exception as e:
            return f"[Decode error: {str(e)}]"

    def walk(p):
        # If this part has subparts, walk them first
        if 'parts' in p and isinstance(p['parts'], list):
            text_plain = ""
            text_html = ""
            for sub in p['parts']:
                content = walk(sub)
                mt = sub.get('mimeType', '')
                if mt == 'text/plain' and not text_plain:
                    text_plain = content
                elif mt == 'text/html' and not text_html:
                    text_html = content
            return text_plain or text_html or ""
        # Leaf part
        mt = p.get('mimeType', '')
        if mt == 'text/plain':
            return decode_part(p)
        if mt == 'text/html':
            return decode_part(p)
        return ""

    try:
        # Try direct body first
        direct = walk(payload)
        if direct:
            return direct
    except Exception as e:
        return f"[Could not extract body: {str(e)}]"

    return "[No body content]"

def format_email_list(emails):
    """Format list of emails for display."""
    result = f"Found {len(emails)} emails:\n\n"
    
    for i, email in enumerate(emails, 1):
        result += f"Email #{i}:\n"
        result += f"  Subject: {email['subject']}\n"
        result += f"  From: {email['from']}\n"
        result += f"  Date: {email['date']}\n"
        result += f"  Preview: {email['body']}\n"
        result += f"  ID: {email['id']}\n"
        result += "-" * 50 + "\n"
    
    return result

def format_single_email(email):
    """Format a single email with full content for display."""
    result = []
    result.append(f"Subject: {email['subject']}")
    result.append(f"From: {email['from']}")
    result.append(f"Date: {email['date']}")
    result.append(f"ID: {email['id']}")
    body_text = email.get('body') or ""
    result.append("Body:\n" + body_text)
    return "\n".join(result)

def get_email_by_id(service, email_id):
    """Retrieve a specific email by its Gmail message ID and return full content."""
    try:
        msg = service.users().messages().get(userId='me', id=email_id, format='full').execute()
        email = format_email_data(msg, truncate=False)
        return format_single_email(email)
    except HttpError as error:
        if error.resp is not None and getattr(error.resp, 'status', None) == 404:
            return f"Email not found for id: {email_id}"
        return f"An error occurred while fetching the email: {error}"
    except Exception as e:
        return f"Failed to get email: {str(e)}"

def execute(args):
    if args is None or len(args) == 0:
        return "No command provided."
    
    action = args.get("action", "").lower()
    
    # Authenticate Gmail
    service, error = authenticate_gmail()
    if error:
        return error
    
    if action == "send":
        # Send regular email
        to = args.get("to")
        subject = args.get("subject", "")
        body = args.get("body", "")
        
        if not to:
            return "No recipient email address provided."
        
        message = create_message(to, subject, body)
        return send_message(service, message)
    
    elif action == "send_with_attachment":
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
    
    elif action in ("get_by_id", "get_id"):
        # Get specific email by ID
        email_id = args.get("id") or args.get("email_id")
        if not email_id:
            return "No email id provided."
        return get_email_by_id(service, email_id)
    elif action == "get":
        # Get emails
        count = args.get("count", 10)  # Default to 10 emails
        
        # Ensure count is an integer
        try:
            count = int(count)
            if count <= 0:
                count = 10
        except (ValueError, TypeError):
            count = 10
        return get_emails(service, count)
    
    else:
        return f"Unknown Gmail action: {action}. Available actions: send, send_with_attachment, get, get_by_id"
