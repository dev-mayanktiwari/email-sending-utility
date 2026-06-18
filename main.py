"""
MailForge — Recruiter outreach, simplified.
Entry point for the Streamlit application.
"""
import csv
import io
import streamlit as st

from config import APP_NAME, APP_ICON, APP_VERSION
from ui.styles import inject_custom_css, render_header, render_section_divider, render_metric_card, render_status_badge
from ui.credentials import render_credentials_sidebar
from ui.quick_send import render_quick_send
from ui.template_mode import render_template_mode
from storage.history import get_history, get_history_stats, clear_history


def render_history_tab():
    """Render the History tab."""
    st.markdown("""
    <div class="glass-card">
        <h3>📊 Send History</h3>
        <p style="color: #8b8fa3; margin: 0;">Track every email sent — successes, failures, and timestamps.</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    stats = get_history_stats()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_metric_card(stats["total"], "Total Sent"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric_card(stats["successful"], "Successful"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric_card(stats["failed"], "Failed"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_metric_card(f"{stats['success_rate']}%", "Success Rate"), unsafe_allow_html=True)

    render_section_divider()

    # History list
    history = get_history(limit=100)

    if history:
        # Filters
        col1, col2 = st.columns([1, 4])
        with col1:
            filter_status = st.selectbox(
                "Filter",
                ["All", "Successful", "Failed"],
                key="history_filter",
            )

        if filter_status == "Successful":
            history = [h for h in history if h.get("success")]
        elif filter_status == "Failed":
            history = [h for h in history if not h.get("success")]

        st.markdown(f"**Showing {len(history)} entries:**")

        for entry in history:
            status_html = render_status_badge(entry.get("success", False))
            mode_label = "⚡" if entry.get("mode") == "quick" else "📝"
            template_info = f" · Template: {entry['template']}" if entry.get("template") else ""

            # Format timestamp
            ts = entry.get("timestamp", "")
            if ts:
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(ts)
                    ts = dt.strftime("%b %d, %Y %I:%M %p")
                except (ValueError, TypeError):
                    pass

            st.markdown(f"""
            <div class="history-row">
                {status_html} &nbsp;
                {mode_label} &nbsp;
                <strong>{entry.get('recipient', 'Unknown')}</strong> &nbsp;·&nbsp;
                {entry.get('subject', 'No subject')}{template_info} &nbsp;·&nbsp;
                <span style="color: #8b8fa3; font-size: 0.8rem;">{ts}</span>
                {"<br><span style='color: #ef4444; font-size: 0.8rem;'>Error: " + entry.get('error', '') + "</span>" if entry.get('error') else ""}
            </div>
            """, unsafe_allow_html=True)

        render_section_divider()

        # Export CSV
        col_export, col_clear, _ = st.columns([1, 1, 3])
        with col_export:
            if history:
                output = io.StringIO()
                writer = csv.DictWriter(
                    output,
                    fieldnames=["timestamp", "recipient", "subject", "success", "mode", "template", "error"],
                    extrasaction="ignore",
                )
                writer.writeheader()
                writer.writerows(history)
                st.download_button(
                    label="📥 Export CSV",
                    data=output.getvalue(),
                    file_name="mailforge_history.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
        with col_clear:
            if st.button("🧹 Clear History", key="clear_history", use_container_width=True):
                clear_history()
                st.success("History cleared.")
                st.rerun()
    else:
        st.info("No emails sent yet. Your send history will appear here.")


def main():
    """Application entry point."""
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Inject custom CSS
    inject_custom_css()

    # Render header
    render_header()

    # Render sidebar credentials
    render_credentials_sidebar()

    # Main tabs
    tab_quick, tab_template, tab_history = st.tabs([
        "🚀 Quick Send",
        "📝 Template Mode",
        "📊 History",
    ])

    with tab_quick:
        render_quick_send()

    with tab_template:
        render_template_mode()

    with tab_history:
        render_history_tab()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f'<p style="color: #8b8fa3; font-size: 0.75rem; text-align: center;">'
        f'{APP_NAME} v{APP_VERSION}<br>Built for recruiter outreach</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()