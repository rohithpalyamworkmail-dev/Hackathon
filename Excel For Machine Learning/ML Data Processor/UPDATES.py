import streamlit as st
import pandas as pd
import ast
class Updates:
  def __init__(self,df):
    self.dataset=df
  def display(self):
    tab1,tab2=st.tabs(["Perform Operations Here","Documentation"])
    with tab1:
      col1,col2=st.columns([1,2],border=True)
      selected_option=col1.radio("Select option",["Edit Manually","Milti Edit Using Condition","Replace Values"])
      if selected_option=="Edit Manually":
        self.edit_manually(col2)
      elif selected_option=="Single Value Edit":
        self.single_value_edit(col2)
      elif selected_option=="Multi Edit":
        self.multi_edit(col2)
      elif selected_option=="Milti Edit Using Condition":
        self.multi_edit_condition(col2)
      elif selected_option=="Replace Values":
        self.replace_values(col2)
  def edit_manually(self,col2):
    edited_data=col2.data_editor(self.dataset,num_rows="dynamic",hide_index=False)
    if col2.button("Conform These Changes",use_container_width=True,type='primary'):
      st.session_state['allData']["Stage - Updates - Edited Datframe - Manually"]=edited_data
  def multi_edit_condition(self, col2):
      with col2.expander("Check column names and row names"):
          col2.write(self.dataset.axes)
  
      try:
          copied_dataframe = self.dataset.copy(deep=True)
          query = col2.text_area("Write Your Query")
  
          if col2.checkbox("Find Information") and query:
              # Apply query to extract relevant rows
              filtered_dataframe = copied_dataframe.query(query)
  
              # Display a data editor to allow modifications
              edited_dataframe = col2.data_editor(filtered_dataframe)
  
              # Update the original DataFrame with the edited values
              copied_dataframe.loc[edited_dataframe.index, edited_dataframe.columns] = edited_dataframe
  
              # Store the updated DataFrame in session state
              st.session_state['allData']["Stage - Updates - Edited DataFrame - Based On Query  - Parent"] = copied_dataframe
              st.session_state['allData']["Stage - Updates - Edited DataFrame - Based On Query"] = edited_dataframe
  
              col2.success("Data updated successfully!")
  
      except Exception as e:
          col2.error(f"Error: {e}")
  def replace_values(self,col2):
    mapper={}
    copied_data=self.dataset.copy(deep=True)
    selected_columns=col2.selectbox("Select the columns",self.dataset.columns.tolist())
    if selected_columns:
        old_values=col2.multiselect("Select the unique values to modify",self.dataset[selected_columns].unique().tolist())
        new_values=col2.text_area(f"Select the new values ',' separated {selected_columns}")
        if col2.button(f"Modify it",use_container_width=True,type='primary'):
          new_values=new_values.split(',')
          if len(old_values)==len(new_values):
            mapper[selected_columns]={old_values[i]:new_values[i] for i in range(len(old_values))}
            copied_data=copied_data.replace(mapper)
            st.session_state['allData'][f'Stage - Upadtes - Replace - {mapper}']=copied_data
            col2.dataframe(copied_data)
          else:
            col2.error("old values length must be match with new values")
          col2.divider()
          

        
