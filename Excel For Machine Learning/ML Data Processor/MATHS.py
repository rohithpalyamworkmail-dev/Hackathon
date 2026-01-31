import streamlit as st
import pandas as pd

class Maths:
    def __init__(self,df):
        self.data = df

    def binary_operation(self, operation):
        """Perform binary operations like add, sub, mul, etc. based on user selection."""
        st.subheader(f"Perform DataFrame.{operation}()")

        numeric_data = self.data.select_dtypes(include=['int32', 'int64', 'float32', 'float64'])

        col1, col2 = st.columns([1, 2], border=True)
        
        with col1:
            st.subheader("Select Option",divider='grey')
            input_method = st.radio("Select Input Method for 'other':", 
                                    options=['Upload Dataset', 'Enter Single Value', 'Enter List'], 
                                    key=f"BineryOperators-{operation}-input-method")
        
        with col2:
            with st.expander(f"{operation.capitalize()} Parameters"):
                other_eval = None
                
                if input_method == 'Upload Dataset':
                    uploaded_file = st.file_uploader("Upload a CSV File", type=["csv"], key=f"BineryOperators-{operation}-upload")
                    if uploaded_file is not None:
                        other_df = pd.read_csv(uploaded_file)
                        other_eval = other_df.select_dtypes(include=['int32', 'int64', 'float32', 'float64']).values
                elif input_method == 'Enter Single Value':
                    other = st.text_input("Enter a single numeric value", key=f"BineryOperators-{operation}-single-value")
                    try:
                        other_eval = float(other) if other else None
                    except ValueError:
                        st.error("Please enter a valid numeric value.")
                elif input_method == 'Enter List':
                    other = st.text_area("Enter a list of values (comma-separated)", key=f"BineryOperators-{operation}-list")
                    if other:
                        try:
                            other_eval = [float(x.strip()) for x in other.split(",")]
                        except ValueError:
                            st.error("Please enter valid numeric values separated by commas.")

                axis = st.selectbox("Select axis (0 for index, 1 for columns)", [0, 1], index=1, key=f"BineryOperators-{operation}-axis")
                level = st.text_area("Enter level (optional)", key=f"BineryOperators-{operation}-level", value="None")
                level_value = eval(level) if level != "None" else None
                fill_value = st.number_input("Enter fill_value (optional)", key=f"BineryOperators-{operation}-fill-value")
                fill_value_value = fill_value if fill_value else None

                if st.checkbox(f"Apply {operation}()", key=f"BineryOperators-{operation}-apply"):
                    try:
                        result = getattr(numeric_data, operation)(other=other_eval, axis=axis, level=level_value, fill_value=fill_value_value)
                        st.write(f"Resulting DataFrame after {operation} on numeric columns:", result)
                        st.session_state['allData'][f"Stage - Mathematics - {operation.capitalize()}"] = result
                    except Exception as e:
                        st.error(f"Error applying {operation}: {e}")

    def add(self):
        self.binary_operation('add')

    def sub(self):
        self.binary_operation('sub')

    def mul(self):
        self.binary_operation('mul')

    def div(self):
        self.binary_operation('div')

    def floordiv(self):
        self.binary_operation('floordiv')

    def mod(self):
        self.binary_operation('mod')

    def pow(self):
        self.binary_operation('pow')

    def dot(self):
        """Perform matrix multiplication with DataFrame.dot()"""
        st.subheader("Perform DataFrame.dot()")
        st.markdown("<h4 style='color: blue;'>You are going to perform DataFrame.dot()</h4>", unsafe_allow_html=True)

        numeric_data = self.data.select_dtypes(include=['int32', 'int64', 'float32', 'float64'])

        col1, col2 = st.columns([1, 2], gap="medium")
        
        with col1:
            st.subheader("Enter Dot Parameters")
            other = st.text_area("Enter 'other' value (DataFrame or Series)", key="BineryOperators-dot-other")
        
        with col2:
            if st.checkbox("Apply dot()", key="BineryOperators-dot-apply"):
                other_eval = eval(other) if other else None
                try:
                    result = numeric_data.dot(other_eval)
                    st.write("Resulting DataFrame after dot multiplication on numeric columns:", result)
                    st.session_state['allData']["Stage - Mathematics - Dot"] = result
                except Exception as e:
                    st.error(f"Error applying dot: {e}")

    def display(self):
        tab1, tab2 = st.tabs(["Perform Operations", "View Operations"])
        
        with tab1:
            operations = ["add", "sub", "mul", "div", "floordiv", "mod", "pow", "dot"]
            selected_operation = st.selectbox("Operations", operations)
            getattr(self, selected_operation)()
        
        with tab2:
            st.subheader("Your Data",divider='blue')
            st.dataframe(self.data)
