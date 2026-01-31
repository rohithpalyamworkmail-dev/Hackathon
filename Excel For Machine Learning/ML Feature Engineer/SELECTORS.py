# importing libraries
import pandas as pd
import streamlit as st
import numpy as np
from feature_engine.selection import *
from sklearn.ensemble import *
from feature_engine.selection import *
if "count" not in st.session_state:
  st.session_state['count']=0
def drop_features(keyy,data):
  select_columns = st.multiselect("Select columns", data.columns.tolist())
  if select_columns:
      dataset = data.copy(deep=True)
      if st.button("Execute Feature Selection", use_container_width=True):   
          object=DropFeatures(select_columns)
          dataframe=object.fit_transform(dataset)
          st.session_state['count']=st.session_state['count']+1
          st.session_state[f"{st.session_state['count']}.{keyy}"]=dataframe
          st.dataframe(dataframe)
def drop_constant_features(option,data):
    tol=int(st.number_input("""Threshold to detect constant/quasi-constant features. Variables showing the same value in a
    percentage of observations greater than tol will be considered 
    constant / quasi-constant and dropped. If tol=1, the transformer 
    removes constant variables. Else, it will remove quasi-constant variables.
    For example, if tol=0.98, the transformer will remove variables that show
    the same value in 98% of the observations.""",1))
    dataset = data.copy(deep=True)
    if st.button("Execute Feature Selection", use_container_width=True):   
        try:
            object=DropConstantFeatures(tol=tol)
            dataframe=object.fit_transform(dataset)
            st.session_state['count']=st.session_state['count']+1
            st.session_state[f"{st.session_state['count']}.{option}"]=dataframe
            st.dataframe(dataframe)
        except Exception as e:
            st.error(e)
def drop_duplicated_features(option,data):
    dataset = data.copy(deep=True)
    if st.button("Execute Feature Selection", use_container_width=True):   
        try:
            object=DropDuplicateFeatures()
            dataframe=object.fit_transform(dataset)
            st.session_state['count']=st.session_state['count']+1
            st.session_state[f"{st.session_state['count']}.{option}"]=dataframe
            st.dataframe(dataframe)
        except Exception as e:
            st.error(e)

def drop_correlated_features(option,data):
    threshold=st.number_input("The correlation threshold above which a feature will be deemed correlated with another one and removed from the dataset.",0.1)
    method=st.selectbox("Correlation method -Can take ‘pearson’, ‘spearman’, ‘kendall’",["pearson","spearman","kendall"])
    dataset = data.copy(deep=True)
    if st.button("Execute Feature Selection", use_container_width=True):   
        try:
            object=DropCorrelatedFeatures(method=method,threshold=threshold)
            dataframe=object.fit_transform(dataset)
            st.session_state['count']=st.session_state['count']+1
            st.session_state[f"{st.session_state['count']}.{option}"]=dataframe
            st.dataframe(dataframe)
        except Exception as e:
            st.error(e)

