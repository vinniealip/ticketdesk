import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(page_title="Dispatch Tracker", layout="wide")

st.title("📋 Dispatch Tracker - Ticket Logs")

# --- Persistent Storage Setup ---
DATA_FILE = "ticket_log.json"

# Load or initialize ticket log
if DATA_FILE not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state[DATA_FILE] = pd.read_json(DATA_FILE)
    else:
        st.session_state[DATA_FILE] = pd.DataFrame(columns=[
            "Ticket #", "Issue", "Project", "Site", "Incident Date",
            "Isolation Status", "Ticket Status", "Remarks",
            "Assessment / Resolution Date"
        ])

tickets_df = st.session_state[DATA_FILE]

# Load dropdown values from session state
project_options = st.session_state.get("projects", [])
issue_options = st.session_state.get("issues", [])
isolation_status_options = st.session_state.get("isolation_status", [])
ticket_status_options = st.session_state.get("ticket_status", [])

# Dynamic project-to-site mapping (simplified example)
project_site_map = {
    "Bluewave 1.0": ["Main Office", "Manila North Harbor Port"],
    "Bluewave 1.1": ["Port of Babak", "Port of Balbagon"],
    "Bluewave 1.2": ["Port of Lucena", "Port of Bulan"],
    "Bluewave 1.3": ["Port of Jordan", "Port of Naval"],
    "Bluewave 1.4": ["NCR North Admin Bldg", "NCR South PTB"],
    "Cottage": ["FDC Misamis Power Plant"],
    "GoSurv": ["URC Calamba Plant 1", "URC Pampanga"],
    "Prada": ["Apex Cold Storage"],
    "Shaw": ["Wack Wack Golf & Country Club"]
}

# Form to add a new ticket
with st.expander("➕ Add New Ticket"):
    with st.form("add_ticket_form"):
        ticket_num = st.text_input("Ticket #")
        issue = st.selectbox("Issue", sorted(issue_options))
        project = st.selectbox("Project", sorted(project_options))

        # Dynamically choose site based on project
        site_options = project_site_map.get(project, ["Other"])
        site = st.selectbox("Site", sorted(site_options))

        incident_date = st.date_input("Incident Date", datetime.today())
        submitted = st.form_submit_button("Add Ticket")

        if submitted:
            new_ticket = {
                "Ticket #": ticket_num,
                "Issue": issue,
                "Project": project,
                "Site": site,
                "Incident Date": incident_date.strftime("%Y-%m-%d"),
                "Isolation Status": "Ongoing",
                "Ticket Status": "Open Ticket (Pending)",
                "Remarks": "",
                "Assessment / Resolution Date": ""
            }
            tickets_df = pd.concat([
                tickets_df,
                pd.DataFrame([new_ticket])
            ], ignore_index=True)
            tickets_df.to_json(DATA_FILE, orient="records")
            st.session_state[DATA_FILE] = tickets_df
            st.success(f"Ticket #{ticket_num} added.")

# Edit and apply logic
st.subheader("📄 Existing Tickets")
edited_df = st.data_editor(
    tickets_df,
    num_rows="dynamic",
    use_container_width=True,
    key="ticket_editor"
)

# Apply auto-updates based on Isolation Status
if st.button("🧠 Apply Isolation Status Logic"):
    status_resolved = ["Resolved", "Resolved (PLDT)", "Resolved (Power)"]
    current_date = datetime.today().strftime("%Y-%m-%d")

    for i, row in edited_df.iterrows():
        if row.get("Isolation Status") in status_resolved:
            edited_df.at[i, "Assessment / Resolution Date"] = current_date
            edited_df.at[i, "Remarks"] = {
                "Resolved (PLDT)": "Network Resolved by PLDT",
                "Resolved (Power)": "Power Resolved on Site"
            }.get(row["Isolation Status"], "Resolved during Isolation")
            edited_df.at[i, "Ticket Status"] = "Completed - Closed Ticket"
        elif row.get("Isolation Status") == "Ongoing":
            edited_df.at[i, "Ticket Status"] = "Open Ticket (Pending)"

    edited_df.to_json(DATA_FILE, orient="records")
    st.session_state[DATA_FILE] = edited_df
    st.success("Logic applied to Isolation Status updates.")

# Download updated data
csv = edited_df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Tickets as CSV", csv, "ticket_log.csv", "text/csv")
