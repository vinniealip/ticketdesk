import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="📋 Dispatch Tracker - Ticket Logs", layout="wide")
st.title("📋 Ticket Log Form")

# --- Load dropdown settings ---
SETTINGS_FILE = "dropdown_settings.json"
TICKET_LOG_FILE = "ticket_logs.json"

# Load dropdown values
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {
        "projects": [],
        "issues": [],
        "isolation_status": [],
        "ticket_status": []
    }

# Load submitted ticket logs
def load_ticket_logs():
    if os.path.exists(TICKET_LOG_FILE):
        with open(TICKET_LOG_FILE, "r") as f:
            return json.load(f)
    return []

# Save updated logs
def save_ticket_logs(logs):
    with open(TICKET_LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

settings = load_settings()
logs = load_ticket_logs()

# --- Ticket Form ---
with st.form("ticket_form"):
    col1, col2 = st.columns(2)

    with col1:
        date_logged = st.date_input("Date Logged", value=datetime.today())
        project = st.selectbox("Project", settings.get("projects", []))
        issue = st.selectbox("Issue", settings.get("issues", []))
        ticket_number = st.text_input("Ticket Number")

    with col2:
        isolation_status = st.selectbox("Isolation Status", settings.get("isolation_status", []))
        ticket_status = st.selectbox("Ticket Status", settings.get("ticket_status", []))
        remarks = st.text_area("Remarks")

    submitted = st.form_submit_button("Save Ticket")

    if submitted:
        new_entry = {
            "Date": str(date_logged),
            "Project": project,
            "Issue": issue,
            "Ticket #": ticket_number,
            "Status": ticket_status,
            "Isolation": isolation_status,
            "Remarks": remarks
        }
        logs.append(new_entry)
        save_ticket_logs(logs)
        st.success("✅ Ticket saved!")
        st.experimental_rerun()

# --- Display ticket logs ---
if logs:
    st.subheader("📑 Submitted Tickets")
    df = pd.DataFrame(logs)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No tickets submitted yet.")