def drop_high_psi_features(option, df):
    # Clone the dataframe to preserve the original
    df_clone = df.copy()
    
    st.header("Drop High PSI Features Configuration")
    
    # Input for split_col
    split_col = st.selectbox(
        "Select the column to split the dataset (split_col):",
        options=[None] + list(df_clone.columns),
        index=0,
        help="The variable that will be used to split the dataset into the basis and test sets. If None, the dataframe index will be used."
    )
    
    # Input for split_frac
    split_frac = st.slider(
        "Proportion of observations in each dataset (split_frac):",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.1,
        help="The proportion of observations in each of the basis and test dataframes. If 0.6, 60% of the observations will be put in the basis data set."
    )
    
    # Input for split_distinct
    split_distinct = st.checkbox(
        "Split based on unique values (split_distinct):",
        value=False,
        help="If True, split_frac is applied to the vector of unique values in split_col instead of being applied to the whole vector of values."
    )
    
    # Input for cut_off
    cut_off = st.text_input(
        "Threshold to split the dataset (cut_off):if you want to give a list then separete elements with ','",
        value="",
        help="Threshold to split the dataset based on the split_col variable. If int, float or date, observations where the split_col values are <= threshold will go to the basis data set and the rest to the test set. If a list, observations where the split_col values are within the list will go to the basis data set."
    )
    
    # Input for switch
    switch = st.checkbox(
        "Switch the order of basis and test datasets (switch):",
        value=False,
        help="If True, the order of the 2 dataframes used to determine the PSI (basis and test) will be switched."
    )
    
    # Input for threshold
    threshold = st.selectbox(
        "Threshold to drop a feature (threshold):",
        options=[0.25, 0.10, 'auto'],
        index=0,
        help="The threshold to drop a feature. If the PSI for a feature is >= threshold, the feature will be dropped. Common values are 0.25 (large shift) and 0.10 (medium shift). If 'auto', the threshold will be calculated based on the size of the basis and test dataset and the number of bins."
    )
    
    # Input for bins
    bins = st.slider(
        "Number of bins or intervals (bins):",
        min_value=1,
        max_value=20,
        value=10,
        step=1,
        help="Number of bins or intervals. For continuous features with good value spread, 10 bins is commonly used."
    )
    
    # Input for strategy
    strategy = st.selectbox(
        "Strategy for discretization (strategy):",
        options=['equal_frequency', 'equal_width'],
        index=0,
        help="If the intervals into which the features should be discretized are of equal size or equal number of observations. 'equal_width' for equally spaced bins or 'equal_frequency' for bins based on quantiles."
    )
    
    # Input for min_pct_empty_bins
    min_pct_empty_bins = st.number_input(
        "Minimum percentage for empty bins (min_pct_empty_bins):",
        min_value=0.0,
        max_value=1.0,
        value=0.0001,
        step=0.0001,
        help="Value to add to empty bins or intervals. If after sorting the variable values into bins, a bin is empty, the PSI cannot be determined. By adding a small number to empty bins, we can avoid this issue."
    )
    
    # Input for missing_values
    missing_values = st.selectbox(
        "Handling missing values (missing_values):",
        options=['raise', 'ignore'],
        index=0,
        help="Whether to perform the PSI feature selection on a dataframe with missing values. 'raise' will raise an error, 'ignore' will drop missing values."
    )
    
    # Input for variables
    variables = st.multiselect(
        "Variables to evaluate (variables):",
        options=list(df_clone.columns),
        default=None,
        help="The list of variables to evaluate. If None, the transformer will evaluate all numerical variables in the dataset."
    )
    
    # Input for confirm_variables
    confirm_variables = st.checkbox(
        "Confirm variables (confirm_variables):",
        value=False,
        help="If set to True, variables that are not present in the input dataframe will be removed from the list of variables."
    )
    
    # Input for p_value
    p_value = st.number_input(
        "P-value for auto threshold (p_value):",
        min_value=0.001,
        max_value=0.05,
        value=0.001,
        step=0.001,
        help="The p-value to test the null hypothesis that there is no feature drift. This parameter is used only if threshold is set to 'auto'."
    )
    
    # Button to apply Drop High PSI Features
    if st.button("Apply Drop High PSI Features", use_container_width=True, type='primary'):
        # Initialize DropHighPSIFeatures with user inputs
        try:
          psi_selector = DropHighPSIFeatures(
              split_col=split_col,
              split_frac=split_frac,
              split_distinct=split_distinct,
              cut_off=eval(cut_off) if cut_off else None,
              switch=switch,
              threshold=threshold,
              bins=bins,
              strategy=strategy,
              min_pct_empty_bins=min_pct_empty_bins,
              missing_values=missing_values,
              variables=variables if variables else None,
              confirm_variables=confirm_variables,
              p_value=p_value
          )
          
          # Fit and transform the dataframe
          df_transformed = psi_selector.fit_transform(df_clone)
          
          st.write("Transformed DataFrame:")
          st.dataframe(df_transformed)
          st.session_state['count']=st.session_state['count']+1
          st.session_state[f"{st.session_state['count']}.{option}"]=df_transformed
        except Exception as e:
          st.error(e)

def select_by_information_value(option, df):
    # Clone the dataframe to preserve the original
    df_clone = df.copy()
    
    st.header("Select By Information Value Configuration")
    
    # Input for target variable (y)
    target_variable = st.selectbox(
        "Select the target variable (y):",
        options=list(df_clone.columns),
        help="The target variable for binary classification. This is required to calculate the Information Value (IV)."
    )
    
    # Input for variables
    variables = st.multiselect(
        "Variables to evaluate (variables):",
        options=[col for col in df_clone.columns if col != target_variable],  # Exclude target variable
        default=None,
        help="The list of variables to evaluate. If None, the transformer will evaluate all variables in the dataset (except datetime)."
    )
    
    # Input for bins
    bins = st.slider(
        "Number of bins for numerical variables (bins):",
        min_value=1,
        max_value=20,
        value=5,
        step=1,
        help="If the dataset contains numerical variables, the number of bins into which the values will be sorted."
    )
    
    # Input for strategy
    strategy = st.selectbox(
        "Strategy for binning (strategy):",
        options=['equal_width', 'equal_frequency'],
        index=0,
        help="Whether the bins should be of equal width ('equal_width') or equal frequency ('equal_frequency')."
    )
    
    # Input for threshold
    threshold = st.number_input(
        "Threshold to drop a feature (threshold):",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.01,
        help="The threshold to drop a feature. If the IV for a feature is < threshold, the feature will be dropped."
    )
    
    # Input for confirm_variables
    confirm_variables = st.checkbox(
        "Confirm variables (confirm_variables):",
        value=False,
        help="If set to True, variables that are not present in the input dataframe will be removed from the list of variables."
    )
    
    # Button to apply Select By Information Value
    if st.button("Apply Select By Information Value", use_container_width=True, type='primary'):
        try:
            # Initialize SelectByInformationValue with user inputs
            iv_selector = SelectByInformationValue(
                variables=variables if variables else None,
                bins=bins,
                strategy=strategy,
                threshold=threshold,
                confirm_variables=confirm_variables
            )
            
            # Separate features (X) and target (y)
            X = df_clone.drop(columns=[target_variable])
            y = df_clone[target_variable]
            
            # Fit and transform the dataframe
            df_transformed = iv_selector.fit_transform(X, y)
            
            st.write("Transformed DataFrame:")
            st.dataframe(df_transformed)
            st.session_state['count']=st.session_state['count']+1
            st.session_state[f"{st.session_state['count']}.{option}"]=df_transformed
            
            # Display the information value for each feature
            st.write("Information Value for Each Feature:")
            st.write(iv_selector.information_values_)
        except Exception as e:
            st.error(f"An error occurred: {e}")

