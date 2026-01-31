import streamlit as st
import pandas as pd
import janitor as jn
import missingno as mno
from DATACLEANERS import *
from feature_engine.discretisation import *
from feature_engine.transformation import *
from DataCleaners import DataCleaners
from ENCODERS import Encoders
from NormStanda import *
class Ml:
  def __init__(self,df):
    self.dataset=df
    self.pandas_methods=PandasMethods(df)
    self.univariate_imputers=UnivariateImputers(df)
    self.data_cleaners=DataCleaners(df)
    self.encoders=Encoders(df)
    self.norm_standas=Standadi(df)
  def display(self):
    tab1,tab2,tab3=st.tabs(["Perfrom Operations","View Operations","Delete Memory"])
    with tab1:
      col1,col2=st.columns([1,2],border=True)
      options=col1.radio("Operation You Want To Perform",["Missing Data","Encode Target Variables",
                                                          "Discritization/Binning","Outlier detection","Varience Stabilizing Transformations",
                                                         "Normalization & Standadization"])
      if options=="Normalization & Standadization":
        with col2:
          self.norm_standas.display()
      if options=="Encode Target Variables":
        encoder_dict = {"Base": self.encoders.apply_basen_encoder,"Binary": self.encoders.apply_binary_encoder,
        "Catboost": self.encoders.apply_catboost_encoder,"Count": self.encoders.apply_count_encoder,
        "Hashing": self.encoders.apply_hashing_encoder,"Helmert": self.encoders.apply_helmert_encoder,
        "James Stein": self.encoders.apply_james_stein_encoder,"Leave One Out": self.encoders.apply_leave_one_out_encoder,
        "M Estimate": self.encoders.apply_m_estimate_encoder,"One Hot": self.encoders.apply_one_hot_encoder,
        "Ordinal": self.encoders.apply_ordinal_encoder,"Polynomial": self.encoders.apply_polynomial_encoder,
        "Quantile": self.encoders.apply_quantile_encoder,"Rank Hot": self.encoders.apply_rankhot_encoder,
        "Sum": self.encoders.apply_sum_encoder,"Summary": self.encoders.apply_summary_encoder,
        "Target": self.encoders.apply_target_encoder,"WOE": self.encoders.apply_woe_encoder,
        }
        option_mode=col2.selectbox("Select the encoding Technique",encoder_dict.keys())
        if option_mode:
          with col2:
            dataFrame=encoder_dict[option_mode]()
            st.session_state['allData'][f'Stage - Encoding - {option_mode}']=dataFrame
      if options=="Missing Data":
        option_mode=col2.selectbox("Select any one operation",["Detect Missing Values","Total Missing Values","Visualize Missing Values","Impute Missing Values"])
        if option_mode=="Detect Missing Values":
          self.detect_missing(col2)
        if option_mode=="Total Missing Values":
          self.total_missing(col2)
        if option_mode=="Impute Missing Values":
          self.impute_missing(col2)
        if option_mode=="Visualize Missing Values":
          self.visualize_missing_data(col2)
      if options=="Discritization/Binning":
        different_options=col2.selectbox("Select the descritization technique",["Binarizer","Multi Label Binarizer","Equal Frequency Descritization","Equal Width Descritization","Arbitery Descritization","Descision Tree Descritizer"])
        if different_options=="Binarizer":
          self.data_cleaners.binarize(col2)
        if different_options=="Multi Label Binarizer":
          self.data_cleaners.multi_label_binarizer(col2)
        if different_options=="Equal Frequency Descritization":
          self.equal_frequency_descritization(col2)
        if different_options=="Equal Width Descritization":
          self.equal_width_descritization(col2)
        if different_options=="Arbitery Descritization":
          self.arbitrary_discretization(col2)
        if different_options=="Descision Tree Descritizer":
          self.geometric_width_discretization(col2)
        if different_options=="KBins Descritizer":
          self.kbins_descritizer(col2)
      if options=="Outlier detection":
        different_options=col2.selectbox("Selct an outlier method",["Winsorizer","Outlier Trimmer"])
        if different_options=="Winsorizer":
          self.winsorizer(col2)
        if different_options=="Outlier Trimmer":
          self.outlier_trimmer(col2)
      if options=="Varience Stabilizing Transformations":
        different_options=col2.selectbox("Select a varience stabilizing transformations",["Log Transformer","Log CP Transformer",
                                                                                          "Reciprocal Transformer","Arc Sin Transformer",
                                                                                          "Power transformer","boxCox Transformer","yeojhonson Transfoermer"])
        if different_options=="Log Transformer":
          self.log_transformer(col2)
        if different_options=="Log CP Transformer":
          self.log_cp_transformer(col2)
        if different_options=="Reciprocal Transformer":
          self.reciprocal_transformer(col2)
        if different_options=="Arc Sin Transformer":
          self.arc_sin_transformer(col2)
        if different_options=="Power transformer":
          self.power_transformer(col2)
        if different_options=="boxCox Transformer":
          self.box_cox_transformer(col2)
        if different_options=="yeojhonson Transfoermer":
          self.yeo_jhonson_transformer(col2)      
    with tab2:
      st.subheader("Your Data",divider='blue')
      st.dataframe(self.dataset)
    with tab3:
      keys=st.selectbox("Please select the data to delete",st.session_state["allData"].keys())
      if keys:
        st.subheader("Your Data Looks Like",divider='blue')
        st.dataframe(st.session_state['allData'][keys])
  def detect_missing(self,col2):
    col2.subheader("Detected Missing Values",divider='blue')
    dataframe=self.dataset.isna().sum()
    col2.dataframe(dataframe)
  def total_missing(self,col2):
    col2.subheader("Total Missing Values Found In The Dataset",divider='blue')
    total_missing_values=self.dataset.isna().sum().sum()
    col2.info(f"Total Number Of Missing Values : {total_missing_values}")
  def visualize_missing_data(self, col2):
    col2.subheader("Visualize the missing Data", divider='blue')
    fig, ax = plt.subplots()
    self.dataset.isna().sum().plot(kind='line', ax=ax)
    st.pyplot(fig)
  def impute_missing(self,col2):
    values=col2.selectbox("Select Techniques",["Fill Missing Values By Direction","Fill Missing Values By Imputation"])
    if values == "Fill Missing Values By Direction":
      columns = col2.multiselect("Select Columns", self.dataset.columns.tolist())
      directions = col2.text_area("Give Directions ',' separated if more than 1, direction : up,down,downup,updown")
      if col2.button("Fill It", use_container_width=True, type='primary'):
          directions = directions.split(',')
          if len(columns) != len(directions):
              col2.warning("Directions Count Must Be Equal To Columns Count")
          else:
              try:
                  mapper = {columns[x]: directions[x].strip() for x in range(len(columns))}
                  dataframe = self.dataset.copy()
                  dataframe = dataframe.fill_direction(**mapper)
                  key = f"Stage-8-Machine Learning Operations - Fill Missing - Fill Direction - {mapper}"
                  st.session_state.setdefault("allData", {})[key] = dataframe
                  col2.dataframe(dataframe)
              except ValueError as e:
                  col2.error(f"Invalid direction specified: {e}")
              except Exception as e:
                  col2.error(f"An error occurred: {e}")
    if values == "Fill Missing Values By Imputation":
      options=col2.selectbox("Select The Imputation Tehnique",["MeanMedianImputer","EndTailImputer",
                                                               "RandomSampleImputer","AddMissingImputer",
                                                               "DropMissingData"])
      if options=="MeanMedianImputer":
        data=self.univariate_imputers.MeanMedianImputer()
        key="Stage 8 - Missing Data - Impute - MeanMeadianImputer"
        st.session_state['allData'][key]=data
      if options=="EndTailImputer":
        data=self.univariate_imputers.EndTailImputer()
        key="Stage 8 - Missing Data - Impute - EndTailImputer"
        st.session_state['allData'][key]=data
      if options=="RandomSampleImputer":
        data=self.univariate_imputers.RandomSampleImputer()
        key="Stage 8 - Missing Data - Impute - RandomSampleImputer"
        st.session_state['allData'][key]=data
      if options=="AddMissingImputer":
        data=self.univariate_imputers.AddMissingIndicator()
        key="Stage 8 - Missing Data - Impute - AddMissingImputer"
        st.session_state['allData'][key]=data
      if options=="DropMissingData":
        pass
  def equal_frequency_descritization(self, col2):
    variables = col2.multiselect(
        "Please select the columns on which you want to perform discretization",
        ["All Columns"] + self.dataset.columns.tolist()
    )
    
    if "All Columns" in variables:
        variables = None
    
    y = col2.selectbox("Select the target variable", [None] + self.dataset.columns.tolist())
    q = int(col2.number_input("Desired number of equal frequency intervals / bins.", min_value=1, value=10))
    return_object = col2.checkbox(
        "Return discrete variable as type object (True) or numeric (False). "
        "Use True if encoding with Feature-engine’s categorical encoders."
    )
    return_boundaries = col2.checkbox("Return interval boundaries instead of integers.")
    precision = int(col2.number_input("Precision for bin labels.", min_value=0, value=3))
    
    if col2.button("Continue to apply", use_container_width=True, type='primary'):
        try:
            efd = EqualFrequencyDiscretiser(
                variables=variables, q=q, return_object=return_object, 
                return_boundaries=return_boundaries, precision=precision
            )
            
            transformed_data = efd.fit_transform(self.dataset)
            
            key = f"Stage - ML - discretization - equal frequency - {variables if variables else 'All Columns'}"
            st.session_state.setdefault('allData', {})[key] = transformed_data
            col2.dataframe(transformed_data)
            
            st.success("Equal Frequency Discretization applied successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
  def equal_width_descritization(self, col2):
    variables = col2.multiselect(
        "Please select the columns on which you want to perform discretization",
        ["All Columns"] + self.dataset.columns.tolist()
    )
    
    if "All Columns" in variables:
        variables = None
    
    bins = int(col2.number_input("Desired number of equal width intervals / bins.", min_value=1, value=10))
    return_object = col2.checkbox(
        "Return discrete variable as type object (True) or numeric (False). "
        "Use True if encoding with Feature-engine’s categorical encoders."
    )
    return_boundaries = col2.checkbox("Return interval boundaries instead of integers.")
    precision = int(col2.number_input("Precision for bin labels.", min_value=0, value=3))
    
    if col2.button("Continue to apply", use_container_width=True, type='primary'):
        try:
            ewd = EqualWidthDiscretiser(
                variables=variables, bins=bins, return_object=return_object, 
                return_boundaries=return_boundaries, precision=precision
            )
            
            transformed_data = ewd.fit_transform(self.dataset)
            
            key = f"Stage - ML - discretization - equal width - {variables if variables else 'All Columns'}"
            st.session_state.setdefault('allData', {})[key] = transformed_data
            col2.dataframe(transformed_data)
            
            st.success("Equal Width Discretization applied successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
  def arbitrary_discretization(self, col2):
    variables = col2.multiselect(
        "Please select the columns on which you want to perform discretization",
        self.dataset.columns.tolist()
    )
    
    binning_dict = {}
    for var in variables:
        bins_input = col2.text_input(f"Enter bin edges for {var} (comma-separated values)")
        if bins_input:
            try:
                binning_dict[var] = list(map(int, bins_input.split(',')))
            except ValueError:
                st.error(f"Invalid input for {var}. Please enter numeric values separated by commas.")
    
    return_object = col2.checkbox(
        "Return discrete variable as type object (True) or numeric (False). "
        "Use True if encoding with Feature-engine’s categorical encoders."
    )
    return_boundaries = col2.checkbox("Return interval boundaries instead of integers.")
    precision = int(col2.number_input("Precision for bin labels.", min_value=0, value=3))
    errors = col2.selectbox("Error handling for out-of-bound values", ["ignore", "raise"], index=0)
    
    if col2.button("Continue to apply", use_container_width=True, type='primary'):
        try:
            ad = ArbitraryDiscretiser(
                binning_dict=binning_dict, return_object=return_object, 
                return_boundaries=return_boundaries, precision=precision, errors=errors
            )
            
            transformed_data = ad.fit_transform(self.dataset)
            
            key = f"Stage - ML - discretization - arbitrary - {variables}"
            st.session_state.setdefault('allData', {})[key] = transformed_data
            col2.dataframe(transformed_data)
            
            st.success("Arbitrary Discretization applied successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
  def descisio_tree_descritizer(self, col2):
    variables = col2.multiselect(
        "Please select the columns on which you want to perform discretization",
        self.dataset.columns.tolist()
    )
    
    bin_output = col2.selectbox(
        "Select bin output type", ["prediction", "bin_number", "boundaries"], index=0
    )
    precision = col2.number_input("Precision for bin labels (if applicable)", min_value=0, value=3, step=1)
    cv = col2.number_input("Number of cross-validation folds", min_value=2, value=3, step=1)
    scoring = col2.text_input("Scoring metric (default: neg_mean_squared_error)", value="neg_mean_squared_error")
    regression = col2.checkbox("Train regression tree? (Uncheck for classification)", value=True)
    random_state = col2.number_input("Random state (for reproducibility)", value=42, step=1)
    
    if col2.button("Continue to apply", use_container_width=True, type='primary'):
        try:
            dtd = DecisionTreeDiscretiser(
                variables=variables, bin_output=bin_output, precision=precision,
                cv=cv, scoring=scoring, regression=regression, random_state=random_state
            )
            
            transformed_data = dtd.fit_transform(self.dataset)
            
            key = f"Stage - ML - discretization - decision_tree - {variables}"
            st.session_state.setdefault('allData', {})[key] = transformed_data
            col2.dataframe(transformed_data)
            
            st.success("Decision Tree Discretization applied successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
  def geometric_width_discretization(self, col2):
    variables = col2.multiselect(
        "Please select the columns on which you want to perform discretization",
        self.dataset.columns.tolist()
    )
    
    bins = col2.number_input("Desired number of geometric width intervals / bins", min_value=2, value=10, step=1)
    return_object = col2.checkbox("Return discrete variable as object? (Enable for categorical encoding)", value=False)
    return_boundaries = col2.checkbox("Return interval boundaries instead of integers?", value=False)
    precision = col2.number_input("Precision for bin labels", min_value=1, value=7, step=1)
    
    if col2.button("Continue to apply", use_container_width=True, type='primary'):
        try:
            gwd = GeometricWidthDiscretiser(
                variables=variables, bins=bins, return_object=return_object,
                return_boundaries=return_boundaries, precision=precision
            )
            
            transformed_data = gwd.fit_transform(self.dataset)
            
            key = f"Stage - ML - discretization - geometric_width - {variables}"
            st.session_state.setdefault('allData', {})[key] = transformed_data
            col2.dataframe(transformed_data)
            
            st.success("Geometric Width Discretization applied successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
  def kbins_descritizer(self,col2):
    pass
  def outliers_params(self, col2, outlier):
    capping_method = col2.selectbox(
        "Select outlier detection method:", ["gaussian", "iqr", "mad", "quantiles"]
    )
    tail = col2.selectbox("Select tail(s) for outlier detection:", ["right", "left", "both"])
    fold = col2.number_input("Fold factor (std, MAD, or IQR multiplier):", min_value=0.1, value=3.0)
    add_indicators = col2.checkbox("Add indicator variables for capped outliers?")
    variables = col2.multiselect("Select numerical variables to transform:", self.dataset.select_dtypes(include=['number']).columns.tolist())
    missing_values = col2.selectbox("Handle missing values:", ["raise", "ignore"])
    
    if col2.button(f"Implement {outlier}", use_container_width=True, type='primary'):
        if outlier == "Winsorizer":
            transformer = Winsorizer(
                capping_method=capping_method,
                tail=tail,
                fold=fold,
                add_indicators=add_indicators,
                variables=variables if variables else None,
                missing_values=missing_values
            )
            action = "Applied Winsorizer"
        else:
            transformer = OutlierTrimmer(
                capping_method=capping_method,
                tail=tail,
                fold=fold,
                variables=variables if variables else None,
                missing_values=missing_values
            )
            action = "Applied OutlierTrimmer"
        
        try:
            dataset = transformer.fit_transform(self.dataset)
            st.session_state['allData'][f"Stage-8-Ml-{outlier} with method={capping_method}, tail={tail}, fold={fold}"]=dataset
            col2.dataframe(dataset)
            col2.success("Outlier handling applied successfully!")
        except Exception as e:
            st.error(f"Error applying {outlier}: {e}")


  def winsorizer(self,col2):
    self.outliers_params(col2,"Winsorizer")
  def outlier_trimmer(self,col2):
    self.outliers_params(col2,"Outlier Trimmer")
  def variance_transformer(self, col2, transformer):
        try:
            variables = col2.multiselect(
                "The list of numerical variables to transform. If None, the transformer will automatically find and select all numerical variables.",
                [None] + self.dataset.columns.tolist()
            )

            if transformer in ["Reciprocal Transformer", "ArcSin Transformer", "BoxCox Transformer", "YeoJohnson Transformer"]:
                return variables if variables and variables != [None] else None

            if transformer in ["Log Transformer", "Log CP Transformer"]:
                base = col2.text_input("Indicates if the natural or base 10 logarithm should be applied. Can take values ‘e’ or ‘10’.", "e")
                if transformer == "Log CP Transformer":
                    C = int(col2.number_input("The constant C to add to the variable before the logarithm, i.e., log(x + C)", value=1))
                    return variables, base, C
                return variables, base

            if transformer == "PowerTransformer":
                exp = col2.number_input("The power (or exponent).", value=0.5)
                return variables, exp

            return variables
        except Exception as e:
            st.error(f"Error in variance_transformer: {str(e)}")
            return None

  def apply_transformation(self, col2, transformer_class, transformer_name, *args):
      try:
          if col2.button(f"Apply {transformer_name}", use_container_width=True, type='primary'):
              # Ensure variables exist before applying transformation
              if isinstance(args[0], list) and len(args[0]) > 0:
                  obj = transformer_class(*args)
                  data = obj.fit_transform(self.dataset[args[0]])
              else:
                  obj = transformer_class(*args[1:])
                  data = obj.fit_transform(self.dataset)
  
              st.session_state['allData'][f"Stage 8 - ML - Variance Stabilize - {transformer_name} - {args[0] if args else 'All'}"] = data
              col2.dataframe(data)
  
      except Exception as e:
          st.error(f"Error in {transformer_name}: {str(e)}")
  
  def log_transformer(self, col2):
      result = self.variance_transformer(col2, "Log Transformer")
      if result:
          self.apply_transformation(col2, LogTransformer, "Log Transformer", *result)
  
  def log_cp_transformer(self, col2):
      result = self.variance_transformer(col2, "Log CP Transformer")
      if result:
          self.apply_transformation(col2, LogCpTransformer, "Log CP Transformer", *result)
  
  def reciprocal_transformer(self, col2):
      result = self.variance_transformer(col2, "Reciprocal Transformer")
      if result:
          self.apply_transformation(col2, ReciprocalTransformer, "Reciprocal Transformer", result)
  
  def box_cox_transformer(self, col2):
      result = self.variance_transformer(col2, "BoxCox Transformer")
      if result:
          self.apply_transformation(col2, BoxCoxTransformer, "BoxCox Transformer", result)
  
  def yeo_jhonson_transformer(self, col2):
      result = self.variance_transformer(col2, "YeoJohnson Transformer")
      if result:
          self.apply_transformation(col2, YeoJohnsonTransformer, "YeoJohnson Transformer", result)
  
  def arc_sin_transformer(self, col2):
      result = self.variance_transformer(col2, "ArcSin Transformer")
      if result:
          self.apply_transformation(col2, ArcsinTransformer, "ArcSin Transformer", result)
  
  def power_transformer(self, col2):
      result = self.variance_transformer(col2, "PowerTransformer")
      if result:
          self.apply_transformation(col2, PowerTransformer, "Power Transformer", *result)
