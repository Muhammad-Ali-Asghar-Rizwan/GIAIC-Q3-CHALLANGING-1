import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Configure Page
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Sidebar (Left Panel)
with st.sidebar:
    # st.image("https://via.placeholder.com/150", width=150)  # Replace with your image URL or file path
    st.title("User Input")
    user_name = st.text_input("Enter your name:", placeholder="Ali Asghar")
    st.write(f"👋 Welcome, {user_name}!" if user_name else "👋 Welcome, Guest!")

    # File Uploader
    uploaded_files = st.file_uploader(
        "📂 Upload your CSV or Excel file",
        type=["csv", "xlsx"],
        accept_multiple_files=True,
    )

# Main Content
st.title("💽 Data Sweeper - Sterling Integrator")
st.write("🚀 Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")  # Ensure openpyxl is used
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # Display File Information
        st.subheader(f"📄 File Details: {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")
        st.dataframe(df.head())  # Show first 5 rows

        # Data Cleaning Options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Enable Cleaning for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Remove Duplicates ({file.name})"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed")

            with col2:
                if st.button(f"🛠️ Fill Missing Values ({file.name})"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Filled")

        # Select Columns to Keep
        st.subheader("🔄 Select Columns")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Graph for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # File Conversion Options
        st.subheader("🔄 Convert File Format")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        # Initialize buffer before conversion
        buffer = BytesIO()
        file_name, mime_type = "", ""

        if st.button(f"💾 Convert {file.name}"):
            buffer = BytesIO()
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
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
            )

        st.success("🎉 Processing Completed Successfully!")
