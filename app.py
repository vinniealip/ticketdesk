# --- app.py ---
import streamlit as st
import json
import os

TICKET_LOG_FILE = "ticket_logs.json"
DROPDOWN_FILE = "dropdown_settings.json"

# Load or initialize dropdown values
if os.path.exists(DROPDOWN_FILE):
    with open(DROPDOWN_FILE, "r") as f:
        dropdowns = json.load(f)
else:
    dropdowns = {
        "projects": [],
        "issues": [],
        "isolation_status": [],
        "ticket_status": []
    }

# Load or initialize ticket logs
if os.path.exists(TICKET_LOG_FILE):
    with open(TICKET_LOG_FILE, "r") as f:
        ticket_logs = json.load(f)
else:
    ticket_logs = []

# Sidebar Navigation
st.sidebar.title("🎛️ Navigation")
page = st.sidebar.radio("Go to", ["Create Ticket", "Dashboard Tracker", "Settings"])

if page == "Create Ticket":
    st.title("📝 Create Ticket")

    with st.form("ticket_form"):
        project = st.selectbox("Project", dropdowns.get("projects", []))
        issue = st.selectbox("Issue", dropdowns.get("issues", []))
        isolation_status = st.selectbox("Isolation Status", dropdowns.get("isolation_status", []))
        ticket_status = st.selectbox("Ticket Status", dropdowns.get("ticket_status", []))
        ticket_details = st.text_area("Ticket Details")
        submitted = st.form_submit_button("Submit Ticket")

        if submitted and ticket_details:
            ticket = {
                "project": project,
                "issue": issue,
                "isolation_status": isolation_status,
                "ticket_status": ticket_status,
                "ticket_details": ticket_details
            }
            ticket_logs.append(ticket)
            with open(TICKET_LOG_FILE, "w") as f:
                json.dump(ticket_logs, f, indent=2)
            st.success("✅ Ticket submitted!")

elif page == "Dashboard Tracker":
    st.title("📊 Dashboard Tracker")

    if ticket_logs:
        edited_data = st.data_editor(ticket_logs, num_rows="dynamic")
        if st.button("💾 Save Changes"):
            with open(TICKET_LOG_FILE, "w") as f:
                json.dump(edited_data, f, indent=2)
            st.success("Changes saved successfully!")
    else:
        st.info("No tickets available.")

elif page == "Settings":
    st.title("⚙️ Dropdown Settings")

    for key in dropdowns:
        st.subheader(f"{key.replace('_', ' ').title()}")
        new_value = st.text_input(f"Add new {key.replace('_', ' ')}", key=f"input_{key}")
        if st.button(f"Add to {key.replace('_', ' ')}", key=f"button_{key}"):
            if new_value and new_value not in dropdowns[key]:
                dropdowns[key].append(new_value)
                with open(DROPDOWN_FILE, "w") as f:
                    json.dump(dropdowns, f, indent=2)
                st.success(f"Added '{new_value}' to {key}.")
                st.experimental_rerun()
        st.markdown("<ul>" + "".join([f"<li>{val}</li>" for val in dropdowns[key]]) + "</ul>", unsafe_allow_html=True)
