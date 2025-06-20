import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="📋 Dispatch Tracker - Ticket Logs", layout="wide")
st.title("📋 Ticket Log Form")

# --- Load dropdown settings ---
SETTINGS_FILE = "dropdown_settings.json"

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

settings = load_settings()

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
        # Placeholder save logic for now
        st.success(f"Ticket for '{project}' logged successfully!")
        st.write("**Details:**")
        st.write({
            "Date": str(date_logged),
            "Project": project,
            "Issue": issue,
            "Ticket #": ticket_number,
            "Status": ticket_status,
            "Isolation": isolation_status,
            "Remarks": remarks
        })
