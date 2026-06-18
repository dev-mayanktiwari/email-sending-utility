"""
Quick Send tab — fire-and-forget emails with no templates or variables.
"""
import time
import streamlit as st

from ui.credentials import get_credentials, is_connected
from ui.styles import render_section_divider
from utils.email_sender import send_email, send_test_email
from utils.validators import is_valid_email
from utils.markdown_parser import markdown_to_html, plain_text_to_html
from storage.history import log_send


def _render_email_preview(subject: str, body: str, sender_name: str, sender_email: str, recipient_email: str = "recipient@example.com"):
    """Render a visual email preview card showing exactly what the recipient sees."""
    use_markdown = st.session_state.get("format_as_markdown", True)
    if use_markdown:
        body_html = markdown_to_html(body, wrap_in_email=False)
    else:
        body_html = plain_text_to_html(body, wrap_in_email=False)

    from_display = f"{sender_name} &lt;{sender_email}&gt;" if sender_name else sender_email or "you@gmail.com"

    st.markdown(f"""
    <div style="
        background: #1e293b;
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 14px;
        overflow: hidden;
        margin: 0.5rem 0;
    ">
        <!-- Email header bar -->
        <div style="
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.1));
            padding: 1rem 1.25rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        ">
            <div style="color: #64748b; font-size: 0.8rem; margin-bottom: 6px;">FROM</div>
            <div style="color: #e2e8f0; font-size: 0.9rem; margin-bottom: 10px;">{from_display}</div>
            <div style="color: #64748b; font-size: 0.8rem; margin-bottom: 6px;">TO</div>
            <div style="color: #e2e8f0; font-size: 0.9rem; margin-bottom: 10px;">{recipient_email}</div>
            <div style="color: #64748b; font-size: 0.8rem; margin-bottom: 6px;">SUBJECT</div>
            <div style="color: #f1f5f9; font-size: 1.05rem; font-weight: 600;">{subject or '<span style="color: #64748b; font-style: italic;">No subject</span>'}</div>
        </div>
        <!-- Email body -->
        <div style="
            padding: 1.25rem;
            color: #cbd5e1;
            font-size: 0.95rem;
            line-height: 1.7;
        ">
            {body_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_quick_send():
    """Render the Quick Send tab."""
    st.markdown("""
    <div class="glass-card">
        <h3>🚀 Quick Send</h3>
        <p style="color: #94a3b8; margin: 0;">Write once, send to many. No templates, no variables — just your message.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Compose ──────────────────────────────────────────────
    st.markdown("#### ✏️ Compose")

    subject = st.text_input(
        "Subject",
        key="qs_subject",
        placeholder="e.g. Fullstack Engineer – Interested in Opportunities",
    )

    # Subject line character counter with visual cue
    if subject:
        char_count = len(subject)
        if char_count <= 50:
            color, note = "#34d399", "great length"
        elif char_count <= 70:
            color, note = "#fbbf24", "a bit long"
        else:
            color, note = "#fb7185", "too long — may get clipped"
        st.markdown(
            f'<p style="font-size:0.78rem; color:{color}; margin-top:-8px;">'
            f'{char_count} chars — {note}</p>',
            unsafe_allow_html=True,
        )

    body = st.text_area(
        "Body",
        key="qs_body",
        height=250,
        placeholder="Write your email body here...\n\nYou can use **Markdown** for formatting (bold, links, lists).",
    )

    # ── Email Preview ────────────────────────────────────────
    if body:
        st.markdown("#### 👁️ Email Preview")
        st.caption("This is exactly how your email will appear to recipients.")
        sender_email, _, sender_name, _ = get_credentials()
        _render_email_preview(
            subject=subject,
            body=body,
            sender_name=sender_name,
            sender_email=sender_email,
        )

    # ── Test Send ────────────────────────────────────────────
    can_test = bool(is_connected() and subject and body)
    if not can_test:
        missing = []
        if not is_connected():
            missing.append("connect credentials in sidebar")
        if not subject:
            missing.append("add a subject")
        if not body:
            missing.append("write a body")
        tooltip = "To unlock: " + ", ".join(missing)
    else:
        tooltip = "Send a test copy to your own inbox"

    if st.button("📨 Send Test to Myself", key="qs_test_send", disabled=not can_test, help=tooltip):
        sender_email, sender_password, sender_name, reply_to = get_credentials()
        use_markdown = st.session_state.get("format_as_markdown", True)
        if use_markdown:
            html_body = markdown_to_html(body)
        else:
            html_body = plain_text_to_html(body)
        with st.spinner("Sending test email..."):
            result = send_test_email(sender_email, sender_password, sender_name, subject, html_body, reply_to)
        if result["success"]:
            st.success(f"✅ Test sent to {sender_email} — check your inbox!")
        else:
            st.error(f"Failed: {result['error']}")

    render_section_divider()

    # ── Recipients ───────────────────────────────────────────
    st.markdown("#### 📬 Recipients")

    if "qs_recipients" not in st.session_state:
        st.session_state.qs_recipients = []

    # Single add
    col1, col2 = st.columns([3, 1])
    with col1:
        new_email = st.text_input(
            "Add email address",
            key="qs_new_email",
            placeholder="recruiter@company.com",
            label_visibility="collapsed",
        )
    with col2:
        if st.button("➕ Add", key="qs_add_btn", use_container_width=True):
            if new_email:
                if is_valid_email(new_email):
                    if new_email not in st.session_state.qs_recipients:
                        st.session_state.qs_recipients.append(new_email)
                        st.rerun()
                    else:
                        st.warning("Already added.")
                else:
                    st.error("Invalid email format.")
            else:
                st.warning("Enter an email address.")

    # Bulk add
    with st.expander("📥 Bulk Import (paste emails, one per line)"):
        bulk_text = st.text_area(
            "Emails",
            key="qs_bulk",
            placeholder="recruiter1@company.com\nrecruiter2@company.com\nrecruiter3@company.com",
            label_visibility="collapsed",
            height=120,
        )
        if st.button("📤 Import", key="qs_bulk_import"):
            if bulk_text.strip():
                added, skipped = 0, 0
                for line in bulk_text.strip().split('\n'):
                    email = line.strip().strip(',').strip(';')
                    if email and is_valid_email(email):
                        if email not in st.session_state.qs_recipients:
                            st.session_state.qs_recipients.append(email)
                            added += 1
                        else:
                            skipped += 1
                    elif email:
                        skipped += 1
                if added:
                    st.success(f"Imported {added} email(s).")
                if skipped:
                    st.warning(f"Skipped {skipped} (invalid or duplicate).")
                if added:
                    st.rerun()

    # Display recipients
    if st.session_state.qs_recipients:
        st.markdown(f"**{len(st.session_state.qs_recipients)} recipient(s):**")
        for i, email in enumerate(st.session_state.qs_recipients):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"`{email}`")
            with col2:
                if st.button("🗑️", key=f"qs_remove_{i}"):
                    st.session_state.qs_recipients.pop(i)
                    st.rerun()

        # Clear all
        if st.button("🧹 Clear All Recipients", key="qs_clear_all"):
            st.session_state.qs_recipients = []
            st.rerun()
    else:
        st.info("Add at least one recipient to start sending.")

    render_section_divider()

    # ── Send ─────────────────────────────────────────────────
    if st.session_state.qs_recipients and subject and body:
        total = len(st.session_state.qs_recipients)
        confirmed = st.checkbox(
            f"Ready to send to **{total} recipient(s)**",
            key="qs_confirm",
        )

        send_col1, send_col2 = st.columns([1, 3])
        with send_col1:
            send_clicked = st.button(
                f"🚀 Send to {total}",
                key="qs_send",
                type="primary",
                use_container_width=True,
                disabled=not confirmed,
            )

        if send_clicked:
            if not is_connected():
                st.error("⚠️ Set up your credentials in the sidebar first.")
                return

            sender_email, sender_password, sender_name, reply_to = get_credentials()
            delay = st.session_state.get("send_delay", 2)
            use_markdown = st.session_state.get("format_as_markdown", True)

            if use_markdown:
                html_body = markdown_to_html(body)
            else:
                html_body = plain_text_to_html(body)

            success_count, fail_count = 0, 0
            progress = st.progress(0)
            status_text = st.empty()
            results_container = st.container()

            for i, recipient_email in enumerate(st.session_state.qs_recipients):
                status_text.text(f"📤 Sending to {recipient_email}... ({i + 1}/{total})")
                progress.progress((i + 1) / total)

                result = send_email(
                    sender_email, sender_password, sender_name,
                    recipient_email, subject, html_body,
                    reply_to=reply_to,
                )

                log_send(
                    recipient_email=recipient_email,
                    subject=subject,
                    success=result["success"],
                    error=result["error"],
                    mode="quick",
                )

                if result["success"]:
                    success_count += 1
                else:
                    fail_count += 1
                    with results_container:
                        st.warning(f"❌ {recipient_email}: {result['error']}")

                if i < total - 1 and delay > 0:
                    time.sleep(delay)

            status_text.empty()

            with results_container:
                if success_count:
                    st.success(f"✅ Successfully sent {success_count}/{total} email(s)!")
                if fail_count:
                    st.error(f"❌ Failed: {fail_count}/{total}")
