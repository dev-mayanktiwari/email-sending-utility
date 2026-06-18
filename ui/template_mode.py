"""
Template Mode tab — create, manage, and send templated emails with custom variables.
"""
import time
import streamlit as st

from ui.credentials import get_credentials, is_connected
from ui.styles import render_section_divider, render_variable_tags
from utils.email_sender import send_email, send_test_email
from utils.validators import is_valid_email, extract_variables, substitute_variables, validate_recipient_data
from utils.markdown_parser import markdown_to_html, plain_text_to_html
from storage.templates import load_templates, save_template, delete_template, get_template_names, get_template
from storage.history import log_send


def render_template_mode():
    """Render the Template Mode tab."""
    st.markdown("""
    <div class="glass-card">
        <h3>📝 Template Mode</h3>
        <p style="color: #8b8fa3; margin: 0;">Create reusable templates with custom variables. Personalize every email at scale.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Template Management ──────────────────────────────────
    _render_template_editor()

    render_section_divider()

    # ── Recipients ───────────────────────────────────────────
    _render_recipients_section()

    render_section_divider()

    # ── Preview & Send ───────────────────────────────────────
    _render_preview_and_send()


def _render_template_editor():
    """Template create/edit section."""
    st.markdown("#### 📄 Template")

    # Load available templates
    template_names = get_template_names()
    options = ["➕ Create New Template"] + [f"{name}" for _, name in template_names]
    slug_map = {name: slug for slug, name in template_names}

    selected_option = st.selectbox(
        "Select Template",
        options,
        key="tm_template_select",
    )

    is_new = selected_option == "➕ Create New Template"
    current_slug = None

    # Load template data if editing existing
    if not is_new:
        current_slug = slug_map.get(selected_option)
        template_data = get_template(current_slug)
        if template_data is None:
            st.error("Template not found.")
            return
    else:
        template_data = {"name": "", "subject": "", "body": "", "variables": []}

    # Template name
    template_name = st.text_input(
        "Template Name",
        value=template_data["name"] if not is_new else "",
        key="tm_name",
        placeholder="e.g. Recruiter Outreach, Follow-Up, Cold Email",
    )

    # Subject
    subject_template = st.text_input(
        "Subject Line",
        value=template_data["subject"],
        key="tm_subject",
        placeholder="e.g. Interested in ${role} at ${company}",
        help="Use ${variable_name} to insert dynamic values.",
    )

    # Subject line character counter
    raw_subject = subject_template or ""
    if raw_subject:
        char_count = len(raw_subject)
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

    # Body
    body_template = st.text_area(
        "Email Body",
        value=template_data["body"],
        key="tm_body",
        height=280,
        placeholder="Hi ${name},\n\nI'm reaching out about the ${role} position at ${company}...\n\nUse ${variable_name} for dynamic content.",
        help="Use **Markdown** for formatting and ${variable_name} for dynamic variables.",
    )

    # Auto-detect variables
    all_text = (subject_template or "") + " " + (body_template or "")
    detected_vars = extract_variables(all_text)

    # Display detected variables
    if detected_vars:
        st.markdown("**Detected Variables:**")
        render_variable_tags(detected_vars)
    elif all_text.strip():
        st.caption("💡 *Tip: Use `${variable_name}` syntax to add dynamic variables (e.g., `${name}`, `${company}`, `${role}`).*")

    # Save / Delete / Duplicate buttons
    col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])

    with col1:
        save_label = "💾 Save Template" if is_new else "💾 Update"
        if st.button(save_label, key="tm_save", type="primary", use_container_width=True):
            if not template_name:
                st.error("Template name is required.")
            elif not subject_template:
                st.error("Subject line is required.")
            elif not body_template:
                st.error("Email body is required.")
            else:
                saved_slug = save_template(
                    name=template_name,
                    subject=subject_template,
                    body=body_template,
                    variables=detected_vars,
                    slug=current_slug,
                )
                st.success(f"Template '{template_name}' saved!")
                st.session_state.tm_active_slug = saved_slug
                st.session_state.tm_active_vars = detected_vars
                time.sleep(0.5)
                st.rerun()

    with col2:
        if not is_new:
            if st.button("📋 Duplicate", key="tm_duplicate", use_container_width=True):
                if subject_template and body_template:
                    new_slug = save_template(
                        name=f"{template_name} (Copy)",
                        subject=subject_template,
                        body=body_template,
                        variables=detected_vars,
                        slug=None,
                    )
                    st.success("Template duplicated!")
                    time.sleep(0.5)
                    st.rerun()

    with col3:
        if not is_new:
            if st.button("🗑️ Delete", key="tm_delete", use_container_width=True):
                delete_template(current_slug)
                st.success("Template deleted.")
                time.sleep(0.5)
                st.rerun()

    # Store active template info for recipients section
    if not is_new and current_slug:
        st.session_state.tm_active_slug = current_slug
        st.session_state.tm_active_vars = detected_vars
        st.session_state.tm_active_subject = subject_template
        st.session_state.tm_active_body = body_template
        st.session_state.tm_active_name = template_data["name"]
    elif detected_vars is not None:
        st.session_state.tm_active_vars = detected_vars
        st.session_state.tm_active_subject = subject_template
        st.session_state.tm_active_body = body_template
        st.session_state.tm_active_name = template_name


def _render_recipients_section():
    """Dynamic recipients section based on template variables."""
    st.markdown("#### 👥 Recipients")

    variables = st.session_state.get("tm_active_vars", [])

    if "tm_recipients" not in st.session_state:
        st.session_state.tm_recipients = []

    # ── Single recipient add ─────────────────────────────────
    # Build dynamic columns based on variables
    fields = ["email"] + variables
    num_fields = len(fields)

    if num_fields <= 4:
        cols = st.columns(num_fields + 1)  # +1 for add button
    else:
        cols = st.columns(5)  # Cap at 5 columns, extras wrap

    field_values = {}

    for idx, field in enumerate(fields):
        col_idx = idx if idx < len(cols) - 1 else len(cols) - 2
        with cols[col_idx]:
            label = field.replace("_", " ").title()
            placeholder = f"Enter {label.lower()}"
            if field == "email":
                placeholder = "recruiter@company.com"
            field_values[field] = st.text_input(
                label,
                key=f"tm_input_{field}",
                placeholder=placeholder,
            )

    with cols[-1]:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add", key="tm_add_recipient", use_container_width=True):
            if not field_values.get("email"):
                st.warning("Email is required.")
            elif not is_valid_email(field_values["email"]):
                st.error("Invalid email format.")
            else:
                # Check for duplicate emails
                existing_emails = [r["email"] for r in st.session_state.tm_recipients]
                if field_values["email"] in existing_emails:
                    st.warning("This email is already added.")
                else:
                    new_recipient = {k: v for k, v in field_values.items()}
                    is_valid, error_msg = validate_recipient_data(new_recipient, variables)
                    if is_valid:
                        st.session_state.tm_recipients.append(new_recipient)
                        st.rerun()
                    else:
                        st.error(error_msg)

    # ── Bulk import ──────────────────────────────────────────
    with st.expander("📥 Bulk Import (CSV)"):
        header_hint = ",".join(fields)
        st.caption(f"**Expected format:** `{header_hint}` (one per line)")
        bulk_csv = st.text_area(
            "Paste CSV data",
            key="tm_bulk_csv",
            placeholder=f"{header_hint}\njohn@company.com,John,Acme Inc",
            label_visibility="collapsed",
            height=120,
        )
        if st.button("📤 Import", key="tm_bulk_import"):
            if bulk_csv.strip():
                added, skipped = 0, 0
                lines = bulk_csv.strip().split('\n')
                existing_emails = {r["email"] for r in st.session_state.tm_recipients}

                for line in lines:
                    parts = [p.strip() for p in line.split(',')]
                    # Skip header row if it matches field names
                    if parts == fields:
                        continue
                    if len(parts) >= len(fields):
                        recipient = {fields[i]: parts[i] for i in range(len(fields))}
                        is_valid, _ = validate_recipient_data(recipient, variables)
                        if is_valid and recipient["email"] not in existing_emails:
                            st.session_state.tm_recipients.append(recipient)
                            existing_emails.add(recipient["email"])
                            added += 1
                        else:
                            skipped += 1
                    else:
                        skipped += 1

                if added:
                    st.success(f"Imported {added} recipient(s).")
                if skipped:
                    st.warning(f"Skipped {skipped} row(s) (invalid, incomplete, or duplicate).")
                if added:
                    st.rerun()

    # ── Display recipients ───────────────────────────────────
    if st.session_state.tm_recipients:
        st.markdown(f"**{len(st.session_state.tm_recipients)} recipient(s):**")

        for i, rec in enumerate(st.session_state.tm_recipients):
            col1, col2 = st.columns([5, 1])
            with col1:
                display_parts = [f"**{rec['email']}**"]
                for var in variables:
                    if var in rec and rec[var]:
                        display_parts.append(f"{var}: {rec[var]}")
                st.markdown(" · ".join(display_parts))
            with col2:
                if st.button("🗑️", key=f"tm_remove_{i}"):
                    st.session_state.tm_recipients.pop(i)
                    st.rerun()

        if st.button("🧹 Clear All Recipients", key="tm_clear_all"):
            st.session_state.tm_recipients = []
            st.rerun()
    else:
        st.info("Add at least one recipient to preview and send emails.")


def _render_email_preview_card(subject: str, body_html: str, sender_name: str, sender_email: str, recipient_email: str):
    """Render a visual email preview card showing exactly what the recipient sees."""
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


def _render_preview_and_send():
    """Preview and send section."""
    recipients = st.session_state.get("tm_recipients", [])
    subject_template = st.session_state.get("tm_active_subject", "")
    body_template = st.session_state.get("tm_active_body", "")
    template_name = st.session_state.get("tm_active_name", "")

    if not recipients:
        return

    if not subject_template or not body_template:
        st.warning("Complete the template (subject + body) to preview and send.")
        return

    st.markdown("#### 👁️ Preview & Send")

    # Preview selector
    preview_options = [f"{r['email']}" for r in recipients]
    selected_preview = st.selectbox(
        "Preview for recipient",
        preview_options,
        key="tm_preview_select",
    )

    selected_idx = preview_options.index(selected_preview)
    selected_recipient = recipients[selected_idx]

    # Substitute variables
    preview_subject = substitute_variables(subject_template, selected_recipient)
    preview_body = substitute_variables(body_template, selected_recipient)

    # Render body HTML for preview
    if st.session_state.get("format_as_markdown", True):
        preview_html = markdown_to_html(preview_body, wrap_in_email=False)
    else:
        preview_html = plain_text_to_html(preview_body, wrap_in_email=False)

    # Get sender info for preview
    sender_email, _, sender_name, reply_to = get_credentials()

    st.caption("This is exactly how your email will appear to the selected recipient.")

    _render_email_preview_card(
        subject=preview_subject,
        body_html=preview_html,
        sender_name=sender_name,
        sender_email=sender_email,
        recipient_email=selected_recipient["email"],
    )

    # Test send button — always visible, locked until connected
    can_test = is_connected()
    test_tooltip = "Send a test copy to your own inbox" if can_test else "To unlock: connect credentials in sidebar"
    if st.button("📨 Send Test to Myself", key="tm_test_send", disabled=not can_test, help=test_tooltip):
        sender_email, sender_password, sender_name, reply_to = get_credentials()
        use_markdown = st.session_state.get("format_as_markdown", True)
        if use_markdown:
            test_html = markdown_to_html(preview_body)
        else:
            test_html = plain_text_to_html(preview_body)
        with st.spinner("Sending test email..."):
            result = send_test_email(sender_email, sender_password, sender_name, preview_subject, test_html, reply_to)
        if result["success"]:
            st.success(f"✅ Test sent to {sender_email} — check your inbox!")
        else:
            st.error(f"Failed: {result['error']}")

    render_section_divider()

    total = len(recipients)
    confirmed = st.checkbox(
        f"Ready to send to **{total} recipient(s)**",
        key="tm_confirm",
    )

    send_col1, send_col2 = st.columns([1, 3])
    with send_col1:
        send_clicked = st.button(
            f"🚀 Send to {total}",
            key="tm_send",
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

        success_count, fail_count = 0, 0
        progress = st.progress(0)
        status_text = st.empty()
        results_container = st.container()

        for i, rec in enumerate(recipients):
            status_text.text(f"📤 Sending to {rec['email']}... ({i + 1}/{total})")
            progress.progress((i + 1) / total)

            final_subject = substitute_variables(subject_template, rec)
            final_body = substitute_variables(body_template, rec)

            if use_markdown:
                html_body = markdown_to_html(final_body)
            else:
                html_body = plain_text_to_html(final_body)

            result = send_email(
                sender_email, sender_password, sender_name,
                rec["email"], final_subject, html_body,
                reply_to=reply_to,
            )

            log_send(
                recipient_email=rec["email"],
                subject=final_subject,
                success=result["success"],
                error=result["error"],
                mode="template",
                template_name=template_name,
            )

            if result["success"]:
                success_count += 1
            else:
                fail_count += 1
                with results_container:
                    st.warning(f"❌ {rec['email']}: {result['error']}")

            if i < total - 1 and delay > 0:
                time.sleep(delay)

        status_text.empty()

        with results_container:
            if success_count:
                st.success(f"✅ Successfully sent {success_count}/{total} email(s)!")
            if fail_count:
                st.error(f"❌ Failed: {fail_count}/{total}")
