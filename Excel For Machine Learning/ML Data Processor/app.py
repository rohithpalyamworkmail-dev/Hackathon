import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import chardet
import io
from ATTRIBUTES import ATTRIBUTES
from COMPARE import COMPARE
from accessModify import *
from AddDelete import AddDelete
from AddPlots import Plots
from MODIFICATIONS import *
from FILTERS import Filters
from MATHS import Maths
from Dashboard import GenerativeAI
from MACHINELEARNING import *
from OptimizeData import OptimizeData
from GenAI import GenAI
from STRINGS import *
from Exports import *
from aboutTheApp import About
from UPDATES import Updates
from COLLABORATIONS import Collaborate
# Initialize session state for storing dataframes
if "allData" not in st.session_state:
    st.session_state["allData"] = {}

def detect_encoding_and_read(file):
    # Read a sample of the file for encoding detection
    raw_data = file.read()
    file.seek(0)  # Reset pointer to beginning after reading
    
    result = chardet.detect(raw_data)  # Detect encoding
    encoding = result['encoding']
    confidence = result['confidence']
    
    if encoding is None:
        encoding = 'utf-8'  # Fallback encoding if detection fails
    
    try:
        # Try reading with detected encoding
        df = pd.read_csv(io.StringIO(raw_data.decode(encoding)), encoding=encoding)
    except Exception:
        # If detected encoding fails, fall back to 'utf-8'
        df = pd.read_csv(io.StringIO(raw_data.decode('utf-8', errors='ignore')), encoding='utf-8')
    
    return df, encoding, confidence

# Streamlit UI
st.header("Data Preprocessor", divider='blue')

dataframe = st.sidebar.file_uploader("Upload file", type=['csv'])

if dataframe:
    if "readed_csv" not in st.session_state.get("allData", {}):
        df, encoding, confidence = detect_encoding_and_read(dataframe)
        if "allData" not in st.session_state:
            st.session_state["allData"] = {}
        st.session_state["allData"]["readed_csv"] = df
        st.write(f"Detected Encoding: {encoding} (Confidence: {confidence:.2f})")
        st.dataframe(df.head())


# Selectbox to choose the dataframe for operations
selected_data = st.selectbox("Please select the dataframe to perform operation", st.session_state["allData"].keys())

# Sidebar menu for selecting operations
with st.sidebar:
    options = option_menu(
        "Select the operation to perform",
        ["About The App","View Data","Delete Data","Optimize DataFrame","Attributes","Dashboard", "Compare DataFrames","Modifications","Filterations","Mathematical & Statistical",
          "Update DataFrames", "Add & Delete", "Access", "Plot Data","Famous Machine Learning Steps","String Manipulation","GenAI","Exports","collaborate"],
        icons=["eye","eraser","info-circle","info-circle", "columns","columns","search","columns", "pen", "pencil-square",
               "trash", "tools", "book","robot","pencil","sun","moon","meet"],
        menu_icon='gear',
        default_index=0
    )

# Perform operation based on selected option
if options=="About The App":
    About().display()
elif options=="View Data":
    tab1,tab2=st.tabs(["Perform Operations","View Operation"])
    with tab1:
        st.subheader("Your Data",divider='blue')
        if selected_data:
            df = st.session_state["allData"][selected_data]
            st.dataframe(df)
        else:
            st.warning("No Data IS Present To Select")
    with tab2:
        st.video("https://youtu.be/AbDKlzAzp7Y")
elif options=="Delete Data":
    tab1,tab2=st.tabs(["Perform Operation","Refernce"])
    with tab1:
        st.subheader("Data Going To Delete",divider='blue')
        if selected_data:
            df = st.session_state["allData"][selected_data]
            st.dataframe(df)
            if st.button("Delete Selected Data",use_container_width=True,type='primary'):
                del st.session_state["allData"][selected_data]
                st.rerun()
        else:
            st.warning("No Data IS Present To Select")
    with tab2:
        st.video("https://youtu.be/lfjqRr7v2ZE")
    
elif options == "Attributes":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        attributes = ATTRIBUTES(df)
        attributes.display()

elif options == "Compare DataFrames":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        compare = COMPARE(df)
        compare.display()
elif options == "Dashboard":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        compare = GenerativeAI(df)
        compare.display()
elif options == "Mathematical & Statistical":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        attributes = Maths(df)
        attributes.display()

elif options == "Add & Delete":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        compare = AddDelete(df)
        compare.display()

elif options == "Access":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        compare = AccessModify(df)
        compare.display()
    

elif options == "Plot Data":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        attributes = Plots(df)
        attributes.display()
elif options=="Modifications":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        attributes = MODIFICATIONS(df)
        attributes.display()
elif options=="Filterations":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        attributes = Filters(df)
        attributes.display()
elif options=="Famous Machine Learning Steps":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        attributes = Ml(df)
        attributes.display()
elif options=="Optimize DataFrame":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        attributes = OptimizeData(df)
        attributes.display()
elif options=="GenAI":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        attributes = GenAI(df)
        attributes.display()
elif options=="String Manipulation":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        attributes = Strings(df)
        attributes.display()
elif options=="Exports":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        attributes = Exports(df)
        attributes.display()
elif options=="Update DataFrames":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        updates = Updates(df)
        updates.display()
elif options=="collaborate":
    if selected_data:
        df = st.session_state["allData"][selected_data]
        updates = Collaborate(df)
        updates.display()
