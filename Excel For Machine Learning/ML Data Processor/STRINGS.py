from textblob import TextBlob
import streamlit as st
import pandas as pd
from textblob import download_corpora

class Strings:
  def __init__(self,dataset):
    self.dataset=dataset
  def display(self):
    tab1,tab2,tab3=st.tabs(["Basic String Functions","Advanced String Functions","View Data Here"])
    with tab1:
      col1,col2=st.columns([1,2],border=True)
      option=col1.radio("Select Operations From This Column",["Capitalize","Tiltle","Lower Case","Upper Case",
                                                              "Change Cases","Center String","Count","Ends With",
                                                              "Starts With","find substring strting position from left",
                                                              "find substring starting position from right","is alpha numeric",
                                                              "is alpha","is decimal","is int","is ascii","is lower","is upper",
                                                              "is printable","is space","is title","split","right split","remove preffix",
                                                              "remove suffix","trim white spaces on both sides of text",
                                                              "trim white spaces on left side of the etxt",
                                                              "trim white spaces on the right side of the text"])
      try:
        if option=="Capitalize":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[selected_columns+"(Capitalized)"]=self.dataset[selected_columns].str.capitalize()
            col2.dataframe(data)
        elif option =="Tiltle":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data=self.dataset.copy(deep=True)
            data[selected_columns+"(Titled)"]=self.dataset[selected_columns].str.title()
            col2.dataframe(data)
        elif option == "Lower Case":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[selected_columns+"(lower)"]=self.dataset[selected_columns].str.lower()
            col2.dataframe(data)
        elif option == "Upper Case":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[selected_columns+"(upper)"]=self.dataset[selected_columns].str.upper()
            col2.dataframe(data)
        elif option == "Change Cases":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[selected_columns+"(upper)"]=self.dataset[selected_columns].str.swapcase()
            col2.dataframe(data)
        elif option =="Center String":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          total_charcters=int(col2.number_input("Select the total number of characters when the string is centered",1))
          startswith=col2.text_input("Enter deleimeter or any symbol or any character to pand on left and right of the string")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Centered)-{total_charcters}-{startswith}"]=self.dataset[selected_columns].str.center(total_charcters,startswith)
            col2.dataframe(data)
        elif option == "Count":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Sub String To Know Its Frequencies")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(count)-{startswith}"]=self.dataset[selected_columns].str.count(startswith)
            col2.dataframe(data)
        elif option == "Ends With":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Suffix To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(endswith)-{startswith}"]=self.dataset[selected_columns].str.endswith(startswith)
            col2.dataframe(data)
        elif option == "find substring strting position from left":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Sub string To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Left Find)-{startswith}"]=self.dataset[selected_columns].str.find(startswith)
            col2.dataframe(data)
        elif option == "Starts With":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Prefix To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Starts With)-{startswith}"]=self.dataset[selected_columns].str.startswith(startswith)
            col2.dataframe(data)
        elif option == "Starts With":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Prefix To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Starts With)-{startswith}"]=self.dataset[selected_columns].str.startswith(startswith)
            col2.dataframe(data)
        elif option == "Starts With":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Prefix To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Starts With)-{startswith}"]=self.dataset[selected_columns].str.startswith(startswith)
            col2.dataframe(data)
        elif option == "Starts With":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Prefix To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Starts With)-{startswith}"]=self.dataset[selected_columns].str.startswith(startswith)
            col2.dataframe(data)
        elif option == "Starts With":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Prefix To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Starts With)-{startswith}"]=self.dataset[selected_columns].str.startswith(startswith)
            col2.dataframe(data)
        elif option == "Starts With":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Prefix To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Starts With)-{startswith}"]=self.dataset[selected_columns].str.startswith(startswith)
            col2.dataframe(data)
        elif option == "Starts With":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Prefix To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Starts With)-{startswith}"]=self.dataset[selected_columns].str.startswith(startswith)
            col2.dataframe(data)
        elif option == "Starts With":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Prefix To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Starts With)-{startswith}"]=self.dataset[selected_columns].str.find(startswith,"Not Present")
            col2.dataframe(data)
        elif option == "find substring starting position from right":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          startswith=col2.text_input("Enter Sub String To Check")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(Starts With)-{startswith}"]=self.dataset[selected_columns].str.rfind(startswith,"Not Present")
            col2.dataframe(data)
        elif option == "is alpha numeric":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(is alpha numeric)"]=self.dataset[selected_columns].str.isalnum()
            col2.dataframe(data)
        elif option == "is alpha":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(is alpha)"]=self.dataset[selected_columns].str.isalpha()
            col2.dataframe(data)
        elif option == "is decimal":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(is decimal)"]=self.dataset[selected_columns].str.isdecimal()
            col2.dataframe(data)
        elif option == "is int":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(is int)"]=self.dataset[selected_columns].str.isdigit()
            col2.dataframe(data)
        elif option == "is ascii":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(is alpha numeric)"]=self.dataset[selected_columns].str.isascii()
            col2.dataframe(data)
        elif option == "is lower":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(is alpha)"]=self.dataset[selected_columns].str.islower()
            col2.dataframe(data)
        elif option == "is upper":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(is upper)"]=self.dataset[selected_columns].str.isupper()
            col2.dataframe(data)
        elif option == "is upper":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(is upper)"]=self.dataset[selected_columns].str.isupper()
            col2.dataframe(data)
        elif option == "is printable":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(is printable)"]=self.dataset[selected_columns].str.isprintabel()
            col2.dataframe(data)
        elif option == "is space":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(is space)"]=self.dataset[selected_columns].str.isspace()
            col2.dataframe(data)
        elif option == "is title":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(is title)"]=self.dataset[selected_columns].str.istitle()
            col2.dataframe(data)    
        #"left split',"right split","remove preffix","remove suffix"
        elif option=="split":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          delimeter=col2.text_input("Specify the delimeter",',')
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(split)"]=self.dataset[selected_columns].str.split(delimeter)
            col2.dataframe(data)    
        elif option=="left split":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          delimeter=col2.text_input("Specify the delimeter",',')
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(lsplit)"]=self.dataset[selected_columns].str.lsplit(delimeter)
            col2.dataframe(data)   
        elif option=="right split":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          delimeter=col2.text_input("Specify the delimeter",',')
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(rsplit)"]=self.dataset[selected_columns].str.rsplit(delimeter)
            col2.dataframe(data)
        elif option=="remove preffix":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          delimeter=col2.text_input("Specify the prefix to remove")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(remove preffix)"]=self.dataset[selected_columns].str.removeprefix(delimeter)
            col2.dataframe(data)
        elif option=="remove suffix":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          delimeter=col2.text_input("Specify the prefix to remove")
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(remove preffix)"]=self.dataset[selected_columns].str.removesuffix(delimeter)
            col2.dataframe(data)
        elif option ==  "trim white spaces on both sides of text":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(strip)"]=self.dataset[selected_columns].str.strip()
            col2.dataframe(data)
        elif option ==  "trim white spaces on left side of the etxt":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(lstrip)"]=self.dataset[selected_columns].str.lstrip()
            col2.dataframe(data)
        elif option ==  "trim white spaces on the right side of the text":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(rstrip)"]=self.dataset[selected_columns].str.rstrip()
            col2.dataframe(data)
        elif option ==  "split columns based on left side":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          delemeter=col2.text_input("select the delimeter",',')
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(lpartition)[0]"]=self.dataset[selected_columns].str.partition(delimeter)[0]
            data[f"{selected_columns}(lpartition)[2]"]=self.dataset[selected_columns].str.partition(delimeter)[2]
            col2.dataframe(data)
        elif option ==  "split columns based on right side":
          selected_columns=col2.selectbox("Select Columns",self.dataset.columns.tolist())
          delemeter=col2.text_input("select the delimeter",',')
          if col2.button("Apply",use_container_width=True):
            data=self.dataset.copy(deep=True)
            data[f"{selected_columns}(rpartition)[0]"]=self.dataset[selected_columns].str.rpartition(delimeter)[0]
            data[f"{selected_columns}(rpartition)[2]"]=self.dataset[selected_columns].str.rpartition(delimeter)[2]
            col2.dataframe(data)
      except Exception as e:
        col2.error(e)
    with tab2:
      st.link_button("Click Here To Navigate To Another Website Where You can Perform Most Advanced String Functions",
                         "https://natural-language-proceappr-rexublsuqse8pxgr2of6f8.streamlit.app/")
      
  