def select_by_shuffling(option, df):
    # Clone the dataframe to preserve the original
    df_clone = df.copy()
    
    st.header("Select By Shuffling Configuration")
    
    # Input for target variable (y)
    target_variable = st.selectbox(
        "Select the target variable (y):",
        options=list(df_clone.columns),
        help="The target variable for the machine learning model. This is required to evaluate feature importance."
    )
    
    # Input for variables
    variables = st.multiselect(
        "Variables to evaluate (variables):",
        options=[col for col in df_clone.columns if col != target_variable],  # Exclude target variable
        default=None,
        help="The list of variables to evaluate. If None, the transformer will evaluate all numerical features in the dataset."
    )
    
    # Input for estimator
    model_type = st.selectbox(
        "Select the model type:",
        options=['Classifier', 'Regressor'],
        index=0,
        help="Choose whether to use a classifier or regressor for feature selection."
    )
    
    if model_type == 'Classifier':
        estimator = RandomForestClassifier(random_state=42)
    else:
        estimator = RandomForestRegressor(random_state=42)
    
    # Input for scoring metric
    scoring = st.selectbox(
        "Select the scoring metric:",
        options=['roc_auc', 'accuracy', 'r2', 'neg_mean_squared_error'],
        index=0,
        help="The metric used to evaluate the performance of the estimator. Common options include 'roc_auc', 'accuracy', 'r2', and 'neg_mean_squared_error'."
    )
    
    # Input for threshold
    threshold = st.number_input(
        "Threshold to drop a feature (threshold):",
        min_value=0.0,
        max_value=1.0,
        value=0.01,
        step=0.01,
        help="The value that defines whether a feature will be selected. Features with a performance drop below this threshold will be removed."
    )
    
    # Input for cross-validation (cv)
    cv = st.number_input(
        "Number of cross-validation folds (cv):",
        min_value=2,
        max_value=10,
        value=3,
        step=1,
        help="The number of folds to use for cross-validation."
    )
    
    # Input for random_state
    random_state = st.number_input(
        "Random state for shuffling (random_state):",
        min_value=0,
        max_value=100,
        value=42,
        step=1,
        help="Controls the randomness when shuffling features."
    )
    
    # Input for confirm_variables
    confirm_variables = st.checkbox(
        "Confirm variables (confirm_variables):",
        value=False,
        help="If set to True, variables that are not present in the input dataframe will be removed from the list of variables."
    )
    
    # Button to apply Select By Shuffling
    if st.button("Apply Select By Shuffling", use_container_width=True, type='primary'):
        try:
            # Initialize SelectByShuffling with user inputs
            shuffling_selector = SelectByShuffling(
                estimator=estimator,
                variables=variables if variables else None,
                scoring=scoring,
                threshold=threshold,
                cv=cv,
                random_state=random_state,
                confirm_variables=confirm_variables
            )
            
            # Separate features (X) and target (y)
            X = df_clone.drop(columns=[target_variable])
            y = df_clone[target_variable]
            
            # Fit and transform the dataframe
            df_transformed = shuffling_selector.fit_transform(X, y)
            
            st.write("Transformed DataFrame:")
            st.dataframe(df_transformed)
            st.session_state['count']=st.session_state['count']+1
            st.session_state[f"{st.session_state['count']}.{option}"]=df_transformed
            
            # Display the performance drop for each feature
            st.write("Performance Drop for Each Feature:")
            st.write(shuffling_selector.performance_drifts_)
        except Exception as e:
            st.error(f"An error occurred: {e}")

from feature_engine.selection import *
from sklearn.model_selection import *

