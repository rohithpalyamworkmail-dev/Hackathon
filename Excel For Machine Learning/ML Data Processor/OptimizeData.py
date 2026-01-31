import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from klib.clean import data_cleaning
from klib import pool_duplicate_subsets
from klib.describe import cat_plot, corr_mat, corr_plot, dist_plot, missingval_plot

class OptimizeData:
    def __init__(self, df):
        self.dataset = df

    def display(self):
        tab1, tab2 = st.tabs(["Perform Operations", "References"])

        with tab1:
            col1, col2 = st.columns([1, 2], border=True)

            if col1.toggle("Optimize Data"):
                dataset = self.dataset
                newDataset = data_cleaning(dataset)

                # Store the cleaned dataset in session state
                st.session_state['allData']["Stage 1 - Optimize Data - Clean Data(Normal)"] = newDataset

                col2.subheader("Optimized Data", divider='blue')
                col2.dataframe(newDataset)

                col2.subheader("Some Info On How Data Is Cleaned & Optimized", divider='blue')
                col2.text("By applying klib.data_cleaning(), the size reduces significantly...")

            if col1.toggle("Advanced Optimization Methods"):
                dataset = self.dataset

                # Convert to Parquet with Snappy compression
                parquet_path = "Optimized_Parquet.parquet"
                dataset.to_parquet(parquet_path, compression="snappy")

                # Read from Parquet and convert to Feather
                df_parquet = pd.read_parquet(parquet_path)
                feather_path = "Optimized_Feather.feather"
                df_parquet.to_feather(feather_path)

                # Read back from Feather for fast computations
                df_feather = pd.read_feather(feather_path)

                # Store optimized data in session state
                st.session_state['allData']["Stage 2 - Optimize Data - Feather Format"] = df_feather

                col2.subheader("Optimized Data (Feather Format)", divider='blue')
                col2.dataframe(df_feather)

                col2.subheader("Compression & Speed Details", divider='blue')
                col2.text("Converted to Parquet (high compression) -> Converted to Feather (fast access).")

        with tab2:
            st.video("https://youtu.be/Fx4LiSg-ZuE")
