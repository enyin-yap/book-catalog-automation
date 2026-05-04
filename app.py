import streamlit as st
import tempfile

from src.pipeline.catalog_pipeline import run_pipeline


st.title("Book Catalog Metadata Pipeline")

uploaded_file = st.file_uploader("Upload your ISBN CSV", type=["csv"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.getvalue())
        input_path = tmp.name

    st.success("File uploaded successfully!")

    if st.button("Run Pipeline"):
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name

        with st.spinner("Processing..."):
            run_pipeline(input_path, output_path)

        st.success("Done!")

        with open(output_path, "rb") as f:
            st.download_button(
                label="Download Excel Output",
                data=f,
                file_name="book_metadata_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )