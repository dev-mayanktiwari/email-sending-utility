"""
Markdown to HTML conversion for email bodies.
Uses the `markdown` library for proper parsing.
"""
import markdown


# Email-safe HTML wrapper with inline styles
EMAIL_HTML_WRAPPER = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 15px;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }}
  a {{
    color: #2563eb;
    text-decoration: none;
  }}
  a:hover {{
    text-decoration: underline;
  }}
  strong {{
    font-weight: 600;
  }}
  p {{
    margin: 0 0 12px 0;
  }}
  ul, ol {{
    margin: 0 0 12px 0;
    padding-left: 24px;
  }}
</style>
</head>
<body>
{content}
</body>
</html>"""


def markdown_to_html(text: str, wrap_in_email: bool = True) -> str:
    """
    Convert markdown text to HTML suitable for emails.

    Args:
        text: Markdown-formatted text
        wrap_in_email: If True, wraps in a full HTML email template with inline styles

    Returns:
        HTML string
    """
    # Convert markdown to HTML
    html_content = markdown.markdown(
        text,
        extensions=['extra', 'nl2br', 'sane_lists'],
    )

    if wrap_in_email:
        return EMAIL_HTML_WRAPPER.format(content=html_content)
    return html_content


def plain_text_to_html(text: str, wrap_in_email: bool = True) -> str:
    """
    Convert plain text to HTML (just converts newlines to <br>).
    For Quick Send mode where users don't want markdown.
    """
    import html as html_module
    escaped = html_module.escape(text)
    html_content = escaped.replace('\n', '<br>\n')

    if wrap_in_email:
        return EMAIL_HTML_WRAPPER.format(content=html_content)
    return html_content
