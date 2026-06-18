"""
Custom CSS injection for a premium Streamlit UI.
Works WITH Streamlit's dark theme (set in .streamlit/config.toml).
"""
import streamlit as st


def inject_custom_css():
    """Inject custom CSS to elevate Streamlit's dark theme."""
    st.markdown("""
    <style>
    /* ── Google Font ────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ─────────────────────────────────────────── */
    html, body, [class*="css"], .stApp, .stMarkdown, p, span, label, li {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(160deg, #0a0a14 0%, #111827 40%, #0f172a 100%) !important;
    }

    /* ── All Text - High Contrast ───────────────────────── */
    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown span {
        color: #cbd5e1 !important;
    }

    /* ── Section Headings (h4 - #### in st.markdown) ───── */
    .stMarkdown h4 {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.75rem !important;
    }

    .stMarkdown h3 {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }

    .stMarkdown h2 {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
    }

    .stMarkdown strong {
        color: #f1f5f9 !important;
    }

    /* ── Header ─────────────────────────────────────────── */
    .app-header {
        text-align: center;
        padding: 2rem 0 1.2rem 0;
        margin-bottom: 0.5rem;
    }

    .app-header h1 {
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #c084fc 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 0.3rem !important;
        letter-spacing: -0.5px;
    }

    .app-header p {
        color: #94a3b8 !important;
        font-size: 1.05rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.3px;
    }

    /* ── Cards ───────────────────────────────────────────── */
    .glass-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(30, 27, 75, 0.4) 100%);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(129, 140, 248, 0.35);
        box-shadow: 0 8px 32px rgba(129, 140, 248, 0.08);
    }

    .glass-card h3 {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        margin-bottom: 0.4rem !important;
        font-size: 1.15rem !important;
    }

    .glass-card p {
        color: #94a3b8 !important;
        font-size: 0.95rem !important;
    }

    /* ── Tabs ────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 14px;
        padding: 5px;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 28px;
        font-weight: 500;
        font-size: 0.95rem;
        color: #94a3b8 !important;
        transition: all 0.25s ease;
        background: transparent;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #e2e8f0 !important;
        background: rgba(148, 163, 184, 0.08);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
    }

    /* ── Labels ──────────────────────────────────────────── */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label,
    .stSlider > label,
    .stNumberInput > label,
    label[data-testid="stWidgetLabel"] {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        margin-bottom: 4px !important;
    }

    /* ── Inputs ──────────────────────────────────────────── */
    /* Text inputs */
    input[data-testid="stTextInputRootElement"] input,
    .stTextInput input,
    div[data-baseweb="input"] input {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        caret-color: #818cf8 !important;
    }

    div[data-baseweb="input"] {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border-color: rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
    }

    input:focus, div[data-baseweb="input"]:focus-within {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.15) !important;
    }

    /* Textareas */
    .stTextArea textarea,
    div[data-baseweb="textarea"] textarea {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        caret-color: #818cf8 !important;
        line-height: 1.6 !important;
    }

    div[data-baseweb="textarea"] {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border-color: rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
    }

    textarea:focus, div[data-baseweb="textarea"]:focus-within {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.15) !important;
    }

    /* Selectbox */
    div[data-baseweb="select"] {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }

    div[data-baseweb="select"] span {
        color: #f1f5f9 !important;
    }

    /* Dropdown menu */
    div[data-baseweb="popover"] {
        background-color: #1e293b !important;
        border: 1px solid rgba(148, 163, 184, 0.15) !important;
        border-radius: 12px !important;
    }

    ul[data-baseweb="menu"] {
        background-color: #1e293b !important;
    }

    li[data-baseweb="menu-item"],
    ul[role="listbox"] li {
        color: #e2e8f0 !important;
        background-color: transparent !important;
    }

    li[data-baseweb="menu-item"]:hover,
    ul[role="listbox"] li:hover,
    li[aria-selected="true"] {
        background-color: rgba(129, 140, 248, 0.15) !important;
        color: #f1f5f9 !important;
    }

    /* Placeholder text */
    input::placeholder,
    textarea::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }

    /* ── Buttons ─────────────────────────────────────────── */
    .stButton > button {
        border-radius: 10px;
        font-weight: 500;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.25s ease;
        border: 1px solid rgba(148, 163, 184, 0.15);
        background-color: rgba(30, 41, 59, 0.6);
        color: #e2e8f0;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: rgba(129, 140, 248, 0.4);
        box-shadow: 0 4px 16px rgba(129, 140, 248, 0.2);
        background-color: rgba(30, 41, 59, 0.9);
        color: #f1f5f9;
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Primary buttons */
    div[data-testid="stButton"] > button[kind="primary"],
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.6rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3);
    }

    div[data-testid="stButton"] > button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45) !important;
        transform: translateY(-2px);
    }

    /* ── Sidebar ─────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a14 0%, #111827 50%, #0f172a 100%) !important;
        border-right: 1px solid rgba(148, 163, 184, 0.08);
    }

    section[data-testid="stSidebar"] .stMarkdown h2 {
        font-size: 1.1rem;
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p {
        color: #94a3b8 !important;
    }

    /* ── Expanders ───────────────────────────────────────── */
    details[data-testid="stExpander"] {
        background: rgba(30, 41, 59, 0.3) !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
        border-radius: 12px !important;
    }

    details[data-testid="stExpander"] summary {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
        list-style: none;
        padding: 0.6rem 1rem;
        cursor: pointer;
    }

    /* Hide browser's native disclosure arrow */
    details[data-testid="stExpander"] summary::-webkit-details-marker {
        display: none;
    }

    details[data-testid="stExpander"] summary::marker {
        display: none;
    }

    /* Keep Streamlit's SVG arrow visible and properly sized */
    details[data-testid="stExpander"] summary svg {
        color: #94a3b8 !important;
        width: 1rem !important;
        height: 1rem !important;
        vertical-align: middle;
        transition: transform 0.2s ease;
    }

    details[data-testid="stExpander"] summary:hover {
        color: #f1f5f9 !important;
    }

    details[data-testid="stExpander"] summary:hover svg {
        color: #e2e8f0 !important;
    }

    /* Expander body padding */
    details[data-testid="stExpander"] > div[data-testid="stExpanderDetails"] {
        padding: 0.5rem 0.25rem 0.25rem 0.25rem;
    }

    /* ── Slider ──────────────────────────────────────────── */
    .stSlider [data-baseweb="slider"] div {
        color: #e2e8f0 !important;
    }

    /* ── Toggle ──────────────────────────────────────────── */
    .stToggle label span {
        color: #cbd5e1 !important;
    }

    /* ── Info/Warning/Success/Error Boxes ─────────────────── */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
    }

    /* ── Code blocks ─────────────────────────────────────── */
    .stCodeBlock,
    code {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }

    /* ── Status Badges ───────────────────────────────────── */
    .status-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }

    .status-success {
        background: rgba(52, 211, 153, 0.12);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.25);
    }

    .status-error {
        background: rgba(251, 113, 133, 0.12);
        color: #fb7185;
        border: 1px solid rgba(251, 113, 133, 0.25);
    }

    .status-pending {
        background: rgba(251, 191, 36, 0.12);
        color: #fbbf24;
        border: 1px solid rgba(251, 191, 36, 0.25);
    }

    /* ── Variable Tags ───────────────────────────────────── */
    .var-tag {
        display: inline-block;
        padding: 4px 14px;
        margin: 3px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        background: rgba(129, 140, 248, 0.12);
        color: #a5b4fc;
        border: 1px solid rgba(129, 140, 248, 0.25);
        font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
    }

    /* ── Metric Cards ────────────────────────────────────── */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(30, 27, 75, 0.3) 100%);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 14px;
        padding: 1.4rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        border-color: rgba(129, 140, 248, 0.25);
        box-shadow: 0 4px 20px rgba(129, 140, 248, 0.08);
    }

    .metric-card .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }

    .metric-card .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 400;
        margin-top: 6px;
    }

    /* ── History Row ──────────────────────────────────────── */
    .history-row {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(148, 163, 184, 0.08);
        border-radius: 10px;
        padding: 0.75rem 1.1rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        color: #cbd5e1;
        transition: all 0.2s ease;
    }

    .history-row:hover {
        background: rgba(30, 41, 59, 0.6);
        border-color: rgba(148, 163, 184, 0.15);
    }

    .history-row strong {
        color: #f1f5f9;
    }

    /* ── Divider ─────────────────────────────────────────── */
    .section-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(129, 140, 248, 0.25) 50%, transparent 100%);
        margin: 1.5rem 0;
    }

    /* ── Connected Badge ─────────────────────────────────── */
    .connected-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        background: rgba(52, 211, 153, 0.1);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.2);
        margin: 8px 0;
    }

    .disconnected-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        background: rgba(251, 113, 133, 0.1);
        color: #fb7185;
        border: 1px solid rgba(251, 113, 133, 0.2);
        margin: 8px 0;
    }

    /* ── Inline code (backticks in markdown) ──────────────── */
    .stMarkdown code {
        background-color: rgba(129, 140, 248, 0.1) !important;
        color: #a5b4fc !important;
        padding: 2px 8px !important;
        border-radius: 6px !important;
        font-size: 0.88rem !important;
        border: 1px solid rgba(129, 140, 248, 0.15) !important;
    }

    /* ── Caption text ─────────────────────────────────────── */
    .stCaption, .stMarkdown small, [data-testid="stCaptionContainer"] {
        color: #64748b !important;
    }

    /* ── Hide Streamlit chrome ────────────────────────────── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Animations ──────────────────────────────────────── */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stTabs [data-baseweb="tab-panel"] {
        animation: fadeIn 0.3s ease;
    }

    /* ── Progress bar ─────────────────────────────────────── */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #a78bfa) !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the app header."""
    st.markdown("""
    <div class="app-header">
        <h1>🔥 MailForge</h1>
        <p>Recruiter outreach, simplified.</p>
    </div>
    """, unsafe_allow_html=True)


def render_section_divider():
    """Render a styled horizontal divider."""
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


def render_variable_tags(variables: list[str]):
    """Render variable names as styled tags."""
    if not variables:
        st.markdown("*No variables detected*")
        return
    tags_html = " ".join(f'<span class="var-tag">${{{v}}}</span>' for v in variables)
    st.markdown(tags_html, unsafe_allow_html=True)


def render_metric_card(value, label):
    """Render a metric card."""
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def render_status_badge(success: bool) -> str:
    """Return HTML for a status badge."""
    if success:
        return '<span class="status-badge status-success">✓ Sent</span>'
    return '<span class="status-badge status-error">✗ Failed</span>'
