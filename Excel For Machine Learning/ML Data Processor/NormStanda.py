import streamlit as st
import pandas as pd
from sklearn.preprocessing import *

class Standadi:
  def __init__(self,df):
    self.dataset=df
  def display(self):
    options=st.selectbox("Select options To Perform",["MaxAbs Scaler","MinMaxScaler","RobustScaler","StandardScaler"])
    if options=="StandardScaler":
      self.standard_scaler()
    if options=="RobustScaler":
      self.robust_scaler()
    if options=="MinMaxScaler":
      self.min_max_scaler()
    if options=="MaxAbs Scaler":
      self.max_abs_scaler()
  def standard_scaler(self):
    try:
        data = self.dataset.copy(deep=True)
        columns = st.multiselect("Select the columns", self.dataset.columns.tolist())
        with_mean = st.checkbox("Center Data (with_mean)", value=True)
        with_std = st.checkbox("Scale Data (with_std)", value=True)
        
        if columns and st.button("Apply Standard Scaler", use_container_width=True, type='primary'):
            scaler = StandardScaler(with_mean=with_mean, with_std=with_std)
            data[columns] = scaler.fit_transform(data[columns])
            st.session_state.setdefault('allData', {})[f'Stage-Normalization-StandardScaler-{columns}'] = data
            st.dataframe(data)
    except Exception as e:
        st.error(f"Error: {e}")
      
  def robust_scaler(self):
    try:
        data = self.dataset.copy(deep=True)
        columns = st.multiselect("Select the columns", self.dataset.columns.tolist())
        quantile_range = st.text_input("Enter quantile range (e.g., 25,75)", "25,75")
        with_centering = st.checkbox("Center Data", value=True)
        with_scaling = st.checkbox("Scale Data", value=True)
        
        if columns and st.button("Apply Robust Scaler", use_container_width=True, type='primary'):
            try:
                q_min, q_max = map(float, quantile_range.split(","))
                scaler = RobustScaler(with_centering=with_centering, with_scaling=with_scaling, quantile_range=(q_min, q_max))
                data[columns] = scaler.fit_transform(data[columns])
                st.session_state.setdefault('allData', {})[f'Stage-Normalization-RobustScaler-{columns}'] = data
                st.dataframe(data)
            except ValueError:
                st.error("Invalid quantile range format. Please enter two numbers separated by a comma.")
    except Exception as e:
        st.error(f"Error: {e}")
  def min_max_scaler(self):
    try:
      data=self.dataset.copy(deep=True)
      feature_range=st.text_area("Describe Feature Ranges like this (0,1) for each column comma seperated")
      column=st.selectbox("Select the columns",self.dataset.columns.tolist())
      if st.button("Apply Max Abs Scaler",use_container_width=True,type='primary'):
        data[column]=MinMaxScaler(feature_range=eval(feature_range)).fit(data[column])
        st.session_state['allData'][f'Stage-Normalization&Standadization-MaxAbsScaler-{column}']=data
        st.dataframe(data)
    except Exception as e:
      st.error(e)
  def max_abs_scaler(self):
    try:
      data=self.dataset.copy(deep=True)
      columns=st.multiselect("Select the columns",self.dataset.columns.tolist())
      if st.button("Apply Max Abs Scaler",use_container_width=True,type='primary'):
        data[columns]=MaxAbsScaler().fit_transform(data[columns])
        st.session_state['allData'][f'Stage-Normalization&Standadization-MaxAbsScaler-{columns}']=data
        st.dataframe(data)
    except Exception as e:
      st.error(e)
    
