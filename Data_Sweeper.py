import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

st.markdown(
    """
    <style>
        .main {
            background: radial-gradient(circle, #141414, #0a0a0a);
            padding: 1.5rem;
        }
        h1, h2, h3 {
            color: #a1d8ff;
            font-family: 'Helvetica', sans-serif;
            letter-spacing: 1px;
        }
        .stButton>button {
            background: linear-gradient(45deg, #0066cc, #003366);
            border: none;
            border-radius: 12px;
            color: #f0f0f0;
            padding: 0.9rem 2rem;
            font-size: 1.2rem;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 18px rgba(0, 102, 204, 0.5);
        }
        .stDataFrame {
            background: #222224;
            border-radius: 15px;
            border: 1px solid #505050;
            padding: 1rem;
        }
        .stText, .stRadio>label, .stCheckbox>label {
            color: #d9d9d9;
            font-family: 'Helvetica', sans-serif;
            font-size: 1.1rem;
        }
        .stDownloadButton>button {
            background: linear-gradient(45deg, #2ecc71, #27ae60);
            border-radius: 12px;
            color: #f0f0f0;
            padding: 0.9rem 2rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .stDownloadButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 18px rgba(46, 204, 113, 0.5);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='app-container'>", unsafe_allow_html=True)
st.title("Data Sweeper")
st.write("Mold your data into perfection with seamless transformations.")

file_drop = st.file_uploader("Insert CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if file_drop:
    for data_file in file_drop:
        ext = os.path.splitext(data_file.name)[-1].lower()

        if ext == ".csv":
            dataset = pd.read_csv(data_file)
        elif ext == ".xlsx":
            dataset = pd.read_excel(data_file)
        else:
            st.error(f"Invalid format detected: {ext}")
            continue

        st.write(f"🗂️ Source: {data_file.name}")
        st.write(f"📐 Scale: {data_file.size / 1024:.2f} KB")
        st.write("First Glance:")
        st.dataframe(dataset.head())

        st.subheader("Purification Chamber")
        if st.checkbox(f"Refine {data_file.name}"):
            left, right = st.columns(2)
            with left:
                if st.button(f"Strip Repeats - {data_file.name}"):
                    dataset.drop_duplicates(inplace=True)
                    st.write("Repeats Eliminated!")
            with right:
                if st.button(f"Mend Voids - {data_file.name}"):
                    num_fields = dataset.select_dtypes(include=['number']).columns
                    dataset[num_fields] = dataset[num_fields].fillna(dataset[num_fields].mean())
                    st.write("Voids Repaired!")

        st.subheader("Element Selector")
        fields = st.multiselect(f"Extract Elements from {data_file.name}", dataset.columns, default=dataset.columns)
        dataset = dataset[fields]

        st.subheader("Insight Forge")
        if st.checkbox(f"Reveal Patterns in {data_file.name}"):
            st.bar_chart(dataset.select_dtypes(include='number').iloc[:, :2])

        st.subheader("Transmutation Vault")
        output_form = st.radio(f"Reform {data_file.name} as:", ["CSV", "Excel"], key=data_file.name)
        if st.button(f"Transmute {data_file.name}"):
            output_stream = BytesIO()
            if output_form == "CSV":
                dataset.to_csv(output_stream, index=False)
                new_name = data_file.name.replace(ext, ".csv")
                file_type = "text/csv"
            else:
                dataset.to_excel(output_stream, index=False, engine='openpyxl')
                new_name = data_file.name.replace(ext, ".xlsx")
                file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            output_stream.seek(0)

            st.download_button(
                label=f"Extract {data_file.name} as {output_form}",
                data=output_stream,
                file_name=new_name,
                mime=file_type
            )

st.success("✨ Transformation complete!")
st.markdown("</div>", unsafe_allow_html=True)
