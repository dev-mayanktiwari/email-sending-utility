"""
SMTP email sending with retry logic and rate limiting.
"""
import re
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from datetime import datetime

from config import SMTP_HOST, SMTP_PORT


def _html_to_plain_text(html: str) -> str:
    """Strip HTML tags to produce a plain-text fallback."""
    text = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    text = re.sub(r'</?p[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</?div[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<li[^>]*>', '\n• ', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def send_email(
    sender_email: str,
    sender_password: str,
    sender_name: str,
    recipient_email: str,
    subject: str,
    body_html: str,
    max_retries: int = 1,
    reply_to: str = "",
) -> dict:
    """
    Send a single email via SMTP.

    Returns:
        dict with keys: success (bool), error (str|None), timestamp (str)
    """
    timestamp = datetime.now().isoformat()

    for attempt in range(1 + max_retries):
        try:
            # multipart/alternative gives spam filters a plain-text version to read
            msg = MIMEMultipart('alternative')
            from_field = f"{sender_name} <{sender_email}>" if sender_name else sender_email
            msg['From'] = from_field
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg['Date'] = formatdate(localtime=True)
            domain = sender_email.split('@')[1] if '@' in sender_email else 'mailforge'
            msg['Message-ID'] = make_msgid(domain=domain)
            if reply_to:
                msg['Reply-To'] = reply_to

            plain_text = _html_to_plain_text(body_html)
            msg.attach(MIMEText(plain_text, 'plain', 'utf-8'))
            msg.attach(MIMEText(body_html, 'html', 'utf-8'))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())

            return {"success": True, "error": None, "timestamp": timestamp}

        except smtplib.SMTPResponseException as e:
            # Retry on transient SMTP errors (4xx)
            if attempt < max_retries and 400 <= e.smtp_code < 500:
                time.sleep(2)
                continue
            return {"success": False, "error": f"SMTP error {e.smtp_code}: {e.smtp_error}", "timestamp": timestamp}

        except smtplib.SMTPAuthenticationError:
            return {"success": False, "error": "Authentication failed. Check your email and app password.", "timestamp": timestamp}

        except Exception as e:
            if attempt < max_retries:
                time.sleep(2)
                continue
            return {"success": False, "error": str(e), "timestamp": timestamp}

    return {"success": False, "error": "Max retries exceeded.", "timestamp": timestamp}


def send_test_email(
    sender_email: str,
    sender_password: str,
    sender_name: str,
    subject: str,
    body_html: str,
    reply_to: str = "",
) -> dict:
    """Send a test email to the sender's own address."""
    return send_email(
        sender_email=sender_email,
        sender_password=sender_password,
        sender_name=sender_name,
        recipient_email=sender_email,
        subject=f"[TEST] {subject}",
        body_html=body_html,
        reply_to=reply_to,
    )


def test_smtp_connection(sender_email: str, sender_password: str) -> tuple[bool, str]:
    """
    Test SMTP connection and authentication without sending an email.
    Returns (success, message).
    """
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, sender_password)
        return True, "Connection successful! SMTP credentials are valid."
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Check your email and app password."
    except Exception as e:
        return False, f"Connection failed: {str(e)}"
