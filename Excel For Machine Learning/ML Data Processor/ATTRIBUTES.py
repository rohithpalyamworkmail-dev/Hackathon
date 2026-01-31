import streamlit as st
import pandas as pd

if 'allData' not in st.session_state:
    st.session_state['allData'] = {}

class ATTRIBUTES:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def display(self):
        tab1,tab2=st.tabs(["Perform","Learn"])
        with tab1:
            col1, col2 = st.columns([1, 2],border=True)
            # Radio buttons in column 1
            operations = [
                "See Indexes",
                "See Columns",
                "See Columns Data Types",
                "Information On DataSet",
                "Create Sub Data With Similer Data Types",
                "See Data Set Values",
                "See Axes",
                "Dataset Dimension",
                "Data Set Size",
                "(Columns,Rows)",
                "memory_usage",
                "Is Data Frame Empty?",
                "Add Column Names",
                'Find Minimum - Maximum Values',
                "Find Unique Values",
                "Find Number Of Unique Values in A Column",
                "Find Value Counts",
                "Covert Data Types",
                "Find Index Which Has Maximum Value",
                "Find Mininum Index Which Has Minimum Value",
                "Find Largest Values",
                "Find Smallest Values",
                "Transpose A Data Frame"
            ]
            selected_operation = col1.radio("Select an operation:", operations)
    
            # Display result in column 2
            try:
                if selected_operation == "See Indexes":
                    col2.dataframe(self.dataframe.index)
                elif selected_operation == "See Columns":
                    col2.write(list(self.dataframe.columns))
                elif selected_operation == "See Columns Data Types":
                    col2.dataframe(self.dataframe.dtypes)
                elif selected_operation == "Information On DataSet":
                    col2.write(self.dataframe.info(verbose=True,show_counts=True))
                elif selected_operation == "Create Sub Data With Similer Data Types":
                    # Display available datatypes in a multiselect
                    available_dtypes = list(self.dataframe.dtypes.unique())
                    selected_dtypes = col2.multiselect("Select datatypes to include:", available_dtypes)
                    if selected_dtypes:
                        filtered_df = self.dataframe.select_dtypes(include=selected_dtypes)
                        col2.dataframe(filtered_df)
                elif selected_operation == "See Data Set Values":
                    col2.write(self.dataframe.values)
                elif selected_operation == "See Axes":
                    col2.write(self.dataframe.axes)
                elif selected_operation == "Dataset Dimension":
                    col2.write(self.dataframe.ndim)
                elif selected_operation == "Data Set Size":
                    col2.write(self.dataframe.size)
                elif selected_operation == "(Columns,Rows)":
                    col2.write(self.dataframe.shape)
                elif selected_operation == "memory_usage":
                    col2.write(self.dataframe.memory_usage())
                elif selected_operation == "Is Data Frame Empty?":
                    col2.write(self.dataframe.empty)
                elif selected_operation == "Add Column Names":
                    values=col2.text_input("Please Input the column names with ',' as seperator")
                    if col2.button("Add These Column Names",use_container_width=True,type='primary'):
                        if values:
                            values=values.split(',')
                            if self.dataframe.shape[1] == len(values):
                                dataframe=self.dataframe.copy(deep=True)
                                dataframe.columns=values
                                col2.subheader("Here Is the sample Data",divider='blue')
                                col2.dataframe(dataframe)
                                st.session_state['allData'][f"Stage 1 - Add Column Names -{values}"]=dataframe
                            else:
                                col2.warning(f"Specified column names does not match with the number of columns present in dataset {self.dataframe.shape[1]}")
                elif selected_operation=='Find Minimum - Maximum Values':
                    self.min_max(col2)
                elif selected_operation == "Find Unique Values":
                    self.unique(col2)
                elif selected_operation=="Find Number Of Unique Values in A Column":
                    self.nunique(col2)
                elif selected_operation == "Find Value Counts":
                    self.value_counts(col2)
                elif selected_operation == "Covert Data Types":
                    self.convert_dtype(col2)
                elif selected_operation == "Find Index Which Has Maximum Value":
                    self.idx_max(col2)
                elif selected_operation == "Find Mininum Index Which Has Minimum Value":
                    self.idx_min(col2)
                elif selected_operation == "Find Largest Values":
                    self.nlargest(col2)
                elif selected_operation == "Find Smallest Values":
                    self.nsmallest(col2)
                elif selected_operation == "Transpose A Data Frame":
                    self.transpose(col2)
            except Exception as e:
                col2.error(e)
        with tab2:
            st.subheader("Video Documentation Given Below",divider='blue')
            st.video("https://youtu.be/Ac6kWTDg02c")
        
    def min_max(self,col2):
        option=col2.radio("Selecte the columns on which you want to perform minimum and maximum values",["All Columns","Specific Columns"])
        if option == "All Columns":
            if col2.button("Apply Min Max",use_container_width=True,type='primary'):
                data=self.dataframe.select_dtypes(include=['int8','int16','int32','int64','float16','float32','float64','number'])
                self.min_values,self.max_values=[],[]
                for i in data.columns.tolist():
                    self.min_values.append(data[i].min())
                    self.max_values.append(data[i].max())
                newDataFrame=pd.DataFrame({"Minimum Values":self.min_values,"Maximum Values":self.max_values},index=data.columns.tolist())
                col2.dataframe(newDataFrame)
                st.session_state['allData'][f'Stage - Attributes - Min Max Columns - {data.columns.tolist()}']=newDataFrame
        if option == "Specific Columns":
            columns=col2.multiselect("Select the columns you want to include",self.dataframe.columns.tolist())
            if col2.button("Apply Min Max",use_container_width=True,type='primary'):
                data=self.dataframe[columns]
                self.min_values,self.max_values=[],[]
                for i in data.columns.tolist():
                    self.min_values.append(data[i].min())
                    self.max_values.append(data[i].max())
                newDataFrame=pd.DataFrame({"Minimum Values":self.min_values,"Maximum Values":self.max_values},index=data.columns.tolist())
                col2.dataframe(newDataFrame)
                st.session_state['allData'][f'Stage - Attributes - Min Max Columns - {data.columns.tolist()}']=newDataFrame       
    def unique(self, col2):
        option = col2.radio("Select the columns on which you want to know the unique values present", ["All Columns", "Specific Columns"])
        
        if option == "All Columns":
            if col2.button("Apply", use_container_width=True, type='primary'):
                unique_values = {col: self.dataframe[col].unique().tolist() for col in self.dataframe.columns}
                col2.write(unique_values)
                st.session_state['allData'][f'Stage - Attributes - Unique Values - All Columns'] = unique_values
    
        if option == "Specific Columns":
            columns = col2.multiselect("Select the columns you want to include", self.dataframe.columns.tolist())
            if columns and col2.button("Apply", use_container_width=True, type='primary'):
                unique_values = {col: self.dataframe[col].unique().tolist() for col in columns}
                col2.write(unique_values)
                st.session_state['allData'][f'Stage - Attributes - Unique Values - {columns}'] = unique_values
    def nunique(self, col2):
        option = col2.radio("Select the columns on which you want to know the number of unique values present", ["All Columns", "Specific Columns"])
        
        if option == "All Columns":
            if col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe.nunique()
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - N Unique - All Columns'] = unique_counts
    
        if option == "Specific Columns":
            columns = col2.multiselect("Select the columns you want to include", self.dataframe.columns.tolist())  # Changed selectbox to multiselect
            if columns and col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = {col: self.dataframe[col].nunique() for col in columns}
                unique_counts_df = pd.DataFrame.from_dict(unique_counts, orient="index", columns=["Unique Count"])  # Convert dictionary to DataFrame
                col2.dataframe(unique_counts_df)
                st.session_state['allData'][f'Stage - Attributes - N Unique - {columns}'] = unique_counts_df

    def value_counts(self,col2):
        option = col2.radio("Select the columns on which you want to know the value counts", ["All Columns", "Specific Columns"])
        
        if option == "All Columns":
            if col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe.value_counts()
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - Value Counts - All Columns'] = unique_counts
    
        if option == "Specific Columns":
            columns = col2.multiselect("Select the columns you want to include", self.dataframe.columns.tolist())  # Changed selectbox to multiselect
            if columns and col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe[columns].value_counts()
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - Value Counts - {columns}'] = unique_counts
    def convert_dtype(self, col2):
        option = col2.selectbox(
            "Select conversion option:",
            [
                "Convert all columns to your desired data types",
                "Convert specific columns to desired datatypes",
                "Convert all columns to best datatypes",
                "Convert specific columns to best datatypes",
                "Just infer datatypes",
            ],
        )
    
        if option == "Convert all columns to your desired data types":
            dtype_input = col2.text_input("Enter the desired datatype (e.g., int32, float32, string, category) Pandas Data Type:")
            if dtype_input and col2.button("Apply Conversion", use_container_width=True, type='primary'):
                converted_df = self.dataframe.astype(dtype_input)
                col2.dataframe(converted_df)
                st.session_state['allData'][f'Stage - Attributes - Convert DTypes - All Columns to {dtype_input}'] = converted_df
    
        elif option == "Convert specific columns to desired datatypes":
            selected_columns = col2.multiselect("Select columns to convert:", self.dataframe.columns.tolist())
            dtype_mappings = col2.text_area(
                "Enter datatypes for selected columns (comma-separated, e.g., col1:int, col2:float):"
            )
    
            if selected_columns and dtype_mappings and col2.button("Apply Conversion", use_container_width=True, type='primary'):
                if len(selected_columns)==len(dtype_mappings.split(',')):
                    dtype_dict = {selected_columns[i]:dtype_mappings.split(',')[i] for i in range(len(dtype_mappings.split(',')))}
                    converted_df = self.dataframe.copy()
                    try:
                        converted_df = converted_df.astype(dtype_dict)
                        col2.dataframe(converted_df)
                        st.session_state['allData'][f'Stage - Attributes - Convert DTypes - Specific Columns {selected_columns}'] = converted_df
                    except Exception as e:
                        col2.error(f"Error in conversion: {e}")
                else:
                    col2.warning("Selected Columns length should match to given dtypes length")
    
        elif option == "Convert all columns to best datatypes":
            if col2.button("Apply Best Conversion", use_container_width=True, type='primary'):
                converted_df = self.dataframe.convert_dtypes()
                col2.dataframe(converted_df)
                st.session_state['allData'][f'Stage - Attributes - Convert DTypes - All Columns to Best'] = converted_df
    
        elif option == "Convert specific columns to best datatypes":
            selected_columns = col2.multiselect("Select columns to convert:", self.dataframe.columns.tolist())
    
            if selected_columns and col2.button("Apply Best Conversion", use_container_width=True, type='primary'):
                converted_df = self.dataframe.copy()
                converted_df[selected_columns] = converted_df[selected_columns].convert_dtypes()
                col2.dataframe(converted_df)
                st.session_state['allData'][f'Stage - Attributes - Convert DTypes - Best for {selected_columns}'] = converted_df
    
        elif option == "Just infer datatypes":
            if col2.button("Infer Datatypes", use_container_width=True, type='primary'):
                converted_df = self.dataframe.infer_objects()
                col2.dataframe(converted_df)
                st.session_state['allData'][f'Stage - Attributes - Convert DTypes - Inferred'] = converted_df

    def idx_max(self,col2):
        option = col2.radio("Select the columns on which you want to know the Maximum Indexes", ["All Columns", "Specific Columns"])
        
        if option == "All Columns":
            if col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe.idxmax()
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - Largest Index - All Columns'] = unique_counts
    
        if option == "Specific Columns":
            columns = col2.multiselect("Select the columns you want to include", self.dataframe.columns.tolist())  # Changed selectbox to multiselect
            if columns and col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe[columns].idxmax()
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - Largest Index - {columns}'] = unique_counts

    def idx_min(self,col2):
        option = col2.radio("Select the columns on which you want to know the Manimum Indexes", ["All Columns", "Specific Columns"])
        
        if option == "All Columns":
            if col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe.idxmin()
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - Smallest Index - All Columns'] = unique_counts
    
        if option == "Specific Columns":
            columns = col2.multiselect("Select the columns you want to include", self.dataframe.columns.tolist())  # Changed selectbox to multiselect
            if columns and col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe[columns].idxmin()
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - Smallest Index - {columns}'] = unique_counts
    def nlargest(self,col2):
        option = col2.radio("Select the columns on which you want to know the Manimum Indexes", ["All Columns", "Specific Columns"])
        keep=col2.selectbox("Select the occureces",["first","last","all"])
        if option == "All Columns":
            n=col2.slider("Drag To Select The Number Of Values You Want",1,self.dataframe.shape[0],1)
            if col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe.nlargest(n,columns=self.dataframe.columns.tolist(),keep=keep)
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - N Largest - All Columns'] = unique_counts
    
        if option == "Specific Columns":
            columns = col2.multiselect("Select the columns you want to include", self.dataframe.columns.tolist())
            n=col2.slider("Drag To Select The Number Of Values You Want",1,self.dataframe.shape[0],1)# Changed selectbox to multiselect
            if columns and col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe[columns].nlargest(n,columns=columns,keep=keep)
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - N Largest - {columns}'] = unique_counts
    def nsmallest(self,col2):
        option = col2.radio("Select the columns on which you want to know the Manimum Indexes", ["All Columns", "Specific Columns"])
        keep=col2.selectbox("Select the Occurences",["first","last","all"])
        
        if option == "All Columns":
            n=col2.slider("Drag To Select The Number Of Values You Want",1,self.dataframe.shape[0],1)
            if col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe.nsmallest(n,columns=self.dataframe.columns.tolist(),keep=keep)
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - N Smallest - All Columns'] = unique_counts
    
        if option == "Specific Columns":
            columns = col2.multiselect("Select the columns you want to include", self.dataframe.columns.tolist())
            n=col2.slider("Drag To Select The Number Of Values You Want",1,self.dataframe.shape[0],1)# Changed selectbox to multiselect
            if columns and col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe[columns].nsmallest(n,columns=columns,keep=keep)
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - N Smallest - {columns}'] = unique_counts
    def transpose(self,col2):
        option = col2.radio("Select the columns on which you want to transpose", ["All Columns", "Specific Columns"])
        
        if option == "All Columns":
            if col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe.T
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - Transpose - All Columns'] = unique_counts
    
        if option == "Specific Columns":
            columns = col2.multiselect("Select the columns you want to include", self.dataframe.columns.tolist())
            n=col2.slider("Drag To Select The Number Of Values You Want",1,self.dataframe.shape[0],1)# Changed selectbox to multiselect
            if columns and col2.button("Apply", use_container_width=True, type='primary'):
                unique_counts = self.dataframe[columns][:n].T
                col2.dataframe(unique_counts)
                st.session_state['allData'][f'Stage - Attributes - Transpose - {columns}'] = unique_counts
