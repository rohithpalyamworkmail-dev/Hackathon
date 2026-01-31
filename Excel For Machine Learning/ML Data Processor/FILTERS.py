import streamlit as st
import pandas as pd
import seaborn as sns
import janitor

if "allData" not in st.session_state:
    st.session_state["allData"] = {}

class Filters:
    def __init__(self, data):
        self.data = data

    def display(self):
        tab1, tab2 = st.tabs(["Perform Operations", "View Data"])
        
        with tab1:
            col1, col2 = st.columns([1, 2], gap="medium",border=True)
            col1.subheader("Please select the operation", divider='blue')
            
            options = col1.radio("Options", [
                "Is IN", "Where", "Mask", "Query", "Filter Columns Is In",
                 "Filter Date"
            ])
            
            if options == "Is IN":
                self.is_in(col1, col2)
            elif options == "Where":
                self.where(col1, col2)
            elif options == "Mask":
                self.mask(col1, col2)
            elif options == "Query":
                self.query(col1, col2)
            elif options == "Is NA":
                self.is_na(col1, col2)
            elif options == "Filter Columns Is In":
                self.filter_columns(col1, col2)
            elif options == "Filter On":
                self.filter_on(col1, col2)
            elif options == "Filter Date":
                self.filter_date(col1, col2)
            elif options == "Filter String":
                self.filter_string(col1, col2)
            elif options == "Find & Replace":
                self.find_replace(col1, col2)
        with tab2:
            st.subheader("Your Data",divider='blue')
            st.dataframe(self.data)
    
    def is_in(self, col1, col2):
        choice = col2.radio("Select Scope", ["Check values in entire data", "Check values in sub data"])
        
        if choice == "Check values in entire data":
            values = col2.text_input("Enter comma-separated values")
            if values:
                values_list = [eval(val.strip()) for val in values.split(",")]
                result = self.data.isin(values_list)
                col2.dataframe(result)
                st.session_state["allData"]["Stage - Filters - Is IN - Entire Data"] = result
        
        elif choice == "Check values in sub data":
            col_selection = col2.multiselect("Select columns", ["All"] + list(self.data.columns))
            row_selection = col2.multiselect("Select rows", ["All"] + list(self.data.index.astype(str)))
            values = col2.text_input("Enter comma-separated values")
            
            if values:
                values_list = [eval(val.strip()) for val in values.split(",")]
                selected_data = self.data.copy()
                
                if "All" not in col_selection:
                    selected_data = selected_data[col_selection]
                if "All" not in row_selection:
                    selected_data = selected_data.loc[row_selection]
                
                result = selected_data.isin(values_list)
                col2.dataframe(result)
                key = f"Stage - Filters - Is IN - Sub data - Columns: {col_selection}, Rows: {row_selection}"
                st.session_state["allData"][key] = result
    
    def where(self, col1, col2):
        condition = col2.text_input("Enter condition for where")
        other = col2.text_input("Enter replacement value (optional)")
        
        if condition:
            result = self.data.where(self.data.eval(condition), other if other else None)
            col2.dataframe(result)
            st.session_state["allData"]["Stage - Filters - Where"] = result
    
    def mask(self, col1, col2):
        condition = col2.text_input("Enter condition for mask")
        other = col2.text_input("Enter replacement value (optional)")
        
        if condition:
            result = self.data.mask(self.data.eval(condition), other if other else None)
            col2.dataframe(result)
            st.session_state["allData"]["Stage - Filters - Mask"] = result
    
    def query(self, col1, col2):
        query_string = col2.text_input("Enter query string")
        if query_string:
            result = self.data.query(query_string)
            col2.dataframe(result)
            st.session_state["allData"]["Stage - Filters - Query"] = result
    
    def filter_columns(self, col1, col2):
        column_name = col2.selectbox("Select column to filter", self.data.columns)
        values = col2.text_input("Enter comma-separated values")
        complement = col2.checkbox("Complement (Exclude selected values)", value=False)
        
        if values:
            values_list = [eval(val.strip()) for val in values.split(",")]
            result = self.data.filter_column_isin(column_name=column_name, iterable=values_list, complement=complement)
            col2.dataframe(result)
            st.session_state["allData"]["Stage - Filters - Filter Columns"] = result
    
    def filter_date(self, col1, col2):
        column_name = col2.selectbox("Select date column", self.data.columns)
        start_date = col2.date_input("Start Date")
        end_date = col2.date_input("End Date")
        
        if start_date and end_date:
            result = self.data.filter_date(column_name, start_date=start_date, end_date=end_date)
            col2.dataframe(result)
            st.session_state["allData"]["Stage - Filters - Filter Date"] = result
