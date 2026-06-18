"""
Template CRUD operations using a local JSON file.
"""
import json
import os
from datetime import datetime

from config import TEMPLATES_FILE, DATA_DIR


def _ensure_file():
    """Create the templates file with a default template if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(TEMPLATES_FILE):
        default = {
            "recruiter_outreach": {
                "name": "Recruiter Outreach",
                "subject": "Eager to Contribute to ${company} – Fullstack Engineer Application",
                "body": (
                    "Hi ${name},\n\n"
                    "I hope you're doing well.\n\n"
                    "I'm reaching out to express my keen interest in joining **${company}** as a Fullstack Engineer.\n\n"
                    "I have hands-on experience building scalable systems using **Node.js, React.js, Next.js, PostgreSQL, and MongoDB**, "
                    "and have worked extensively across **AWS, GCP, Azure, and Kubernetes** to deploy and manage cloud-native applications.\n\n"
                    "I'm passionate about solving real-world problems through efficient engineering and clean, maintainable code. "
                    "I've attached my resume for your reference and would be grateful for an opportunity to chat or contribute in any way that adds value to your team.\n\n"
                    "Looking forward to hearing from you.\n\n"
                    "Warm regards,  \n\n"
                    "Mayank Tiwari  \n"
                    "Contact: 9319557584  \n"
                    "Github: https://www.github.com/dev-mayanktiwari  \n"
                    "Resume: https://drive.google.com/file/d/1tFdzcqGoUzwy5LkBUTPdg6v4f71dOcDs/view"
                ),
                "variables": ["name", "company"],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
        }
        with open(TEMPLATES_FILE, "w") as f:
            json.dump(default, f, indent=2)


def _read_all() -> dict:
    """Read all templates from the JSON file."""
    _ensure_file()
    with open(TEMPLATES_FILE, "r") as f:
        return json.load(f)


def _write_all(data: dict):
    """Write all templates to the JSON file."""
    with open(TEMPLATES_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_templates() -> dict:
    """Load all templates. Returns dict keyed by template slug."""
    return _read_all()


def get_template(slug: str) -> dict | None:
    """Get a single template by its slug."""
    templates = _read_all()
    return templates.get(slug)


def save_template(name: str, subject: str, body: str, variables: list[str], slug: str | None = None) -> str:
    """
    Save a template (create or update).

    Args:
        name: Display name of the template
        subject: Subject line template
        body: Body template
        variables: List of variable names used
        slug: Optional slug for updating existing. If None, generates from name.

    Returns:
        The slug of the saved template.
    """
    templates = _read_all()

    if slug is None:
        # Generate slug from name
        slug = name.lower().replace(" ", "_").replace("-", "_")
        # Ensure uniqueness
        base_slug = slug
        counter = 1
        while slug in templates:
            slug = f"{base_slug}_{counter}"
            counter += 1

    now = datetime.now().isoformat()

    if slug in templates:
        # Update existing
        templates[slug]["name"] = name
        templates[slug]["subject"] = subject
        templates[slug]["body"] = body
        templates[slug]["variables"] = variables
        templates[slug]["updated_at"] = now
    else:
        # Create new
        templates[slug] = {
            "name": name,
            "subject": subject,
            "body": body,
            "variables": variables,
            "created_at": now,
            "updated_at": now,
        }

    _write_all(templates)
    return slug


def delete_template(slug: str) -> bool:
    """Delete a template by slug. Returns True if deleted, False if not found."""
    templates = _read_all()
    if slug in templates:
        del templates[slug]
        _write_all(templates)
        return True
    return False


def get_template_names() -> list[tuple[str, str]]:
    """Return list of (slug, display_name) for all templates, sorted by name."""
    templates = _read_all()
    return sorted(
        [(slug, data["name"]) for slug, data in templates.items()],
        key=lambda x: x[1].lower(),
    )
