# --- utils/data_handler.py ---
import json
import os
import pandas as pd
from datetime import datetime

DATA_DIR = "data"
TICKET_FILE = os.path.join(DATA_DIR, "ticket_logs.json")
DROPDOWN_FILE = os.path.join(DATA_DIR, "dropdown_settings.json")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")

DEFAULT_DROPDOWNS = {
    "ticket_status": [],
    "issue": [],
    "project": [],
    "site": [],
    "isolation_status": []
}

def load_tickets():
    if os.path.exists(TICKET_FILE):
        with open(TICKET_FILE, "r") as f:
            return json.load(f)
    return []

def save_tickets(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(TICKET_FILE, "w") as f:
        json.dump(data, f, indent=2)
    backup_path = os.path.join(BACKUP_DIR, f"tickets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    with open(backup_path, "w") as f:
        json.dump(data, f, indent=2)

def load_dropdowns():
    if os.path.exists(DROPDOWN_FILE):
        with open(DROPDOWN_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_DROPDOWNS.copy()

def save_dropdowns(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DROPDOWN_FILE, "w") as f:
        json.dump(data, f, indent=2)

def export_tickets_to_csv(df):
    df.to_csv("ticket_export.csv", index=False)
    with open("ticket_export.csv", "rb") as f:
        st.download_button("Download CSV", f, file_name="ticket_export.csv")

def export_tickets_to_excel(df):
    df.to_excel("ticket_export.xlsx", index=False)
    with open("ticket_export.xlsx", "rb") as f:
        st.download_button("Download Excel", f, file_name="ticket_export.xlsx")
