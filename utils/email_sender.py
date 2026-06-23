"""
SMTP email sending with retry logic and rate limiting.
"""

import mimetypes
import re
import smtplib
import time
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

from config import SMTP_HOST, SMTP_PORT


def _html_to_plain_text(html: str) -> str:
    """Strip HTML tags to produce a plain-text fallback."""
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"</?p[^>]*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</?div[^>]*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<li[^>]*>", "\n• ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
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
    attachments: list[dict] | None = None,
) -> dict:
    """
    Send a single email via SMTP.

    Each item in *attachments* must be a dict with:
        name (str)   — filename shown to the recipient
        data (bytes) — raw file bytes

    Returns:
        dict with keys: success (bool), error (str|None), timestamp (str)
    """
    timestamp = datetime.now().isoformat()

    for attempt in range(1 + max_retries):
        try:
            # Outer container: mixed when there are attachments, alternative otherwise
            has_attachments = bool(attachments)
            if has_attachments:
                msg = MIMEMultipart("mixed")
            else:
                msg = MIMEMultipart("alternative")

            from_field = (
                f"{sender_name} <{sender_email}>" if sender_name else sender_email
            )
            msg["From"] = from_field
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg["Date"] = formatdate(localtime=True)
            domain = sender_email.split("@")[1] if "@" in sender_email else "mailforge"
            msg["Message-ID"] = make_msgid(domain=domain)
            if reply_to:
                msg["Reply-To"] = reply_to

            # Build text/html alternative part
            plain_text = _html_to_plain_text(body_html)
            if has_attachments:
                # Nest plain+html inside a multipart/alternative sub-part
                alt_part = MIMEMultipart("alternative")
                alt_part.attach(MIMEText(plain_text, "plain", "utf-8"))
                alt_part.attach(MIMEText(body_html, "html", "utf-8"))
                msg.attach(alt_part)
            else:
                msg.attach(MIMEText(plain_text, "plain", "utf-8"))
                msg.attach(MIMEText(body_html, "html", "utf-8"))

            # Attach files
            for attachment in attachments or []:
                filename = attachment["name"]
                data = attachment["data"]
                mime_type, _ = mimetypes.guess_type(filename)
                if mime_type:
                    main_type, sub_type = mime_type.split("/", 1)
                else:
                    main_type, sub_type = "application", "octet-stream"
                part = MIMEBase(main_type, sub_type)
                part.set_payload(data)
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", "attachment", filename=filename)
                msg.attach(part)

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
            return {
                "success": False,
                "error": f"SMTP error {e.smtp_code}: {e.smtp_error}",
                "timestamp": timestamp,
            }

        except smtplib.SMTPAuthenticationError:
            return {
                "success": False,
                "error": "Authentication failed. Check your email and app password.",
                "timestamp": timestamp,
            }

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
    attachments: list[dict] | None = None,
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
        attachments=attachments,
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
