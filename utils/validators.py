"""
Email validation and template variable utilities.
"""
import re


def is_valid_email(email: str) -> bool:
    """Validate an email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None


def extract_variables(text: str) -> list[str]:
    """
    Extract all ${variable_name} patterns from a template string.
    Returns a deduplicated, ordered list of variable names.
    """
    matches = re.findall(r'\$\{(\w+)\}', text)
    # Deduplicate while preserving order
    seen = set()
    result = []
    for var in matches:
        if var not in seen:
            seen.add(var)
            result.append(var)
    return result


def validate_recipient_data(recipient: dict, required_variables: list[str]) -> tuple[bool, str]:
    """
    Validate that a recipient dict has all required variable values filled in.
    Returns (is_valid, error_message).
    """
    if "email" not in recipient or not recipient["email"]:
        return False, "Email address is required."

    if not is_valid_email(recipient["email"]):
        return False, f"Invalid email format: {recipient['email']}"

    for var in required_variables:
        if var not in recipient or not str(recipient[var]).strip():
            return False, f"Missing value for variable '${{{var}}}' for {recipient.get('email', 'unknown')}."

    return True, ""


def substitute_variables(template: str, variables: dict) -> str:
    """
    Replace all ${variable_name} in template with values from the variables dict.
    Missing variables are left as-is.
    """
    def replacer(match):
        var_name = match.group(1)
        return str(variables.get(var_name, match.group(0)))

    return re.sub(r'\$\{(\w+)\}', replacer, template)