def select_by_target_mean_performance(option, df):
    # Clone the dataframe to preserve the original
    df_clone = df.copy()
    
    st.header("Select By Target Mean Performance Configuration")
    
    # Input for target variable (y)
    target_variable = st.selectbox(
        "Select the target variable (y):",
        options=list(df_clone.columns),
        help="The target variable for the machine learning model. This is required to evaluate feature importance."
    )
    
    # Input for variables
    variables = st.multiselect(
        "Variables to evaluate (variables):",
        options=[col for col in df_clone.columns if col != target_variable],  # Exclude target variable
        default=None,
        help="The list of variables to evaluate. If None, the transformer will evaluate all variables in the dataset (except datetime)."
    )
    
    # Input for bins
    bins = st.slider(
        "Number of bins for numerical variables (bins):",
        min_value=1,
        max_value=20,
        value=5,
        step=1,
        help="If the dataset contains numerical variables, the number of bins into which the values will be sorted."
    )
    
    # Input for strategy
    strategy = st.selectbox(
        "Strategy for binning (strategy):",
        options=['equal_width', 'equal_frequency'],
        index=0,
        help="Whether the bins should be of equal width ('equal_width') or equal frequency ('equal_frequency')."
    )
    
    # Input for scoring metric
    scoring = st.selectbox(
        "Select the scoring metric:",
        options=['roc_auc', 'accuracy', 'r2', 'neg_mean_squared_error'],
        index=0,
        help="The metric used to evaluate the performance of the estimator. Common options include 'roc_auc', 'accuracy', 'r2', and 'neg_mean_squared_error'."
    )
    
    # Input for threshold
    threshold = st.number_input(
        "Threshold to drop a feature (threshold):",
        min_value=0.0,
        max_value=1.0,
        value=0.01,
        step=0.01,
        help="The value that defines whether a feature will be selected. Features with a performance below this threshold will be removed."
    )
    
    # Input for cross-validation (cv)
    cv = st.number_input(
        "Number of cross-validation folds (cv):",
        min_value=2,
        max_value=10,
        value=3,
        step=1,
        help="The number of folds to use for cross-validation."
    )
    
    # Input for groups
    groups = st.text_input(
        "Group labels for the samples (groups):",
        value="",
        help="Group labels for the samples used while splitting the dataset into train/test set. Only used in conjunction with a 'Group' cv instance (e.g., GroupKFold)."
    )
    
    # Input for regression
    regression = st.checkbox(
        "Is the target variable for regression? (regression):",
        value=False,
        help="Indicates whether the target is one for regression or a classification."
    )
    
    # Input for confirm_variables
    confirm_variables = st.checkbox(
        "Confirm variables (confirm_variables):",
        value=False,
        help="If set to True, variables that are not present in the input dataframe will be removed from the list of variables."
    )
    
    # Button to apply Select By Target Mean Performance
    if st.button("Apply Select By Target Mean Performance", use_container_width=True, type='primary'):
        try:
            # Initialize SelectByTargetMeanPerformance with user inputs
            target_mean_selector = SelectByTargetMeanPerformance(
                variables=variables if variables else None,
                bins=bins,
                strategy=strategy,
                scoring=scoring,
                threshold=threshold,
                cv=cv,
                groups=eval(groups) if groups else None,
                regression=regression,
                confirm_variables=confirm_variables
            )
            
            # Separate features (X) and target (y)
            X = df_clone.drop(columns=[target_variable])
            y = df_clone[target_variable]
            
            # Fit and transform the dataframe
            df_transformed = target_mean_selector.fit_transform(X, y)
            
            st.write("Transformed DataFrame:")
            st.dataframe(df_transformed)
            st.session_state['count']=st.session_state['count']+1
            st.session_state[f"{st.session_state['count']}.{option}"]=df_transformed
            
            # Display the performance for each feature
            st.write("Performance for Each Feature:")
            st.write(target_mean_selector.feature_performance_)
        except Exception as e:
            st.error(f"An error occurred: {e}")

def probe_feature_selection(option, df):
    # Clone the dataframe to preserve the original
    df_clone = df.copy()
    
    st.header("Probe Feature Selection Configuration")
    
    # Input for target variable (y)
    target_variable = st.selectbox(
        "Select the target variable (y):",
        options=list(df_clone.columns),
        help="The target variable for the machine learning model. This is required to evaluate feature importance."
    )
    
    # Input for variables
    variables = st.multiselect(
        "Variables to evaluate (variables):",
        options=[col for col in df_clone.columns if col != target_variable],  # Exclude target variable
        default=None,
        help="The list of variables to evaluate. If None, the transformer will evaluate all numerical features in the dataset."
    )
    
    # Input for estimator
    model_type = st.selectbox(
        "Select the model type:",
        options=['Classifier', 'Regressor'],
        index=0,
        help="Choose whether to use a classifier or regressor for feature selection."
    )
    
    if model_type == 'Classifier':
        estimator = RandomForestClassifier(random_state=42)
    else:
        estimator = RandomForestRegressor(random_state=42)
    
    # Input for collective
    collective = st.checkbox(
        "Use collective feature importance (collective):",
        value=True,
        help="Whether the feature importance should be derived from an estimator trained on the entire dataset (True), or trained using individual features (False)."
    )
    
    # Input for scoring metric
    scoring = st.selectbox(
        "Select the scoring metric:",
        options=['roc_auc', 'accuracy', 'r2', 'neg_mean_squared_error'],
        index=0,
        help="The metric used to evaluate the performance of the estimator. Common options include 'roc_auc', 'accuracy', 'r2', and 'neg_mean_squared_error'."
    )
    
    # Input for n_probes
    n_probes = st.number_input(
        "Number of probe features to create (n_probes):",
        min_value=1,
        max_value=10,
        value=1,
        step=1,
        help="Number of probe features to be created. If distribution is 'all', n_probes must be a multiple of 3."
    )
    
    # Input for distribution
    distribution = st.selectbox(
        "Distribution for probe features (distribution):",
        options=['normal', 'binomial', 'uniform', 'all'],
        index=0,
        help="The distribution used to create the probe features. The options are 'normal', 'binomial', 'uniform', and 'all'. 'all' creates at least 1 or more probe features comprised of each distribution type."
    )
    
    # Input for cross-validation (cv)
    cv = st.number_input(
        "Number of cross-validation folds (cv):",
        min_value=2,
        max_value=10,
        value=5,
        step=1,
        help="The number of folds to use for cross-validation."
    )
    
    # Input for groups
    groups = st.text_input(
        "Group labels for the samples (groups):",
        value="",
        help="Group labels for the samples used while splitting the dataset into train/test set. Only used in conjunction with a 'Group' cv instance (e.g., GroupKFold)."
    )
    
    # Input for random_state
    random_state = st.number_input(
        "Random state for reproducibility (random_state):",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
        help="Controls the randomness when creating probe features and splitting the dataset."
    )
    
    # Input for confirm_variables
    confirm_variables = st.checkbox(
        "Confirm variables (confirm_variables):",
        value=False,
        help="If set to True, variables that are not present in the input dataframe will be removed from the list of variables."
    )
    
    # Button to apply Probe Feature Selection
    if st.button("Apply Probe Feature Selection", use_container_width=True, type='primary'):
        try:
            # Initialize ProbeFeatureSelection with user inputs
            probe_selector = ProbeFeatureSelection(
                estimator=estimator,
                variables=variables if variables else None,
                collective=collective,
                scoring=scoring,
                n_probes=n_probes,
                distribution=distribution,
                cv=cv,
                groups=eval(groups) if groups else None,
                random_state=random_state,
                confirm_variables=confirm_variables
            )
            
            # Separate features (X) and target (y)
            X = df_clone.drop(columns=[target_variable])
            y = df_clone[target_variable]
            
            # Fit and transform the dataframe
            df_transformed = probe_selector.fit_transform(X, y)
            
            st.write("Transformed DataFrame:")
            st.dataframe(df_transformed)
            st.session_state['count']=st.session_state['count']+1
            st.session_state[f"{st.session_state['count']}.{option}"]=df_transformed
            
            # Display the feature importance for each feature
            st.write("Feature Importance for Each Feature:")
            st.write(probe_selector.feature_importances_)
        except Exception as e:
            st.error(f"An error occurred: {e}")

