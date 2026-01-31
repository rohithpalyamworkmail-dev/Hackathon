import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import janitor

if "allData" not in st.session_state:
    st.session_state["allData"]={}
class MODIFICATIONS:
    def __init__(self, data):
        self.data = data
    
    def display(self):
        st.subheader("DataFrame Operations", divider='blue')
        tab1, tab2 = st.tabs(["Perform Operations", "View Results"])
        
        with tab1:
            col1, col2 = st.columns([1, 2], border=True)
            
            with col1:
                st.subheader("Select Operation")
                self.operation = st.radio(
                    "Choose an operation:",
                    [
                        "Apply", "Apply & Map", "Aggregate", "Group By", "Sort Values", "Sort Index", "Add Suffix", "Add Prefix", 
                        "Rename", "Set Index", "Bin Numeric", "Clean Names", "Concatenate Columns", 
                        "Expand Columns", "Factorize Columns","Add preffix","Add suffix"
                    ]
                )
            if self.operation=="Apply":
                self.apply(col1,col2)
            if self.operation == "Apply & Map":
                self.apply_map(col1,col2)
            if self.operation == "Aggregate":
                self.aggregate(col1,col2)
            if self.operation=="Group By":
                self.group_by(col1,col2)
            if self.operation=="Sort Values":
                self.sort_values(col1,col2)
            if self.operation=="Sort Index":
                self.sort_index(col1,col2)
            if self.operation=="Add Prefix":
                self.add_prefix(col1,col2)
            if self.operation=="Add Suffix":
                self.add_suffix(col1,col2)
            if self.operation=="Rename":
                self.rename(col1,col2)
            if self.operation == "Set Index":
                self.set_index(col1,col2)
            if self.operation == "Bin Numeric":
                self.bin_numeric(col1,col2)
            if self.operation == "Clean Names":
                self.clean_names(col1,col2)
            if self.operation=="Concatenate Columns":
                self.concatenate_columns(col1,col2)
            if self.operation == "Expand Columns":
                self.expand_columns(col1,col2)
            if self.operation=="Factorize Columns":
                self.factorize_columns(col1,col2)
            if self.operation=="Add preffix":
                self.add_Preffix(col1,col2)
            if self.operation=="Add suffix":
                self.add_Suffix(col1,col2)
        with tab2:
            st.subheader("Your Data",divider='blue')
            st.dataframe(self.data)
                
    def add_Suffix(self, col1, col2):
        data1 = self.data.copy(deep=True)
        column = col2.selectbox("Select the columns in which you want to add values", self.data.columns)
        suffix = col2.text_area("Enter comma ',' separated values")
        
        if col2.button("Apply add suffix operation", use_container_width=True, type='primary'):
            data1[f'{column}_{suffix}']=data1[column]+suffix
            col2.dataframe(data1)
            st.session_state['allData'][f'Stage - Modifications - {column} - {suffix}']=data1
    def add_Preffix(self,col1,col2):
        data1 = self.data.copy(deep=True)
        column = col2.selectbox("Select the columns in which you want to add values", self.data.columns)
        preffix = col2.text_area("Enter value")
        
        if col2.button("Apply add suffix operation", use_container_width=True, type='primary'):
            data1[f'{column}_{preffix}']=preffix+data1[column]
            col2.dataframe(data1)
            st.session_state['allData'][f'Stage - Modifications - {column} - {preffix}']=data1
    def apply(self, col1, col2):
        with col2:
            columns = st.multiselect("Select columns to apply function", self.data.columns.tolist())
            lambda_func = st.text_input("Enter lambda function", "lambda x: x")
            
            if st.button("Apply Function"):
                data=self.data.copy(deep=True)
                data[f"Apply({columns})"] = self.data[columns].apply(eval(lambda_func))
                st.success("Function applied successfully!")
                st.session_state["allData"][f"Stage - Modifications - Apply - {columns}"]=data
                st.dataframe(data)
    
    def apply_map(self, col1, col2):
        with col2:
            column = st.selectbox("Select a column", self.data.columns.tolist())
            unique_values = self.data[column].unique().tolist()
            selected_values = st.multiselect("Select values to map", unique_values)
            mapping_values = st.text_input("Enter mapping values (comma-separated)")
            
            if st.button("Apply Map",use_container_width=True):
                try:
                    mapping_dict = dict(zip(selected_values, mapping_values.split(',')))
                    data=self.data.copy(deep=True)
                    data[column] = data[column].map(mapping_dict)
                    st.success("Mapping applied successfully!")
                    st.dataframe(data)
                    key=f"Stage - Modifications - Map - {column}"
                    st.session_state["allData"][key]=data
                except Exception as e:
                    st.error(f"Error applying map: {e}")
    
    def aggregate(self, col1, col2):
        with col2:
            columns = st.multiselect("Select columns to aggregate", self.data.columns.tolist())
            agg_funcs = st.multiselect("Select aggregation functions", ["sum", "mean", "median", "min", "max", "std", "var", "count"])
            
            if st.button("Apply Aggregation", use_container_width=True):
                try:
                    aggregated_data = self.data[columns].agg(agg_funcs)
                    st.success("Aggregation applied successfully!")
                    st.dataframe(aggregated_data)
                    key=f"Stage - Modifications - Aggregate - {columns} - {agg_funcs}"
                    st.session_state["allData"][key]=aggregated_data
                except Exception as e:
                    st.error(f"Error applying aggregation: {e}")
    
    def group_by(self, col1, col2):
        with col2:
            group_column = st.selectbox("Select column to group by", self.data.columns.tolist())
            agg_columns = st.multiselect("Select columns to aggregate", self.data.columns.tolist())
            agg_funcs = st.multiselect("Select aggregation functions", ["sum", "mean", "median", "min", "max", "std", "var", "count"])
            
            if st.button("Apply Group By", use_container_width=True):
                try:
                    grouped_data = self.data.groupby(group_column)[agg_columns].agg(agg_funcs)
                    st.success("Group By applied successfully!")
                    st.dataframe(grouped_data)
                    key=f"Stage - Modifications - Group By - {group_column} - {agg_columns} - {agg_funcs}"
                    st.session_state["allData"][key]=grouped_data
                except Exception as e:
                    st.error(f"Error applying Group By: {e}")
    
    def sort_values(self, col1, col2):
        with col2:
            columns = st.multiselect("Select columns to sort by", self.data.columns.tolist())
            axis = st.selectbox("Select axis", [0, 1], index=0)
            ascending = st.checkbox("Sort in ascending order", value=True)
            kind = st.selectbox("Select sorting algorithm", ["quicksort", "mergesort", "heapsort", "stable"], index=0)
            na_position = st.selectbox("Select NaN position", ["last", "first"], index=0)
            ignore_index = st.checkbox("Ignore index", value=False)
            
            if st.button("Apply Sort Values", use_container_width=True):
                try:
                    sorted_data = self.data.sort_values(
                        by=columns if columns else None,
                        axis=axis,
                        ascending=ascending,
                        kind=kind,
                        na_position=na_position,
                        ignore_index=ignore_index
                    )
                    st.success("Sort applied successfully!")
                    st.dataframe(sorted_data)
                    key=f"Stage - Modifications - sort_values - Columns : {columns} - axis : {axis} - ascending : {ascending} - kind : {kind} - na_position : {na_position} - ignore_index : {ignore_index}"
                    st.sesion_state["allData"][key]=sorted_data
                except Exception as e:
                    st.error(f"Error applying Sort Values: {e}")
    
    def sort_index(self, col1, col2):
        with col2:
            columns = st.multiselect("Select columns to sort by", self.data.columns.tolist())
            axis = st.selectbox("select axis", [0, 1], index=0)
            ascending = st.checkbox("sort in ascending order", value=True)
            kind = st.selectbox("select sorting algorithm", ["quicksort", "mergesort", "heapsort", "stable"], index=0)
            na_position = st.selectbox("select NaN position", ["last", "first"], index=0)
            sort_remaining = st.checkbox("sort remaining", value=False)
            
            if st.button("Apply Sort Values", use_container_width=True):
                try:
                    sorted_data = self.data[columns].sort_index(
                        axis=axis,
                        ascending=ascending,
                        kind=kind,
                        na_position=na_position,
                        sort_remaining=sort_remaining
                    )
                    st.success("Sort applied successfully!")
                    st.dataframe(sorted_data)
                    key=f"Stage - Modifications - sort_index - Columns : {columns} - axis : {axis} - ascending : {ascending} - kind : {kind} - na_position : {na_position} - ignore_index : {sort_remaining}"
                    st.session_state["allData"][key]=sorted_data
                except Exception as e:
                    st.error(f"Error applying Sort Values: {e}")
    
    def add_suffix(self, col1, col2):
        with col2:
            columns = st.multiselect("Select columns for suffix", self.data.columns.tolist())
            suffix = st.text_input("Enter suffix to add")
            
            if st.button("Apply Add Suffix", use_container_width=True):
                try:
                    updated_data=self.data.copy(deep=True)
                    updated_data = updated_data[columns].add_suffix(suffix)
                    st.success("Suffix added successfully!")
                    st.dataframe(updated_data)
                except Exception as e:
                    st.error(f"Error applying Add Suffix: {e}")
    
    def add_prefix(self, col1, col2):
        with col2:
            prefix = st.text_input("Enter prefix to add")
            
            if st.button("Apply Add Prefix", use_container_width=True):
                try:
                    updated_data = self.data.add_prefix(prefix)
                    st.success("Prefix added successfully!")
                    st.dataframe(updated_data)
                except Exception as e:
                    st.error(f"Error applying Add Prefix: {e}")
    
    def rename(self, col1, col2):
        with col2:
            # Select columns or index to rename
            rename_type = st.radio("Select Type to Rename", ("Index", "Columns"))
    
            # Input for renaming index or columns
            if rename_type == "Index":
                selected_index = st.multiselect("Select Indexes to Rename", options=self.data.index.tolist(), default=self.data.index.tolist())
                self.index_map = st.text_area("Enter Index Mapping comma separetd")
                if self.index_map:
                    self.index_map=index_map.split(',')
                    self.index_mapping={i:j for i,j in zip(selected_index,index_map)}
    
            elif rename_type == "Columns":
                selected_columns = st.multiselect("Select Columns to Rename", options=self.data.columns.tolist(), default=self.data.columns.tolist())
                column_map = st.text_area("Enter Column Mapping comma seperated")
                if column_map:
                    column_map=column_map.split(',')
                    self.column_map={i:j for i,j in zip(selected_columns,column_map)}
    
            # Error handling parameter
            errors = st.selectbox("Choose Error Behavior", ["ignore", "raise"], index=0)
    
            # Button to perform renaming operation
            if st.button("Apply Rename", use_container_width=True):
                try:
                    # Perform renaming based on selection
                    if rename_type == "Index":
                        renamed_data = self.data.rename(index=self.index_mapping, errors=errors)
                    elif rename_type == "Columns":
                        renamed_data = self.data.rename(columns=self.column_map, errors=errors)
    
                    # Show success message and renamed DataFrame
                    st.success("Rename applied successfully!")
                    st.dataframe(renamed_data)
    
                    # Save to session state
                    key = f"Stage - Modifications - rename - {rename_type} : {selected_index if rename_type == 'Index' else selected_columns} - errors : {errors}"
                    st.session_state["allData"][key] = renamed_data
    
                except Exception as e:
                    st.error(f"Error applying Rename: {e}")

    
    def set_index(self, col1, col2):
        with col2:
            # Select columns to set as the index
            columns = st.multiselect("Select columns to set as index", self.data.columns.tolist())
            drop = st.checkbox("Drop columns used as index", value=True)
            append = st.checkbox("Append to existing index", value=False)
            verify_integrity = st.checkbox("Verify index integrity (check for duplicates)", value=False)
    
            if st.button("Apply Set Index", use_container_width=True):
                try:
                    # Apply set_index with the selected parameters
                    new_data = self.data.set_index(
                        keys=columns,
                        drop=drop,
                        append=append,
                        verify_integrity=verify_integrity
                    )
    
                    # Save to session state
                    key = f"Stage - Modifications - set_index - Columns: {columns} - drop: {drop} - append: {append} - verify_integrity: {verify_integrity}"
                    st.session_state["allData"][key] = new_data
                    st.success("Successfull")
                    st.dataframe(new_data)
    
                except Exception as e:
                    st.error(f"Error applying Set Index: {e}")

    
    def bin_numeric(self, col1, col2):
        with col2:
            # Select the column to bin
            from_column_name = st.selectbox("Select a column to bin", self.data.columns.tolist())

            # Input for the new column name to store binned values
            to_column_name = st.text_input("Enter new column name for binned data", value=f"{from_column_name}_binned")

            # Input for the bin edges (comma-separated integers)
            bins_input = st.text_input("Enter bin edges (comma-separated integers)", value="0, 5, 11, 15")

            # Convert bins input into a list of integers
            try:
                bins = list(map(int, bins_input.split(',')))
            except ValueError:
                st.error("Invalid bin edges input. Please enter valid comma-separated integers.")
                bins = []

            # Button to apply binning
            if st.button("Apply Binning", use_container_width=True):
                try:
                    if bins:
                        # Use janitor's bin_numeric function to bin the data
                        self.data = self.data.bin_numeric(
                            from_column_name=from_column_name,
                            to_column_name=to_column_name,
                            bins=bins,
                        )
                        st.success("Binning applied successfully!")
                        st.dataframe(self.data)

                        # Save the modified data to session state
                        key = f"Stage - Modifications - bin_numeric - {from_column_name} - bins: {bins}"
                        st.session_state["allData"][key] = self.data

                except Exception as e:
                    st.error(f"Error applying binning: {e}")
    
    def clean_names(self, col1, col2):
        with col2:
            # Option to select axis (columns or index)
            axis = st.selectbox("Select axis to clean", ['columns', 'index'], index=0)
            
            # Input for column names (for specific column cleaning)
            column_names = st.multiselect("Select column names to clean", self.data.columns.tolist())
            if not column_names:
                st.info("Please select at lease one column")
                return " "

            # Options for additional cleaning
            strip_underscores = st.selectbox("Remove outer underscores", ['None', 'left', 'right', 'both'], index=0)
            case_type = st.selectbox("Convert case", ['lower', 'upper', 'preserve', 'snake'], index=0)
            remove_special = st.checkbox("Remove special characters", value=False)
            strip_accents = st.checkbox("Strip accents", value=True)
            preserve_original_labels = st.checkbox("Preserve original labels", value=True)
            enforce_string = st.checkbox("Enforce string type for column names/values", value=True)
            truncate_limit = st.number_input("Truncate column names/values to length", min_value=0, value=0)

            if st.button("Apply Clean Names", use_container_width=True):
                try:
                    # Apply clean_names from janitor
                    self.data = self.data.clean_names(
                        axis=axis,
                        column_names=column_names if axis == 'columns' else None,
                        strip_underscores=strip_underscores if strip_underscores != 'None' else None,
                        case_type=case_type,
                        remove_special=remove_special,
                        strip_accents=strip_accents,
                        preserve_original_labels=preserve_original_labels,
                        enforce_string=enforce_string,
                        truncate_limit=truncate_limit if truncate_limit > 0 else None,
                    )
                    st.success("Column names cleaned successfully!")
                    st.dataframe(self.data)

                    # Save the modified data to session state
                    key = f"Stage - Modifications - clean_names - axis: {axis} - columns: {column_names} - strip_underscores: {strip_underscores} - case_type: {case_type} - remove_special: {remove_special} - strip_accents: {strip_accents} - preserve_original_labels: {preserve_original_labels} - enforce_string: {enforce_string} - truncate_limit: {truncate_limit}"
                    st.session_state["allData"][key] = self.data

                except Exception as e:
                    st.error(f"Error applying clean names: {e}")
    
    def concatenate_columns(self, col1, col2):
        with col2:
            # Select columns to concatenate
            column_names = st.multiselect("Select columns to concatenate", self.data.columns.tolist())
            new_column_name = st.text_input("Enter the new column name", value="new_column")

            # Options for separator and handling empty values
            sep = st.text_input("Enter separator (default '-'): ", value="-")
            ignore_empty = st.checkbox("Ignore empty values (NaN)", value=True)

            if st.button("Apply Concatenate Columns", use_container_width=True):
                try:
                    # Apply concatenate_columns from janitor
                    self.data = self.data.concatenate_columns(
                        column_names=column_names,
                        new_column_name=new_column_name,
                        sep=sep,
                        ignore_empty=ignore_empty
                    )
                    st.success(f"Columns concatenated successfully into '{new_column_name}'!")
                    st.dataframe(self.data)

                    # Save the modified data to session state
                    key = f"Stage - Modifications - concatenate_columns - columns: {column_names} - new_column_name: {new_column_name} - sep: {sep} - ignore_empty: {ignore_empty}"
                    st.session_state["allData"][key] = self.data

                except Exception as e:
                    st.error(f"Error applying concatenate columns: {e}")
    
    def encode_categorical(self, col1, col2):
        pass
    
    def expand_columns(self, col1, col2):
        with col2:
            # Select column to expand
            column_name = st.selectbox("Select a column to expand", self.data.columns.tolist())

            # Separator input
            sep = st.text_input("Enter separator (default ', '):", value=", ")

            # Option for concatenating expanded columns with the original DataFrame
            concat = st.checkbox("Concatenate expanded columns to original DataFrame", value=True)

            if st.button("Apply Expand Column", use_container_width=True):
                try:
                    # Apply expand_column method from janitor
                    expanded_data = self.data.expand_column(
                        column_name=column_name,
                        sep=sep,
                        concat=concat
                    )
                    st.success(f"Column '{column_name}' expanded successfully!")
                    st.dataframe(expanded_data)

                    # Save the modified data to session state
                    key = f"Stage - Modifications - expand_column - column: {column_name} - sep: {sep} - concat: {concat}"
                    st.session_state["allData"][key] = expanded_data

                except Exception as e:
                    st.error(f"Error expanding column: {e}")
                    
    def factorize_columns(self, col1, col2):
        with col2:
            # Select column(s) to factorize
            column_names = st.multiselect("Select columns to factorize", self.data.columns.tolist())

            # Suffix input
            suffix = st.text_input("Enter suffix for new column(s) (default '_enc'):", value="_enc")
            if st.button("Apply Factorize Columns", use_container_width=True):
                try:
                    # Apply factorize_columns method from janitor
                    factorized_data = self.data.factorize_columns(
                        column_names=column_names,
                        suffix=suffix,
                    )
                    st.success("Factorization applied successfully!")
                    st.dataframe(factorized_data)

                    # Save the modified data to session state
                    key = f"Stage - Modifications - factorize_columns - columns: {column_names} - suffix: {suffix}"
                    st.session_state["allData"][key] = factorized_data

                except Exception as e:
                    st.error(f"Error factorizing columns: {e}")

