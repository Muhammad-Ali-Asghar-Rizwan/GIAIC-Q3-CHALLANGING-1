import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS styles
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("💽 Data Sweeper Sterling Integrator By Ali Asghar")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for Quarter 3!")

# File uploader
uploaded_files = st.file_uploader("Upload your CSV or Excel file here", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")  # Ensure openpyxl is used
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display file information
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # Show first 5 rows of the DataFrame
        st.write("Preview the Head of the DataFrame")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates From {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Filled with Mean!")

        # Choose Specific Columns to Keep or Convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Create Some Visualizations
        st.subheader("💥 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # File Conversion Options
        st.subheader("🔔 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        # Initialize buffer before conversion
        buffer = BytesIO()
        file_name = ""
        mime_type = ""

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()  # Create a new buffer
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"🔗 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

        st.success("😜 All files processed successfully!")