def recursive_feature_addition(option, df):
    # Clone the dataframe to preserve the original
    df_clone = df.copy()
    
    st.header("Recursive Feature Addition Configuration")
    
    # Input for target variable (y)
    target_variable = st.selectbox(
        "Select the target variable (y):",
        options=list(df_clone.columns),
        help="The target variable for the machine learning model. This is required to evaluate feature importance."
    )
    
    # Input for variables
    variables = st.multiselect(
        "Variables to evaluate (variables):",
        options=[col for col in df_clone.columns if col != target_variable],  # Exclude target variable
        default=None,
        help="The list of variables to evaluate. If None, the transformer will evaluate all numerical features in the dataset."
    )
    
    # Input for estimator
    model_type = st.selectbox(
        "Select the model type:",
        options=['Classifier', 'Regressor'],
        index=0,
        help="Choose whether to use a classifier or regressor for feature selection."
    )
    
    if model_type == 'Classifier':
        estimator = RandomForestClassifier(random_state=42)
    else:
        estimator = RandomForestRegressor(random_state=42)
    
    # Input for scoring metric
    scoring = st.selectbox(
        "Select the scoring metric:",
        options=['roc_auc', 'accuracy', 'r2', 'neg_mean_squared_error'],
        index=0,
        help="The metric used to evaluate the performance of the estimator. Common options include 'roc_auc', 'accuracy', 'r2', and 'neg_mean_squared_error'."
    )
    
    # Input for threshold
    threshold = st.number_input(
        "Threshold to drop a feature (threshold):",
        min_value=0.0,
        max_value=1.0,
        value=0.01,
        step=0.01,
        help="The value that defines whether a feature will be selected. Features with a performance increase below this threshold will be removed."
    )
    
    # Input for cross-validation (cv)
    cv = st.number_input(
        "Number of cross-validation folds (cv):",
        min_value=2,
        max_value=10,
        value=3,
        step=1,
        help="The number of folds to use for cross-validation."
    )
    
    # Input for groups
    groups = st.text_input(
        "Group labels for the samples (groups):",
        value="",
        help="Group labels for the samples used while splitting the dataset into train/test set. Only used in conjunction with a 'Group' cv instance (e.g., GroupKFold)."
    )
    
    # Input for confirm_variables
    confirm_variables = st.checkbox(
        "Confirm variables (confirm_variables):",
        value=False,
        help="If set to True, variables that are not present in the input dataframe will be removed from the list of variables."
    )
    
    # Button to apply Recursive Feature Addition
    if st.button("Apply Recursive Feature Addition", use_container_width=True, type='primary'):
        try:
            # Initialize RecursiveFeatureAddition with user inputs
            rfa_selector = RecursiveFeatureAddition(
                estimator=estimator,
                variables=variables if variables else None,
                scoring=scoring,
                threshold=threshold,
                cv=cv,
                groups=eval(groups) if groups else None,
                confirm_variables=confirm_variables
            )
            
            # Separate features (X) and target (y)
            X = df_clone.drop(columns=[target_variable])
            y = df_clone[target_variable]
            
            # Fit and transform the dataframe
            df_transformed = rfa_selector.fit_transform(X, y)
            
            st.write("Transformed DataFrame:")
            st.dataframe(df_transformed)
            st.session_state['count']=st.session_state['count']+1
            st.session_state[f"{st.session_state['count']}.{option}"]=df_transformed
            
            # Display the feature importance for each feature
            st.write("Feature Importance for Each Feature:")
            st.write(rfa_selector.feature_importances_)
        except Exception as e:
            st.error(f"An error occurred: {e}")

