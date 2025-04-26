import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import string
import os
from dotenv import load_dotenv

load_dotenv()

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def send_email(sender_email, sender_password, sender_name, recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <{sender_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def convert_markdown_to_html(text):
    # Simple markdown replacements
    text = text.replace('**', '<strong>', 1)
    text = text.replace('**', '</strong>', 1)
    text = text.replace('**', '<strong>', 1)
    text = text.replace('**', '</strong>', 1)
    return text.replace('\n', '<br>')

def main():
    st.title("📧 Personalized Email Sender")

    # Load from .env if not given manually
    env_sender_email = os.getenv("SENDER_EMAIL", "")
    env_sender_password = os.getenv("SENDER_PASSWORD", "")
    env_sender_name = os.getenv("SENDER_NAME", "Sender")

    with st.expander("🔐 Email Credentials", expanded=True):
        sender_email = st.text_input("Your Email Address", value=env_sender_email)
        sender_password = st.text_input("Your Email Password", value=env_sender_password, type="password")
        sender_name = st.text_input("Your Name", value=env_sender_name)

    with st.expander("📄 Email Template", expanded=True):
        st.markdown("### ✨ Default Template")
        st.code("""title: Eager to Contribute to ${company} – Fullstack Engineer Application
Hi ${name},
I hope you're doing well.
...""")
        
        custom_template = st.text_area("📝 Customize Email Template", 
        """title: Eager to Contribute to ${company} – Fullstack Engineer Application
Hi ${name},

I hope you're doing well.

I'm reaching out to express my keen interest in joining ${company} as a Fullstack Engineer.

I have hands-on experience building scalable systems using **Node.js, React.js, Next.js, PostgreSQL, and MongoDB**, and have worked extensively across **AWS, GCP, Azure, and Kubernetes** to deploy and manage cloud-native applications.

I'm passionate about solving real-world problems through efficient engineering and clean, maintainable code. I've attached my resume for your reference and would be grateful for an opportunity to chat or contribute in any way that adds value to your team.

Looking forward to hearing from you.

Warm regards,  

Mayank Tiwari  
Contact: 9319557584  
Github: https://www.github.com/dev-mayanktiwari  
Resume: https://drive.google.com/file/d/1tFdzcqGoUzwy5LkBUTPdg6v4f71dOcDs/view""", height=380)

    st.markdown("### 👥 Add Recipients")

    if 'recipients' not in st.session_state:
        st.session_state.recipients = []

    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        recipient_email = st.text_input("Recipient Email")
    with col2:
        recipient_name = st.text_input("Recipient Name")
    with col3:
        recipient_company = st.text_input("Company Name")

    if st.button("➕ Add Recipient"):
        if recipient_email and recipient_name and recipient_company:
            if is_valid_email(recipient_email):
                st.session_state.recipients.append({
                    "email": recipient_email,
                    "name": recipient_name,
                    "company": recipient_company
                })
                st.success(f"Added {recipient_name} from {recipient_company}")
            else:
                st.error("Invalid email format.")
        else:
            st.warning("Please fill in all fields.")

    if st.session_state.recipients:
        st.markdown("### 📋 Recipients List")
        for i, rec in enumerate(st.session_state.recipients):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"{rec['name']} ({rec['email']}) - {rec['company']}")
            with col2:
                if st.button("🗑️ Remove", key=f"remove_{i}"):
                    st.session_state.recipients.pop(i)
                    st.rerun()

    with st.expander("📥 Bulk Import"):
        bulk_recipients = st.text_area("Paste CSV (email,name,company per line)", 
        placeholder="example@example.com,John Doe,Example Inc.")
        if st.button("📤 Import Recipients"):
            lines = bulk_recipients.strip().split('\n')
            success, fail = 0, 0
            for line in lines:
                try:
                    email, name, company = [x.strip() for x in line.split(',')]
                    if is_valid_email(email):
                        st.session_state.recipients.append({
                            "email": email,
                            "name": name,
                            "company": company
                        })
                        success += 1
                    else:
                        fail += 1
                except:
                    fail += 1
            if success:
                st.success(f"Imported {success} recipients.")
            if fail:
                st.error(f"Failed to import {fail} lines.")
            if success:
                st.rerun()

    if st.session_state.recipients:
        template_lines = custom_template.split('\n')
        subject_template = "Fullstack Engineer Application"
        body_template = custom_template

        if template_lines[0].lower().startswith("title:"):
            subject_template = template_lines[0][6:].strip()
            body_template = '\n'.join(template_lines[1:])

        with st.expander("📬 Preview First Email"):
            first = st.session_state.recipients[0]
            subject = string.Template(subject_template).substitute(company=first['company'])
            body = string.Template(body_template).substitute(name=first['name'], company=first['company'])
            st.markdown("**Subject:**")
            st.write(subject)
            st.markdown("**Body:**")
            st.markdown(body)

        if st.button("🚀 Send Emails"):
            if not sender_email or not sender_password:
                st.error("Email credentials are required.")
                return

            success, failure = 0, 0
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, rec in enumerate(st.session_state.recipients):
                progress_bar.progress((i + 1) / len(st.session_state.recipients))
                status_text.text(f"Sending to {rec['email']}...")

                subject = string.Template(subject_template).substitute(company=rec['company'])
                body = string.Template(body_template).substitute(name=rec['name'], company=rec['company'])
                html_body = convert_markdown_to_html(body)

                sent, msg = send_email(sender_email, sender_password, sender_name, rec['email'], subject, html_body)
                if sent:
                    success += 1
                else:
                    st.warning(f"❌ {rec['email']} - {msg}")
                    failure += 1

            st.success(f"✅ Sent: {success}")
            if failure:
                st.error(f"❌ Failed: {failure}")
    else:
        st.info("Add at least one recipient to start sending emails.")

if __name__ == "__main__":
    main()