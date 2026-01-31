import pandas as pd
import streamlit as st
import numpy as np
from feature_engine.imputation import *
from feature_engine.outliers import *
import matplotlib.pyplot as plt
import seaborn as sns

# Class for methods offered by pandas
class PandasMethods:
    def __init__(self, dataset):
        self.dataset = dataset

    def backward_fill(self):
        axis = st.selectbox("select axis to perform backward fill", ["columns", "index"])
        limit = st.text_input("How many consecutive nan values do you wanted to dill using backwaard fill [enter none to fill all nan values]")
        if st.checkbox("Fix the above settings for backward fill"):
            if limit.lower() == "none":
                return self.dataset.bfill(axis=axis)
            else:
                return self.dataset.bfill(axis=axis, limit=int(limit))
    def forward_fill(self):
        axis = st.selectbox("select axis to perform forward fill", ["columns", "index"])
        limit = st.text_input("How many consecutive nan values do you wanted to dill using forward fill [enter none to fill all nan values]")
        if st.checkbox("Fix the above settings for forward fill"):
            if limit.lower() == "none":
                return self.dataset.ffill(axis=axis)
            else:
                return self.dataset.ffill(axis=axis, limit=int(limit))
    def drop_na(self):
        axis = st.selectbox("Select axis to drop missing values", ["rows", "columns"], index=0)
        choice = st.radio("Select criteria to drop rows/columns", ["how", "threshold"])
        if choice == "how":
            how = st.selectbox("How to drop?", ["any", "all"], index=0)
        if choice=="threshold":
            thresh = st.number_input("Require this many non-NA values", min_value=0, max_value=len(self.dataset), value=None, step=1)

        if st.checkbox("Fix the above settings for dropna"):
            if axis == "rows":
                axis_value = 0
            else:
                axis_value = 1

            if choice=="how":
                return self.dataset.dropna(axis=axis_value, how=how)
            else:
                return self.dataset.dropna(axis=axis_value, thresh=thresh)
    def fill_na(self):
        selected_columns = st.multiselect("select the columns to fill the na values",self.dataset.columns)
        fill_value = st.text_input("Enter the value to fill the corresponding na values with ',' as separator")
        if fill_value:
            fill_value=fill_value.split(",")
        values = self.make_dictionary(selected_columns, fill_value)
        if st.checkbox("Confirm to apply fill values"):
            return self.dataset.fillna(values)
    def interpolate_missing_values(self):
        method = st.selectbox("Select interpolation method", [
            'linear', 'time', 'index', 'pad', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic'
        ])
        if method == 'polynomial':
            order = st.number_input("Specify the order for polynomial interpolation", min_value=1, step=1)

        if st.checkbox("Confirm interpolate missing values operation"):
            dataframe = self.dataset.interpolate(method=method)
            return dataframe


    def make_dictionary(self, selected_columns, values):
        fill_dict = {}
        for i in range(len(selected_columns)):
            if values[i].isdigit():
                fill_dict[selected_columns[i]] = int(values[i])
            elif values[i].isnumeric():
                fill_dict[selected_columns[i]] = float(values[i])
            else:
                fill_dict[selected_columns[i]] = values[i]
        return fill_dict
        

class UnivariateImputers:
    def __init__(self, dataset):
        self.dataset = dataset

    def MeanMedianImputer(self):
        st.write("### Mean/Median Imputer")
        imputation_method = st.radio("Choose imputation method:", ["mean", "median"])
        method = "mean" if imputation_method == "mean" else "median"

        variables_mode = st.radio(
            "How would you like to select variables?",
            ["All variables", "Specific variables"],
        )

        if variables_mode == "Specific variables":
            variables = st.multiselect(
                "Select variables to impute:",
                options=self.dataset.columns.tolist(),
                help="Choose one or more columns to apply imputation.",
            )
        else:
            variables = None  # Default to all variables

        imputer = MeanMedianImputer(imputation_method=method, variables=variables)
        imputer.fit(self.dataset)
        transformed_data = imputer.transform(self.dataset)

        st.success("Imputation complete!")
        return transformed_data

    def EndTailImputer(self):
        st.write("### End Tail Imputer")
        tail = st.radio("Choose the tail to use for imputation:", ["right", "left"])
        fold = st.slider("Select the fold value:", 1.0, 5.0, 3.0, step=0.1)

        variables_mode = st.radio(
            "How would you like to select variables?",
            ["All variables", "Specific variables"],
        )

        if variables_mode == "Specific variables":
            variables = st.multiselect(
                "Select variables to impute:",
                options=self.dataset.columns.tolist(),
                help="Choose one or more columns to apply imputation.",
            )
        else:
            variables = None  # Default to all variables

        imputer = EndTailImputer(tail=tail, fold=fold, variables=variables)
        imputer.fit(self.dataset)
        transformed_data = imputer.transform(self.dataset)

        st.success("Imputation complete!")
        return transformed_data

    def RandomSampleImputer(self):
        st.write("### Random Sample Imputer")
        seed = st.radio(
            "Select seeding method:",
            ["general", "observation"],
            help="Choose whether to set one seed for all observations or a unique seed for each observation.",
        )
        random_state = st.number_input(
            "Set random state (leave blank for None):",
            value=None,
            min_value=0,
            format="%d",
        )

        variables_mode = st.radio(
            "How would you like to select variables?",
            ["All variables", "Specific variables"],
        )

        if variables_mode == "Specific variables":
            variables = st.multiselect(
                "Select variables to impute:",
                options=self.dataset.columns.tolist(),
                help="Choose one or more columns to apply imputation.",
            )
        else:
            variables = None  # Default to all variables

        imputer = RandomSampleImputer(
            variables=variables, random_state=random_state, seed=seed
        )
        imputer.fit(self.dataset)
        transformed_data = imputer.transform(self.dataset)

        st.success("Imputation complete!")
        return transformed_data

    def AddMissingIndicator(self):
        st.write("### Add Missing Indicator")
        missing_only = st.radio(
            "Should indicators be added only for variables with missing data?",
            ["Yes", "No"],
            help="Yes: Indicators for variables with missing data only. No: Indicators for all variables.",
        )
        missing_only = True if missing_only == "Yes" else False

        variables_mode = st.radio(
            "How would you like to select variables?",
            ["All variables", "Specific variables"],
        )

        if variables_mode == "Specific variables":
            variables = st.multiselect(
                "Select variables to add missing indicators:",
                options=self.dataset.columns.tolist(),
                help="Choose one or more columns to apply missing indicator creation.",
            )
        else:
            variables = None  # Default to all variables

        imputer = AddMissingIndicator(missing_only=missing_only, variables=variables)
        imputer.fit(self.dataset)
        transformed_data = imputer.transform(self.dataset)

        st.success("Missing indicators added!")
        return transformed_data
        