def select_by_single_feature_performance(option, df):
    # Clone the dataframe to preserve the original
    df_clone = df.copy()
    
    st.header("Select By Single Feature Performance Configuration")
    
    # Input for target variable (y)
    target_variable = st.selectbox(
        "Select the target variable (y):",
        options=list(df_clone.columns),
        help="The target variable for the machine learning model. This is required to evaluate feature importance."
    )
    
    # Input for variables
    variables = st.multiselect(
        "Variables to evaluate (variables):",
        options=[col for col in df_clone.columns if col != target_variable],  # Exclude target variable
        default=None,
        help="The list of variables to evaluate. If None, the transformer will evaluate all numerical features in the dataset."
    )
    
    # Input for estimator
    model_type = st.selectbox(
        "Select the model type:",
        options=['Classifier', 'Regressor'],
        index=0,
        help="Choose whether to use a classifier or regressor for feature selection."
    )
    
    if model_type == 'Classifier':
        estimator = RandomForestClassifier(random_state=42)
    else:
        estimator = RandomForestRegressor(random_state=42)
    
    # Input for scoring metric
    scoring = st.selectbox(
        "Select the scoring metric:",
        options=['roc_auc', 'accuracy', 'r2', 'neg_mean_squared_error'],
        index=0,
        help="The metric used to evaluate the performance of the estimator. Common options include 'roc_auc', 'accuracy', 'r2', and 'neg_mean_squared_error'."
    )
    
    # Input for threshold
    threshold = st.number_input(
        "Threshold to drop a feature (threshold):",
        min_value=0.0,
        max_value=1.0,
        value=0.01,
        step=0.01,
        help="The value that defines whether a feature will be selected. Features with a performance below this threshold will be removed."
    )
    
    # Input for cross-validation (cv)
    cv = st.number_input(
        "Number of cross-validation folds (cv):",
        min_value=2,
        max_value=10,
        value=3,
        step=1,
        help="The number of folds to use for cross-validation."
    )
    
    # Input for groups
    groups = st.text_input(
        "Group labels for the samples (groups):",
        value="",
        help="Group labels for the samples used while splitting the dataset into train/test set. Only used in conjunction with a 'Group' cv instance (e.g., GroupKFold)."
    )
    
    # Input for confirm_variables
    confirm_variables = st.checkbox(
        "Confirm variables (confirm_variables):",
        value=False,
        help="If set to True, variables that are not present in the input dataframe will be removed from the list of variables."
    )
    
    # Button to apply Select By Single Feature Performance
    if st.button("Apply Select By Single Feature Performance", use_container_width=True, type='primary'):
        try:
            # Initialize SelectBySingleFeaturePerformance with user inputs
            sfs_selector = SelectBySingleFeaturePerformance(
                estimator=estimator,
                variables=variables if variables else None,
                scoring=scoring,
                threshold=threshold,
                cv=cv,
                groups=eval(groups) if groups else None,
                confirm_variables=confirm_variables
            )
            
            # Separate features (X) and target (y)
            X = df_clone.drop(columns=[target_variable])
            y = df_clone[target_variable]
            
            # Fit and transform the dataframe
            df_transformed = sfs_selector.fit_transform(X, y)
            
            st.write("Transformed DataFrame:")
            st.dataframe(df_transformed)
            st.session_state['count']=st.session_state['count']+1
            st.session_state[f"{st.session_state['count']}.{option}"]=df_transformed
            
            # Display the performance for each feature
            st.write("Performance for Each Feature:")
            st.write(sfs_selector.feature_performance_)
        except Exception as e:
            st.error(f"An error occurred: {e}")

def recursive_feature_elimination(option, df):
    # Clone the dataframe to preserve the original
    df_clone = df.copy()
    
    st.header("Recursive Feature Elimination Configuration")
    
    # Input for target variable (y)
    target_variable = st.selectbox(
        "Select the target variable (y):",
        options=list(df_clone.columns),
        help="The target variable for the machine learning model. This is required to evaluate feature importance."
    )
    
    # Input for variables
    variables = st.multiselect(
        "Variables to evaluate (variables):",
        options=[col for col in df_clone.columns if col != target_variable],  # Exclude target variable
        default=None,
        help="The list of variables to evaluate. If None, the transformer will evaluate all numerical features in the dataset."
    )
    
    # Input for estimator
    model_type = st.selectbox(
        "Select the model type:",
        options=['Classifier', 'Regressor'],
        index=0,
        help="Choose whether to use a classifier or regressor for feature selection."
    )
    
    if model_type == 'Classifier':
        estimator = RandomForestClassifier(random_state=42)
    else:
        estimator = RandomForestRegressor(random_state=42)
    
    # Input for scoring metric
    scoring = st.selectbox(
        "Select the scoring metric:",
        options=['roc_auc', 'accuracy', 'r2', 'neg_mean_squared_error'],
        index=0,
        help="The metric used to evaluate the performance of the estimator. Common options include 'roc_auc', 'accuracy', 'r2', and 'neg_mean_squared_error'."
    )
    
    # Input for threshold
    threshold = st.number_input(
        "Threshold to drop a feature (threshold):",
        min_value=0.0,
        max_value=1.0,
        value=0.01,
        step=0.01,
        help="The value that defines whether a feature will be selected. Features with a performance drop below this threshold will be removed."
    )
    
    # Input for cross-validation (cv)
    cv = st.number_input(
        "Number of cross-validation folds (cv):",
        min_value=2,
        max_value=10,
        value=3,
        step=1,
        help="The number of folds to use for cross-validation."
    )
    
    # Input for groups
    groups = st.text_input(
        "Group labels for the samples (groups):",
        value="",
        help="Group labels for the samples used while splitting the dataset into train/test set. Only used in conjunction with a 'Group' cv instance (e.g., GroupKFold)."
    )
    
    # Input for confirm_variables
    confirm_variables = st.checkbox(
        "Confirm variables (confirm_variables):",
        value=False,
        help="If set to True, variables that are not present in the input dataframe will be removed from the list of variables."
    )
    
    # Button to apply Recursive Feature Elimination
    if st.button("Apply Recursive Feature Elimination", use_container_width=True, type='primary'):
        try:
            # Initialize RecursiveFeatureElimination with user inputs
            rfe_selector = RecursiveFeatureElimination(
                estimator=estimator,
                variables=variables if variables else None,
                scoring=scoring,
                threshold=threshold,
                cv=cv,
                groups=eval(groups) if groups else None,
                confirm_variables=confirm_variables
            )
            
            # Separate features (X) and target (y)
            X = df_clone.drop(columns=[target_variable])
            y = df_clone[target_variable]
            
            # Fit and transform the dataframe
            df_transformed = rfe_selector.fit_transform(X, y)
            st.session_state['count']=st.session_state['count']+1
            st.session_state[f"{st.session_state['count']}.{option}"]=df_transformed
            
            st.write("Transformed DataFrame:")
            st.dataframe(df_transformed)
            
            # Display the feature importance for each feature
            st.write("Feature Importance for Each Feature:")
            st.write(rfe_selector.feature_importances_)
        except Exception as e:
            st.error(f"An error occurred: {e}")

