"""
Sidebar credentials widget with connection test.
Credentials are always entered by the user — never pre-filled.
"""
import streamlit as st

from utils.email_sender import test_smtp_connection


def render_credentials_sidebar():
    """
    Render the credentials section in the sidebar.
    All fields start empty — the user must enter their own credentials.
    """
    if "cred_email" not in st.session_state:
        st.session_state.cred_email = ""
    if "cred_password" not in st.session_state:
        st.session_state.cred_password = ""
    if "cred_name" not in st.session_state:
        st.session_state.cred_name = ""
    if "cred_reply_to" not in st.session_state:
        st.session_state.cred_reply_to = ""
    if "cred_connected" not in st.session_state:
        st.session_state.cred_connected = False

    with st.sidebar:
        st.markdown("## 🔐 Credentials")

        if st.session_state.cred_connected and st.session_state.cred_email:
            st.markdown(
                f'<div class="connected-badge">🟢 Connected as {st.session_state.cred_email}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="disconnected-badge">🔴 Not connected</div>',
                unsafe_allow_html=True,
            )

        with st.expander("Edit Credentials", expanded=not st.session_state.cred_connected):
            email_input = st.text_input(
                "Gmail Address",
                value=st.session_state.cred_email,
                key="cred_email_input",
                placeholder="you@gmail.com",
            )

            password_input = st.text_input(
                "App Password",
                value="",
                type="password",
                key="cred_password_input",
                placeholder="16-character app password",
                help="myaccount.google.com → Security → 2-Step Verification → App passwords",
            )

            name_input = st.text_input(
                "Display Name",
                value=st.session_state.cred_name,
                key="cred_name_input",
                placeholder="John Doe",
                help="Shown as the sender name in the recipient's inbox.",
            )

            reply_to_input = st.text_input(
                "Reply-To (optional)",
                value=st.session_state.cred_reply_to,
                key="cred_reply_to_input",
                placeholder="other@email.com",
                help="Replies go here instead of your Gmail address.",
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Save", use_container_width=True):
                    if email_input:
                        st.session_state.cred_email = email_input
                    if password_input:
                        st.session_state.cred_password = password_input
                    if name_input:
                        st.session_state.cred_name = name_input
                    st.session_state.cred_reply_to = reply_to_input
                    st.session_state.cred_connected = bool(
                        st.session_state.cred_email and st.session_state.cred_password
                    )
                    if st.session_state.cred_connected:
                        st.success("Saved!")
                    else:
                        st.warning("Email & password required.")
                    st.rerun()

            with col2:
                if st.button("🔌 Test", use_container_width=True):
                    test_email = email_input or st.session_state.cred_email
                    test_pass = password_input or st.session_state.cred_password

                    if not test_email or not test_pass:
                        st.error("Enter email & password first.")
                    else:
                        with st.spinner("Testing connection..."):
                            ok, msg = test_smtp_connection(test_email, test_pass)
                        if ok:
                            st.success("✓ Connected!")
                            st.session_state.cred_email = test_email
                            st.session_state.cred_password = test_pass
                            if name_input:
                                st.session_state.cred_name = name_input
                            st.session_state.cred_reply_to = reply_to_input
                            st.session_state.cred_connected = True
                        else:
                            st.error(msg)

        st.markdown("---")
        st.markdown("## ⚙️ Settings")

        st.session_state.send_delay = st.slider(
            "Delay between sends (sec)",
            min_value=0,
            max_value=10,
            value=st.session_state.get("send_delay", 2),
            help="Delay between consecutive emails to avoid Gmail rate limiting.",
        )

        st.session_state.format_as_markdown = st.toggle(
            "Markdown formatting",
            value=st.session_state.get("format_as_markdown", True),
            help="If enabled, email body is parsed as Markdown → HTML. If disabled, sent as plain text.",
        )

        st.markdown("---")
        with st.expander("📬 Deliverability Tips"):
            st.markdown("""
**Avoid spam filters:**

✅ **Keep subject under 60 chars** — longer lines get clipped or flagged

✅ **Use your real name** as the display name — generic names look spammy

✅ **Personalize** with variables like `${name}` — identical bulk emails trigger filters

✅ **Don't use ALL CAPS** or excessive `!!!` in subject

✅ **Set a delay ≥ 2 sec** between sends — rate-bursting looks like spam

✅ **Test first** — use "Send Test" to check your own inbox before bulk sending

✅ **Keep lists clean** — remove bounced addresses from future sends

⚠️ **Gmail limits:** ~500 emails/day via App Password. Use Google Workspace for higher volume.
            """)


def get_credentials() -> tuple[str, str, str, str]:
    """
    Get current credentials from session state.
    Returns (email, password, name, reply_to).
    """
    return (
        st.session_state.get("cred_email", ""),
        st.session_state.get("cred_password", ""),
        st.session_state.get("cred_name", ""),
        st.session_state.get("cred_reply_to", ""),
    )


def is_connected() -> bool:
    """Check if credentials are loaded and presumably valid."""
    return st.session_state.get("cred_connected", False)
