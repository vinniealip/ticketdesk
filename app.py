# --- app.py ---
import streamlit as st
from utils.data_handler import load_dropdowns, load_tickets, save_tickets, save_dropdowns, export_tickets_to_csv, export_tickets_to_excel
import pandas as pd
import os

st.set_page_config(page_title="📋 Ticket Tracker", layout="wide")

# Load data
dropdowns = load_dropdowns()
tickets = load_tickets()

# Sidebar Navigation
st.sidebar.title("🎛️ Navigation")
page = st.sidebar.radio("Go to", ["Ticket Dashboard", "Settings"])

if page == "Ticket Dashboard":
    st.title("📝 Ticket Dashboard")

    edited_df = st.data_editor(
        pd.DataFrame(tickets),
        num_rows="dynamic",
        use_container_width=True,
        key="ticket_editor"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Changes"):
            save_tickets(edited_df.to_dict(orient="records"))
            st.success("Tickets saved successfully!")
    with col2:
        export_format = st.selectbox("Export format", ["CSV", "Excel"])
        if st.button("📤 Export Tickets"):
            if export_format == "CSV":
                export_tickets_to_csv(edited_df)
            else:
                export_tickets_to_excel(edited_df)

elif page == "Settings":
    st.title("⚙️ Dropdown Settings")

    for category, options in dropdowns.items():
        st.subheader(f"{category.replace('_', ' ').title()}")
        new_option = st.text_input(f"Add to {category}", key=f"input_{category}")
        if st.button(f"➕ Add", key=f"btn_add_{category}"):
            if new_option and new_option not in options:
                options.append(new_option)
                save_dropdowns(dropdowns)
                st.success(f"Added '{new_option}' to {category}.")
                st.experimental_rerun()

        # Show current values and allow deletion
        to_delete = st.multiselect(f"Select {category} entries to delete:", options, key=f"del_{category}")
        if st.button(f"❌ Delete Selected from {category}", key=f"btn_del_{category}"):
            dropdowns[category] = [opt for opt in options if opt not in to_delete]
            save_dropdowns(dropdowns)
            st.success(f"Removed selected entries from {category}.")
            st.experimental_rerun()

        st.markdown("<ul>" + "".join([f"<li>{opt}</li>" for opt in dropdowns[category]]) + "</ul>", unsafe_allow_html=True)
