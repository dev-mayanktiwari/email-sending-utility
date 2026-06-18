"""
Application configuration constants.
"""
import os

# ── App Metadata ──────────────────────────────────────────────
APP_NAME = "MailForge"
APP_ICON = "🔥"
APP_TAGLINE = "Recruiter outreach, simplified."
APP_VERSION = "2.0.0"

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMPLATES_FILE = os.path.join(DATA_DIR, "templates.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

# ── SMTP Defaults ─────────────────────────────────────────────
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# ── Send Settings ─────────────────────────────────────────────
DEFAULT_SEND_DELAY_SECONDS = 2
MAX_RECIPIENTS_PER_BATCH = 100

# ── Ensure data dir exists ────────────────────────────────────
os.makedirs(DATA_DIR, exist_ok=True)
