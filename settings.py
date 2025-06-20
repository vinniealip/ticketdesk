import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Dispatch Tracker", layout="wide")

st.title("📋 Dispatch Tracker - Ticket Logs")

# Fallback defaults if session state not set
project_options = st.session_state.get("projects", ["Bluewave 1.0", "Bluewave 1.1"])
issue_options = st.session_state.get("issues", ["Camera Down", "Site Down"])
isolation_status_options = st.session_state.get("isolation_status", ["Ongoing", "Resolved"])
ticket_status_options = st.session_state.get("ticket_status", ["Open Ticket (Pending)", "Completed - Closed Ticket"])

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

# Initialize or simulate in-memory ticket data
if "tickets" not in st.session_state:
    st.session_state.tickets = pd.DataFrame(columns=[
        "Ticket #", "Issue", "Project", "Site", "Incident Date",
        "Isolation Status", "Ticket Status", "Remarks",
        "Assessment / Resolution Date"
    ])

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
            st.session_state.tickets = pd.concat([
                st.session_state.tickets,
                pd.DataFrame([new_ticket])
            ], ignore_index=True)
            st.success(f"Ticket #{ticket_num} added.")

# Edit and apply logic
st.subheader("📄 Existing Tickets")
edited_df = st.data_editor(
    st.session_state.tickets,
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

    st.session_state.tickets = edited_df.copy()
    st.success("Logic applied to Isolation Status updates.")

# Download updated data
csv = edited_df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download Tickets as CSV", csv, "ticket_log.csv", "text/csv")
