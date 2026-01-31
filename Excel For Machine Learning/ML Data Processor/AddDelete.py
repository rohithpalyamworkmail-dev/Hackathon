import pandas as pd
import streamlit as st
import numpy as np
import chardet

class AddDelete:
    def __init__(self, df):
        self.data = df
        if "allData" not in st.session_state:
            st.session_state["allData"] = {}

    def display(self):
        tab1, tab2 = st.tabs(["Perform Operations", "View Data"])
        
        with tab1:
            col1, col2 = st.columns([1, 2], border=True)
            col1.subheader("Select the operation that you want to perform", divider='blue')
            options = col1.radio("Options", ["Add", "Delete"])
            
            if options == "Add":
                self.add(col2)
            elif options == "Delete":
                self.delete(col2)
        
        with tab2:
            st.markdown("**Your Data**")
            st.dataframe(self.data)

    def add(self, col2):
        col2.subheader("You Implement Add Operation Here", divider='blue')
        options = col2.selectbox("Select the option to add", ["Add Columns", "Add Rows"])
        extractedColumns = list(self.data.columns)
    
        if options == "Add Columns":
            col2.info("Upload a dataset with the same column names and the same number of rows")
            file = col2.file_uploader("Upload the file", type=["csv", "xlsx"])
    
            join_type = col2.radio("Join Type", ["outer", "inner"], index=0)
            ignore_index = col2.checkbox("Ignore Index", value=True)
            verify_integrity = col2.checkbox("Verify Integrity", value=False)
            copy_data = col2.checkbox("Copy Data", value=True)
    
            if file:
                dataFrame = self.parseFile(file)
                if dataFrame is not None:
                    if dataFrame.shape[0] != self.data.shape[0]:
                        col2.warning("Row count mismatch! Ensure the uploaded file has the same number of rows.")
                        return
    
                    new_columns = extractedColumns + [x + "1" if x in extractedColumns else x for x in list(dataFrame.columns)]
                    data = pd.concat([self.data, dataFrame],
                                     axis=1,
                                     join=join_type,
                                     copy=copy_data)
                    data.columns = new_columns
    
                    key = "Stage - Add & Delete - Add Columns Through File Uploader"
                    st.session_state["allData"][key] = data
                    col2.dataframe(data)
                else:
                    col2.error("Could not read the file. Please check the format.")
    
        elif options == "Add Rows":
            col2.info("Upload a dataset with the same column names to append rows")
            file = col2.file_uploader("Upload the file", type=["csv", "xlsx"])
    
            ignore_index = col2.checkbox("Ignore Index", value=True)
            verify_integrity = col2.checkbox("Verify Integrity", value=False)
            copy_data = col2.checkbox("Copy Data", value=True)
    
            if file:
                dataFrame = self.parseFile(file)
                if dataFrame is not None:
                    if set(dataFrame.columns) != set(self.data.columns):
                        col2.warning("Column names mismatch! Ensure the uploaded file has the same columns.")
                        return
    
                    data = pd.concat([self.data, dataFrame],
                                     axis=0,
                                     ignore_index=ignore_index,
                                     verify_integrity=verify_integrity,
                                     copy=copy_data)
    
                    key = "Stage - Add & Delete - Add Rows Through File Uploader"
                    st.session_state["allData"][key] = data
                    col2.dataframe(data)
                else:
                    col2.error("Could not read the file. Please check the format.")

    def delete(self, col2):
        col2.subheader("You Implement Delete Operation Here", divider='blue')
        options = col2.selectbox("Select the option to delete", 
                                 ["Delete Columns", "Delete Rows", "Delete Duplicated Rows", "Delete Missing Values"])
        
        if options == "Delete Columns":
            columns = col2.multiselect("Select columns to delete", self.data.columns)
            
            if columns and col2.button("Delete Selected Columns", use_container_width=True, type='primary'):
                data=self.data.drop(columns=columns, axis=1)
                st.session_state["allData"]["Stage - Add & Delete - Delete Columns"] = data
                col2.dataframe(data)

        elif options == "Delete Rows":
            rows = col2.multiselect("Select indexes to remove", self.data.index)
            
            if rows and col2.button("Delete Selected Rows", use_container_width=True, type="primary"):
                dataframe=self.data.drop(index=rows, axis=0)
                st.session_state["allData"]["Stage - Add & Delete - Delete Rows"] = dataframe
                col2.dataframe(dataframe)

        elif options == "Delete Duplicated Rows":
            before = self.data.shape[0]
            data=self.data.drop_duplicates()
            after = data.shape[0]
            removed = before - after

            st.session_state["allData"]["Stage - Add & Delete - Delete Duplicates"] = data
            col2.success(f"Removed {removed} duplicated rows.")
            col2.dataframe(data)

        elif options == "Delete Missing Values":
            before = self.data.shape[0]
            data=self.data.dropna()
            after = data.shape[0]
            removed = before - after

            st.session_state["allData"]["Stage - Add & Delete - Delete Missing Values"] = data
            col2.success(f"Removed {removed} rows with missing values.")
            col2.dataframe(data)

    def parseFile(self, file):
      """Parses an uploaded CSV or Excel file, handling encoding issues using chardet."""
      try:
          # Read the first few bytes of the file to detect the encoding
          raw_data = file.read(10000)
          result = chardet.detect(raw_data)
          encoding = result['encoding']
          file.seek(0)  # Reset the file pointer to the start
  
          if file.name.endswith(".csv"):
              # Attempt to read CSV using detected encoding
              try:
                  df = pd.read_csv(file, encoding=encoding)
              except UnicodeDecodeError:
                  # If there's still an issue, try with a fallback encoding
                  file.seek(0)  # Reset file pointer
                  df = pd.read_csv(file, encoding="ISO-8859-1")  # Fallback encoding
  
          elif file.name.endswith(".xlsx"):
              # For Excel files, just attempt to read them with the default engine
              df = pd.read_excel(file, engine="openpyxl")
  
          return df
  
      except Exception as e:
          st.error(f"Error reading file: {e}")
          return None
