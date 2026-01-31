import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import *
import seaborn as sns

class AccessModify:
    def __init__(self, df):
        self.df = df
        if "allData" not in st.session_state:
            st.session_state["allData"] = {}

    def display(self):
        tab1, tab2 = st.tabs(['Perform Operations', 'View Your Results'])
        
        with tab1:
            col1, col2 = st.columns([1, 2],border=True)
            
            options = col1.radio("Please select the operation that you want to perform", 
                                ['Access Data', 'Access Data (Advanced)'])
            
            if options == 'Access Data':
                self.access_data(col1, col2)
            elif options == 'Access Data (Advanced)':
                self.access_data_advanced(col2)
            elif options == 'Modify Values':
                st.warning("Feature not implemented yet.")
            elif options == 'Modify Values (Advanced)':
                st.warning("Feature not implemented yet.")
        
        with tab2:
            st.subheader("Stored Results", divider='green')
            if st.session_state["allData"]:
                for key, value in st.session_state["allData"].items():
                    st.write(f"**{key}**")
                    st.dataframe(value)
            else:
                st.info("No stored results yet.")

    def access_data(self, col1, col2):
        col2.subheader("Please select an option", divider='green')
        options = col2.radio("Options", 
                            ['Access first n rows', 'Access last n rows', 'Access Sample Data', 'Access Filtered Data'])
        
        if options == 'Access first n rows':
            self.access_first_n_rows(col2)
        elif options == 'Access last n rows':
            self.access_last_n_rows(col2)
        elif options == 'Access Sample Data':
            self.access_sample_data(col2)
        elif options == 'Access Filtered Data':
            self.access_filtered_data(col2)

    def access_first_n_rows(self, col2):
        col2.subheader("Provide input for selected option", divider='green')
        slider = col2.slider("Drag to select number of rows", 1, self.df.shape[0])
        columns = col2.multiselect("Select the columns", ['All Columns'] + list(self.df.columns))
        
        if col2.button("Fix My Settings", use_container_width=True, type='primary'):
            if not columns:
                col2.warning("You must select at least one column.")
                return
            
            if "All Columns" in columns:
                selected_data = self.df.head(slider)
            else:
                selected_data = self.df.head(slider)[columns]
            
            key = f"Stage - Access & Modify - First {slider} Rows with columns - {columns}"
            st.session_state["allData"][key] = selected_data
            
            col2.subheader("Your Results", divider='grey')
            col2.dataframe(selected_data)

    def access_last_n_rows(self, col2):
        col2.subheader("Provide input for selected option", divider='green')
        slider = col2.slider("Drag to select number of rows", 1, self.df.shape[0])
        columns = col2.multiselect("Select the columns", ['All Columns'] + list(self.df.columns))
        
        if col2.button("Fix My Settings", use_container_width=True, type='primary'):
            if not columns:
                col2.warning("You must select at least one column.")
                return
            
            if "All Columns" in columns:
                selected_data = self.df.tail(slider)
            else:
                selected_data = self.df.tail(slider)[columns]
            
            key = f"Stage - Access & Modify - Last {slider} Rows with columns - {columns}"
            st.session_state["allData"][key] = selected_data
            
            col2.subheader("Your Results", divider='grey')
            col2.dataframe(selected_data)

    def access_sample_data(self, col2):
        col2.subheader("Provide input for selected option", divider='green')
        sample_size = col2.slider("Select number of random samples", 1, self.df.shape[0])
        columns = col2.multiselect("Select the columns", ['All Columns'] + list(self.df.columns))
        
        if col2.button("Fix My Settings", use_container_width=True, type='primary'):
            if not columns:
                col2.warning("You must select at least one column.")
                return
            
            if "All Columns" in columns:
                selected_data = self.df.sample(sample_size)
            else:
                selected_data = self.df.sample(sample_size)[columns]
            
            key = f"Stage - Access & Modify - Sample {sample_size} Rows with columns - {columns}"
            st.session_state["allData"][key] = selected_data
            
            col2.subheader("Your Results", divider='grey')
            col2.dataframe(selected_data)
    # pass
    def access_filtered_data(self, col2):
        col2.subheader("Pass Input for the selected option", divider='green')
        
        axis = col2.selectbox("Specify the axis", ['index', 'columns'])
        
        if axis == 'index':
            self.selected_items = list(self.df.index)
        else:
            self.selected_items = list(self.df.columns)
    
        filter_option = col2.radio("Choose a filtering method", ["Items", "Like", "Regex"])
        
        selected_items, like, regex = None, None, None
    
        if filter_option == "Items":
            selected_items = col2.multiselect("Select specific rows or columns", ["All"] + self.selected_items)
            if "All" in selected_items:
                selected_items = None  # Ignore 'All' and select everything
        elif filter_option == "Like":
            like = col2.text_input("Enter substring to filter (e.g., 'rab' for 'rabbit')")
        elif filter_option == "Regex":
            regex = col2.text_input("Enter regex pattern")
    
        if col2.button("Apply Filter", use_container_width=True, type='primary'):
            try:
                if selected_items:
                    selected_data = self.df.filter(items=selected_items, axis=0 if axis == "index" else 1)
                elif like:
                    selected_data = self.df.filter(like=like, axis=0 if axis == "index" else 1)
                elif regex:
                    selected_data = self.df.filter(regex=regex, axis=0 if axis == "index" else 1)
                else:
                    col2.warning("No valid filtering criteria provided.")
                    return
    
                key = f"Filtered Data - {filter_option} - {selected_items if selected_items else like if like else regex}"
                st.session_state["allData"][key] = selected_data
    
                col2.subheader("Your Results", divider='grey')
                col2.dataframe(selected_data)
    
            except Exception as e:
                col2.warning(f"Error: {e}")
    def access_data_advanced(self,col2):
        col2.subheader("Please select an option",divider='green')
        options=col2.radio("Options",["Desired Rows And Columns","Portion Of Rows And Columns","Trucante Data","Boolean Conditions"])
        if options=="Desired Rows And Columns":
            self.desired_rows_and_columns(col2)
        if options=="Portion Of Rows And Columns":
            self.portion_rows_and_columns(col2)
        if options=="Trucante Data":
            self.truncate_data(col2)
        if options=="Boolean Conditions":
            self.boolean_conditions(col2)
    def desired_rows_and_columns(self, col2):
        col2.subheader("Give Inputs", divider='blue')
        rows_options = col2.selectbox("Type Of Row Selection", ["Continuous Rows ['Slicing']", "Desired Rows"])
        columns_options = col2.selectbox("Type Of Column Selection", ["All Columns", "Specific Columns"])
    
        if rows_options == "Continuous Rows ['Slicing']":
            start_index = col2.number_input("Start Index for Slicing", min_value=0, max_value=len(self.df) - 1, value=0)
            end_index = col2.number_input("End Index for Slicing", min_value=0, max_value=len(self.df), value=len(self.df))
            selected_rows = slice(start_index, end_index)
        else:
            selected_rows = col2.multiselect("Select the desired indexes", list(self.df.index))
            if not selected_rows:
                col2.warning("You must select at least one row.")
                return
    
        if columns_options == "All Columns":
            selected_columns = self.df.columns
        else:
            selected_columns = col2.multiselect("Select the columns", list(self.df.columns))
            if not selected_columns:
                col2.warning("You must select at least one column.")
                return
    
        if col2.button("Fix to extract", use_container_width=True, type='primary'):
            selected_data = self.df.loc[selected_rows, selected_columns]
            key = f"Stage - Access & Modify (Advanced) = Desired Rows ({selected_rows}), Columns ({selected_columns})"
            st.session_state["allData"][key] = selected_data
            col2.subheader("Your Results", divider='grey')
            col2.dataframe(selected_data)
            
    def portion_rows_and_columns(self, col2):
        col2.subheader("Extract a portion of rows first", divider='blue')
        sample_size = col2.slider("Select sample size", 0.0,1.0,0.2)
    
        sample_data = self.df.sample(frac=sample_size)
    
        columns_options = col2.selectbox("Type Of Column Selection", ["All Columns", "Specific Columns"])
        if columns_options == "All Columns":
            selected_data = sample_data
        else:
            selected_columns = col2.multiselect("Select the columns", list(sample_data.columns))
            if not selected_columns:
                col2.warning("You must select at least one column.")
                return
            selected_data = sample_data[selected_columns]
    
        if col2.button("Fix to extract", use_container_width=True, type='primary'):
            key = f"Stage - Access & Modify (Advanced) = Portion Rows ({sample_size}), Columns ({selected_columns if columns_options != 'All Columns' else 'All'})"
            st.session_state["allData"][key] = selected_data
            col2.subheader("Your Results", divider='grey')
            col2.dataframe(selected_data)
            
    def truncate_data(self, col2):
        col2.subheader("Truncate Data", divider='blue')
        before_index = col2.text_input("Truncate before index (leave blank for none)", "")
        after_index = col2.text_input("Truncate after index (leave blank for none)", "")
    
        if col2.button("Apply Truncate", use_container_width=True, type='primary'):
            try:
                selected_data = self.df.truncate(before=int(before_index) if before_index.isdigit() else None, 
                                                 after=int(after_index) if after_index.isdigit() else None)
                key = f"Stage - Access & Modify (Advanced) = Truncated before {before_index}, after {after_index}"
                st.session_state["allData"][key] = selected_data
                col2.subheader("Your Results", divider='grey')
                col2.dataframe(selected_data)
            except Exception as e:
                col2.warning(f"Error: {e}")

    def boolean_conditions(self, col2):
        col2.subheader("Apply Boolean Conditions", divider='blue')
        column_selected = col2.selectbox("Select a column", list(self.df.columns))
        condition = col2.text_input("Enter a condition (e.g., > 50, == 'value')")
    
        if col2.button("Apply Condition", use_container_width=True, type='primary'):
            try:
                selected_data = self.df.query(f"{column_selected} {condition}")
                key = f"Stage - Access & Modify (Advanced) = Boolean Condition on {column_selected} ({condition})"
                st.session_state["allData"][key] = selected_data
                col2.subheader("Your Results", divider='grey')
                col2.dataframe(selected_data)
            except Exception as e:
                col2.warning(f"Error: {e}")