def mrmr_feature_selection(option, df):
    # Clone the dataframe to preserve the original
    df_clone = df.copy()
    
    st.header("MRMR Feature Selection Configuration")
    
    # Input for target variable (y)
    target_variable = st.selectbox(
        "Select the target variable (y):",
        options=list(df_clone.columns),
        help="The target variable for the machine learning model. This is required to evaluate feature importance."
    )
    
    # Input for variables
    variables = st.multiselect(
        "Variables to evaluate (variables):",
        options=[col for col in df_clone.columns if col != target_variable],  # Exclude target variable
        default=None,
        help="The list of variables to evaluate. If None, the transformer will evaluate all numerical variables in the dataset."
    )
    
    # Input for method
    method = st.selectbox(
        "Select the MRMR method:",
        options=['MIQ', 'MID', 'FCD', 'FCQ', 'RFCQ'],
        index=0,
        help="How to estimate the relevance, redundance, and relation between the two. Options include 'MIQ', 'MID', 'FCD', 'FCQ', and 'RFCQ'."
    )
    
    # Input for max_features
    max_features = st.number_input(
        "Maximum number of features to select (max_features):",
        value=1 if variables is None else int(len(variables) * 0.2),
        help="The number of features to select. If None, it defaults to 20% of the features seen during fit()."
    )
    
    # Input for discrete_features
    discrete_features = st.selectbox(
        "Discrete features handling (discrete_features):",
        options=['auto', True, False],
        index=0,
        help="If bool, then determines whether to consider all features discrete or continuous. If 'auto', it is assigned to False for dense X and to True for sparse X."
    )
    
    # Input for n_neighbors
    n_neighbors = st.number_input(
        "Number of neighbors for MI estimation (n_neighbors):",
        min_value=1,
        max_value=10,
        value=3,
        step=1,
        help="Number of neighbors to use for MI estimation for continuous variables. Only used when method is 'MIQ' or 'MID'."
    )
    
    # Input for scoring
    scoring = st.selectbox(
        "Select the scoring metric:",
        options=['roc_auc', 'accuracy', 'r2', 'neg_mean_squared_error'],
        index=0,
        help="The metric used to evaluate the performance of the estimator. Only used when method = 'RFCQ'."
    )
    
    # Input for cross-validation (cv)
    cv = st.number_input(
        "Number of cross-validation folds (cv):",
        min_value=2,
        max_value=10,
        value=3,
        step=1,
        help="The number of folds to use for cross-validation. Only used when method = 'RFCQ'."
    )
    
    # Input for param_grid
    param_grid = st.text_input(
        "Hyperparameters for grid search (param_grid):",
        value="{'max_depth': [1, 2, 3, 4]}",
        help="The hyperparameters to optimize for the random forest through a grid search. Only used when method = 'RFCQ'."
    )
    
    # Input for regression
    regression = st.checkbox(
        "Is the target variable for regression? (regression):",
        value=False,
        help="Indicates whether the target is one for regression or a classification."
    )
    
    # Input for confirm_variables
    confirm_variables = st.checkbox(
        "Confirm variables (confirm_variables):",
        value=False,
        help="If set to True, variables that are not present in the input dataframe will be removed from the list of variables."
    )
    
    # Input for random_state
    random_state = st.number_input(
        "Random state for reproducibility (random_state):",
        min_value=0,
        max_value=100,
        value=42,
        step=1,
        help="Seed for reproducibility. Used when method is one of 'RFCQ', 'MIQ', or 'MID'."
    )
    
    # Input for n_jobs
    n_jobs = st.number_input(
        "Number of jobs for parallel processing (n_jobs):",
        min_value=-1,
        max_value=16,
        value=-1,
        step=1,
        help="The number of jobs to use for computing the mutual information. -1 means using all processors."
    )
    
    # Button to apply MRMR Feature Selection
    if st.button("Apply MRMR Feature Selection", use_container_width=True, type='primary'):
        try:
            # Initialize MRMR with user inputs
            mrmr_selector = MRMR(
                variables=variables if variables else None,
                method=method,
                max_features=max_features,
                discrete_features=discrete_features,
                n_neighbors=n_neighbors,
                scoring=scoring,
                cv=cv,
                param_grid=eval(param_grid) if param_grid else None,
                regression=regression,
                confirm_variables=confirm_variables,
                random_state=random_state,
                n_jobs=n_jobs
            )
            
            # Separate features (X) and target (y)
            X = df_clone.drop(columns=[target_variable])
            y = df_clone[target_variable]
            
            # Fit and transform the dataframe
            df_transformed = mrmr_selector.fit_transform(X, y)
            
            st.write("Transformed DataFrame:")
            st.dataframe(df_transformed)
            st.session_state['count']=st.session_state['count']+1
            st.session_state[f"{st.session_state['count']}.{option}"]=df_transformed
            
            # Display the feature importance for each feature
            st.write("Feature Importance for Each Feature:")
            st.write(mrmr_selector.feature_importances_)
        except Exception as e:
            st.error(f"An error occurred: {e}")

