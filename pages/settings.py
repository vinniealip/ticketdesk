import streamlit as st
import json
import os

st.set_page_config(page_title="Dropdown Settings", layout="wide")
st.title("⚙️ Admin: Edit Dropdown Lists")

# --- Persistent Storage Setup ---
SETTINGS_FILE = "dropdown_settings.json"

# Load saved settings or fallback to empty
if SETTINGS_FILE not in st.session_state:
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            st.session_state[SETTINGS_FILE] = json.load(f)
    else:
        st.session_state[SETTINGS_FILE] = {
            "projects": [],
            "issues": [],
            "isolation_status": [],
            "ticket_status": []
        }

settings = st.session_state[SETTINGS_FILE]

# Save function
def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

# Editable fields
dropdown_fields = {
    "Projects": "projects",
    "Issues": "issues",
    "Isolation Status": "isolation_status",
    "Ticket Status": "ticket_status"
}

for label, key in dropdown_fields.items():
    st.subheader(f"{label}")
    if key not in settings:
        settings[key] = []

    new_value = st.text_input(f"Add new {label}", key=f"new_{key}")
    if st.button(f"➕ Add to {label}", key=f"add_{key}"):
        cleaned = new_value.strip()
        if cleaned and cleaned not in settings[key]:
            settings[key].append(cleaned)
            save_settings()
            st.success(f"Added: {cleaned}")
            st.session_state[f"new_{key}"] = ""  # Clear input manually
        else:
            st.warning("Value already exists or is empty.")

    to_remove = st.multiselect(f"Remove from {label}", settings[key], key=f"remove_{key}")
    if st.button(f"❌ Remove selected from {label}", key=f"removebtn_{key}") and to_remove:
        settings[key] = [item for item in settings[key] if item not in to_remove]
        save_settings()
        st.success(f"Removed: {', '.join(to_remove)}")
        st.session_state[f"remove_{key}"] = []

# Sync into session state
for key in settings:
    st.session_state[key] = settings[key]
