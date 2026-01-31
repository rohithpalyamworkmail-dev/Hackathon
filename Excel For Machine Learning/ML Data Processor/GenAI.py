import streamlit as st
import pandas as pd
from groq import Groq

class GenAI:
    def __init__(self, df):
        self.dataset = df

    def query_groq(self, question, api_key, selected_data_json):
        """Uses Groq API to answer questions about the dataset."""
        client = Groq(api_key=api_key)

        prompt = f"""
        You are an expert data analyst. Given the following dataset (in JSON format):

        {selected_data_json}

        Answer the following user query in a concise and insightful way:
        "{question}"
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Use a supported Groq model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def display(self):
        # Create two tabs
        tab1, tab2 = st.tabs(["Query Data", "Selected Data"])

        with tab1:
            col1, col2 = st.columns([1, 2], border=True)

            with col1:
                st.subheader("Configuration", divider='blue')
                # Step 1: Ask for Groq API Key
                groq_api_key = st.text_input("Enter Your Groq API Key:", type="password")
                if groq_api_key:
                    # Step 2: Select columns
                    selected_columns = st.multiselect(
                        "Select Columns",
                        options=self.dataset.columns,
                        key="selected_columns"
                    )

                    if selected_columns:
                        # Step 3: Select rows
                        row_selection_type = st.radio(
                            "Select Rows",
                            ["Sequence Rows", "Random Rows", "All Rows"],
                            key="row_selection_type"
                        )

                        if row_selection_type == "Sequence Rows":
                            start_index, end_index = st.slider(
                                "Select Row Range",
                                min_value=0,
                                max_value=len(self.dataset) - 1,
                                value=(0, min(10, len(self.dataset) - 1)),
                                step=1
                            )
                            sub_df = self.dataset.iloc[start_index:end_index + 1][selected_columns]
                        elif row_selection_type == "Random Rows":
                            sample_size = st.slider(
                                "Select Number of Random Rows",
                                min_value=1,
                                max_value=len(self.dataset),
                                value=min(10, len(self.dataset)),
                                step=1
                            )
                            sub_df = self.dataset[selected_columns].sample(n=sample_size)
                        else:  # All Rows
                            sub_df = self.dataset[selected_columns]

                        # Display the selected data in Tab 2
                        tab2.subheader("Selected Data", divider='blue')
                        tab2.dataframe(sub_df)

                        # Step 4: Ask for a question
                        question = st.text_area("Enter your question about the selected data:")

                        if question:
                            if st.button("Submit Query"):
                                # Convert the selected data to JSON
                                selected_data_json = sub_df.to_json(orient="records")

                                # Query Groq API
                                response = self.query_groq(question, groq_api_key, selected_data_json)

                                # Display the response in Column 2
                                with col2:
                                    st.subheader("Groq Response", divider='blue')
                                    st.write(response)

            with col2:
                st.subheader("Groq Query Results", divider='blue')

        with tab2:
            if 'sub_df' in locals():
                st.subheader("Selected Data Preview", divider='blue')
                st.dataframe(sub_df)
            else:
                st.info("No data selected yet. Configure in Tab 1.")
