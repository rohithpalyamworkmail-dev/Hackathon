import pandas as pd
import streamlit as st
import numpy as np
import io

class Exports:
    def __init__(self, df):
        self.dataset = df

    def display(self):
        tab1, tab2 = st.tabs(["View Operations", "View Data"])

        with tab1:
            col1, col2 = st.columns([1, 2], border=True)

            options = col1.radio("Options", [
                "To ORC", "To Parquet", "To Pickle", "To Feather", "To CSV",
                "To SQL", "To HDF5", "To JSON", "To Dict", "To HTML", "To LaTeX", 
                "To Stata", 
                "To Clipboard"
            ])

            file_buffer = io.BytesIO()  # In-memory storage
            mime_type = None
            file_name = None
            show_inputs = False  # Whether extra inputs are needed

            if options == "To ORC":
                file_name = "exported_data.orc"
                self.dataset.to_orc(file_buffer, engine="pyarrow")
                mime_type = "application/octet-stream"

            elif options == "To Parquet":
                file_name = "exported_data.parquet"
                self.dataset.to_parquet(file_buffer, compression="snappy")
                mime_type = "application/octet-stream"

            elif options == "To Pickle":
                file_name = "exported_data.pkl"
                self.dataset.to_pickle(file_buffer, compression="gzip")
                mime_type = "application/octet-stream"

            elif options == "To Feather":
                file_name = "exported_data.feather"
                self.dataset.to_feather(file_buffer)
                mime_type = "application/octet-stream"

            elif options == "To CSV":
                file_name = "exported_data.csv"
                self.dataset.to_csv(file_buffer, index=False)
                mime_type = "text/csv"

            elif options == "To SQL":
                show_inputs = True
                sql_table_name = col1.text_input("Enter SQL Table Name")
                db_uri = col1.text_input("Enter Database URI")
                if col1.button("Export to SQL"):
                    from sqlalchemy import create_engine
                    engine = create_engine(db_uri)
                    self.dataset.to_sql(sql_table_name, con=engine, if_exists="replace")
                    col2.success(f"Data exported to SQL table: {sql_table_name}")

            elif options == "To HDF5":
                show_inputs = True
                hdf_key = col1.text_input("Enter HDF5 Key")
                file_name = "exported_data.h5"
                if col1.button("Export to HDF5"):
                    self.dataset.to_hdf(file_name, key=hdf_key, mode="w")
                    col2.success(f"Data exported to {file_name}")

            elif options == "To JSON":
                file_name = "exported_data.json"
                self.dataset.to_json(file_buffer, orient="records")
                mime_type = "application/json"

            elif options == "To Dict":
                col2.json(self.dataset.to_dict())
                
            elif options == "To HTML":
                file_name = "exported_data.html"
                html_data = self.dataset.to_html()  # Generate HTML string
                file_buffer.write(html_data.encode("utf-8"))  # Convert string to bytes
                file_buffer.seek(0)  # Reset buffer position
                mime_type = "text/html"

            elif options == "To LaTeX":
                file_name = "exported_data.tex"
                latex_data = self.dataset.to_latex()  # Generate LaTeX string
                file_buffer.write(latex_data.encode("utf-8"))  # Convert string to bytes
                file_buffer.seek(0)  # Reset buffer position
                mime_type = "text/x-tex"

            elif options == "To Stata":
                file_name = "exported_data.dta"
                
                # Ensure column names are valid (max 32 chars)
                self.dataset.columns = [col[:32] for col in self.dataset.columns]
            
                # Truncate string columns to 244 characters (Stata limit)
                for col in self.dataset.select_dtypes(include=['object']):
                    self.dataset[col] = self.dataset[col].astype(str).str[:244]
            
                # Convert to Stata format and write to buffer
                self.dataset.to_stata(file_buffer, write_index=False)
                file_buffer.seek(0)  # Reset buffer position
                mime_type = "application/x-stata"

            elif options == "To String":
                col2.text(self.dataset.to_string())

            elif options == "To Clipboard":
                file_name = "exported_data_clipboard.txt"
            
                # Convert dataframe to a clipboard-friendly format (TSV)
                clipboard_text = self.dataset.to_csv(sep="\t", index=False)
            
                # Show data in a text box for manual copying
                col2.text_area("Copy the Data Below:", clipboard_text, height=300)
            
                # Provide a download button instead
                col2.download_button(
                    label="Download as Text File",
                    data=clipboard_text,
                    file_name=file_name,
                    mime="text/plain"
                )
            # Show Download Button if applicable
            col2.subheader("Click The Button Below To Download The Data",divider='blue')
            if file_name and not show_inputs:
                file_buffer.seek(0)  # Reset pointer
                col2.download_button(
                    label="Download File",
                    data=file_buffer,
                    file_name=file_name,
                    mime=mime_type,
                    use_container_width=True,
                    type='primary'
                )

        with tab2:
            st.subheader("View Data", divider='blue')
            st.dataframe(self.dataset)