class OutliersTreatment:
    def __init__(self, dataset):
        self.dataset = dataset

    def display_radio_options(self):
        # Provide a radio button to select the outlier treatment method
        self.method = st.radio("Select Outlier Treatment Method", 
                               ('Arbitrary Outlier Capper', 'Winsorizer', 'Outlier Trimmer'))
    
    def arbitrary_outlier_capper(self):
        st.subheader("Arbitrary Outlier Capper")

        # User inputs for max and min capping dictionaries
        max_capping = st.text_input("Enter max capping values (e.g., {'x1': 8})")
        min_capping = st.text_input("Enter min capping values (e.g., {'x1': 2})")
        
        try:
            max_capping_dict = eval(max_capping)
            min_capping_dict = eval(min_capping)
        except:
            st.error("Invalid dictionary format. Please enter a valid dictionary.")
            return self.dataset  # Return the original dataset in case of an error

        # Create the ArbitraryOutlierCapper object
        capper = ArbitraryOutlierCapper(max_capping_dict=max_capping_dict, 
                                        min_capping_dict=min_capping_dict)
        
        # Apply transformation and return the transformed dataset
        self.dataset = capper.fit_transform(self.dataset)
        st.dataframe(self.dataset)  # Display using st.dataframe for better interactivity
        return self.dataset

    def winsorizer(self):
        st.subheader("Winsorizer")

        # User input for capping method
        capping_method = st.radio("Select capping method", ('gaussian', 'iqr', 'mad', 'quantiles'), index=0)
        
        # Tail and fold configuration
        tail = st.radio("Select tail to cap", ('right', 'left', 'both'), index=0)
        fold = st.number_input("Enter the fold factor", value=3.0, step=0.1)
        
        # Create Winsorizer object
        winsorizer = Winsorizer(capping_method=capping_method, 
                                tail=tail, 
                                fold=fold)
        
        # Apply transformation and return the transformed dataset
        self.dataset = winsorizer.fit_transform(self.dataset)
        st.dataframe(self.dataset)  # Display using st.dataframe for better interactivity
        return self.dataset

    def outlier_trimmer(self):
        st.subheader("Outlier Trimmer")
        
        # Ask user for trim percentage
        lower_percentile = st.slider("Lower percentile for trimming", 0.0, 50.0, 25.0)
        upper_percentile = st.slider("Upper percentile for trimming", 50.0, 100.0, 75.0)
        
        # Trim the dataset using percentiles
        lower_limit = self.dataset.quantile(lower_percentile / 100)
        upper_limit = self.dataset.quantile(upper_percentile / 100)
        
        # Apply the trimming operation and return the transformed dataset
        self.dataset = self.dataset[(self.dataset >= lower_limit) & (self.dataset <= upper_limit)]
        st.dataframe(self.dataset)  # Display using st.dataframe for better interactivity
        return self.dataset
    
    def apply_outlier_treatment(self):
        # Display method selection
        self.display_radio_options()
        
        # Apply the corresponding treatment method based on user input
        if self.method == 'Arbitrary Outlier Capper':
            return self.arbitrary_outlier_capper()
        elif self.method == 'Winsorizer':
            return self.winsorizer()
        elif self.method == 'Outlier Trimmer':
            return self.outlier_trimmer()
    def visualize_outliers(self):
        st.subheader("Visualize Outliers with Boxplot")
        
        # Create a boxplot for each numeric column to visualize outliers
        numeric_columns = self.dataset.select_dtypes(include=["int32","int64","float32","float64"]).columns.tolist()
        
        for column in numeric_columns:
            plt.figure(figsize=(8, 6))
            sns.boxplot(x=self.dataset)
            plt.title(f"Boxplot")
            st.pyplot(plt)  # Display the plot using Streamlit
