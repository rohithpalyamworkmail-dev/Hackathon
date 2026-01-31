import streamlit as st
import pandas as pd
import time
from streamlit_extras.metric_cards import style_metric_cards

class About:
    def __init__(self):
        pass
    def stream_text(self, text):
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.2)

    def display(self):
        # Display a high-quality image as a banner
        st.image("./images/ba.png", use_container_width=True)
        
        # Title and Introduction
        st.header("About The App")
        st.write(
            "This application is a powerful data analysis and visualization tool, "
            "similar to Excel and Power BI. It allows users to perform various "
            "operations, preprocess data efficiently, and visualize insights through "
            "an intuitive graphical interface. With support for CSV and Excel files, "
            "the app enhances the data analysis workflow by integrating multiple "
            "functionalities, making data handling seamless."
        )

        st.write(
            "Users can explore their datasets using various functions, optimize "
            "DataFrames for better performance, and preprocess data effectively. "
            "Additionally, the application provides visualization tools to gain "
            "insights and supports exporting processed data. The app also offers "
            "real-time updates and interactive dashboards, allowing users to "
            "monitor and analyze their data dynamically."
        )

        st.write(
            "With a user-friendly interface, the app ensures that even users "
            "with minimal technical knowledge can easily clean, transform, "
            "and visualize data. The inclusion of automated preprocessing "
            "steps, such as handling missing values and data type conversions, "
            "further enhances the experience."
        )
        
        # Features Header
        st.subheader("Key Features")
        
        # Metric Cards Display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Functions To Perform To Know Information Of The Dataset", "20+")
        with col2:
            st.metric("Functions To Perform To Optimize Data Frames", "2+")
        with col3:
            st.metric("Functions To Perform Data Preprocessing", "100+")
        
        # Style the metric cards
        style_metric_cards(border_left_color="#4CAF50")
        
        st.write(
            "This tool is designed to empower users with an extensive suite of "
            "functionalities, ensuring a smooth and effective data analysis experience. "
            "Whether you are a data scientist, business analyst, or a beginner exploring "
            "data processing, this app provides all the essential tools you need in one place."
        )
        
