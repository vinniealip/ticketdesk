import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Dispatch Tracker", layout="wide")

st.title("📋 Dispatch Tracker Web App")

# Use your actual Excel file name
EXCEL_PATH = "Ticket and Dispatch Tracker.xlsx"

try:
    xlsx = pd.ExcelFile(EXCEL_PATH)

    # Check for the correct sheet
    if "Dispatch Tracker" in xlsx.sheet_names:
        df = xlsx.parse("Dispatch Tracker", skiprows=1)  # skip header row if needed

        st.subheader("🧾 Current Dispatch Records")
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

        # Apply Isolation Status logic
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

                    for col in [
                        "Dispatch Type", "Turnover Date", "Service Provider",
                        "Acknowledgement Date", "Scheduled Dispatch Date", "Personnel Names",
                        "Dispatch Remarks", "Actual Dispatch Date", "Dispatch Status",
                        "Assessment / Formal Report", "Quotation"
                    ]:
                        edited_df.at[i, col] = "Not Applicable"

                elif row.get("Isolation Status") == "Ongoing":
                    edited_df.at[i, "Ticket Status"] = "Open Ticket (Pending)"

        # Download updated CSV
        csv = edited_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Updated CSV", csv, "updated_dispatch.csv", "text/csv")
    else:
        st.error("Sheet 'Dispatch Tracker' not found in the Excel file.")

except FileNotFoundError:
    st.error(f"Excel file '{EXCEL_PATH}' not found. Please place it in the same folder as app.py.")