def smart_correlated_selection(option, df):
    # Clone the dataframe to preserve the original
    df_clone = df.copy()
    
    st.header("Smart Correlated Selection Configuration")
    
    # Input for target variable (y)
    target_variable = st.selectbox(
        "Select the target variable (y):",
        options=list(df_clone.columns),
        help="The target variable for the machine learning model. This is required to evaluate feature importance."
    )
    
    # Input for variables
    variables = st.multiselect(
        "Variables to evaluate (variables):",
        options=[col for col in df_clone.columns if col != target_variable],  # Exclude target variable
        default=None,
        help="The list of variables to evaluate. If None, the transformer will evaluate all numerical features in the dataset."
    )
    
    # Input for correlation method
    method = st.selectbox(
        "Select the correlation method:",
        options=['pearson', 'spearman', 'kendall'],
        index=0,
        help="The correlation method to be used to identify the correlated features. Options include 'pearson', 'spearman', and 'kendall'."
    )
    
    # Input for threshold
    threshold = st.number_input(
        "Correlation threshold (threshold):",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
        step=0.01,
        help="The correlation threshold above which a feature will be deemed correlated with another one and removed from the dataset."
    )
    
    # Input for missing values handling
    missing_values = st.selectbox(
        "Handling missing values (missing_values):",
        options=['ignore', 'raise'],
        index=0,
        help="Whether the missing values should be raised as error or ignored when determining correlation."
    )
    
    # Input for selection method
    selection_method = st.selectbox(
        "Selection method (selection_method):",
        options=['missing_values', 'cardinality', 'variance', 'model_performance'],
        index=0,
        help="The method to select features from correlated groups. Options include 'missing_values', 'cardinality', 'variance', and 'model_performance'."
    )
    
    # Input for estimator (only required if selection_method is 'model_performance')
    estimator = None
    if selection_method == 'model_performance':
        model_type = st.selectbox(
            "Select the model type:",
            options=['Classifier', 'Regressor'],
            index=0,
            help="Choose whether to use a classifier or regressor for feature selection."
        )
        
        if model_type == 'Classifier':
            estimator = RandomForestClassifier(random_state=42)
        else:
            estimator = RandomForestRegressor(random_state=42)
    
    # Input for scoring metric (only required if selection_method is 'model_performance')
    scoring = None
    if selection_method == 'model_performance':
        scoring = st.selectbox(
            "Select the scoring metric:",
            options=['roc_auc', 'accuracy', 'r2', 'neg_mean_squared_error'],
            index=0,
            help="The metric used to evaluate the performance of the estimator."
        )
    
    # Input for cross-validation (cv) (only required if selection_method is 'model_performance')
    cv = None
    if selection_method == 'model_performance':
        cv = st.number_input(
            "Number of cross-validation folds (cv):",
            min_value=2,
            max_value=10,
            value=3,
            step=1,
            help="The number of folds to use for cross-validation."
        )
    
    # Input for groups (only required if selection_method is 'model_performance')
    groups = None
    if selection_method == 'model_performance':
        groups = st.text_input(
            "Group labels for the samples (groups):",
            value="",
            help="Group labels for the samples used while splitting the dataset into train/test set. Only used in conjunction with a 'Group' cv instance (e.g., GroupKFold)."
        )
    
    # Input for confirm_variables
    confirm_variables = st.checkbox(
        "Confirm variables (confirm_variables):",
        value=False,
        help="If set to True, variables that are not present in the input dataframe will be removed from the list of variables."
    )
    
    # Button to apply Smart Correlated Selection
    if st.button("Apply Smart Correlated Selection", use_container_width=True, type='primary'):
        try:
            # Initialize SmartCorrelatedSelection with user inputs
            scs_selector = SmartCorrelatedSelection(
                variables=variables if variables else None,
                method=method,
                threshold=threshold,
                missing_values=missing_values,
                selection_method=selection_method,
                estimator=estimator,
                scoring=scoring,
                cv=cv,
                groups=eval(groups) if groups else None,
                confirm_variables=confirm_variables
            )
            
            # Separate features (X) and target (y)
            X = df_clone.drop(columns=[target_variable])
            y = df_clone[target_variable]
            
            # Fit and transform the dataframe
            df_transformed = scs_selector.fit_transform(X, y)
            st.session_state['count']=st.session_state['count']+1
            st.session_state[f"{st.session_state['count']}.{option}"]=df_transformed
            
            st.write("Transformed DataFrame:")
            st.dataframe(df_transformed)
            
            # Display the selected features
            st.write("Selected Features:")
            st.write(scs_selector.features_to_drop_)
        except Exception as e:
            st.error(f"An error occurred: {e}")
