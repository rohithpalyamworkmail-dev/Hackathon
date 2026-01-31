import streamlit as st
import pandas as pd
from pymongo import MongoClient
from PIL import Image
import io
import base64
import os

class Collaborate:
    def __init__(self, df):
        try:
            self.client = MongoClient(os.environ.get("mongoURI"))
        except Exception as e:
            st.error(f"Database connection error: {e}")
        self.data = df
        
    def display(self):
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
            ["Add Data", "View Data", "Modify Data", "Delete Data", "Add Media", "View Complaints"]
        )
        
        with tab1:
            self._add_data_tab()
                    
        with tab2:
            self._view_data_tab()
            
        with tab3:
            self._modify_data_tab()
            
        with tab4:
            self._delete_data_tab()
            
        with tab5:
            self._add_media_tab()
            
        with tab6:
            self._view_complaints_tab()
    
    def _add_data_tab(self):
        col1, col2 = st.columns([1, 2], border=True)
        
        with col1:
            option = st.radio("Select Operation", 
                             ["Connect To Data Base", "Add Collections", "Add Data"],
                             key="add_data_radio")
            
        with col2:
            if option == "Connect To Data Base":
                self._connect_database_ui()
            elif option == "Add Collections":
                self._add_collections_ui()
            elif option == "Add Data":
                self._add_data_ui()
    
    def _view_data_tab(self):
        col1, col2 = st.columns([1, 2], border=True)
        
        with col1:
            if 'database' not in st.session_state:
                st.warning("Please connect to a database first")
                return
                
            collections = self._get_collections()
            if not collections:
                return
                
            selected_collection = st.selectbox("Select Collection", collections, key="view_collection_select")
            view_option = st.radio("View Option", ["View Selected Output", "View All Outputs"],
                                 key="view_option_radio")
        
        with col2:
            if view_option == "View Selected Output":
                self._view_selected_output(selected_collection)
            else:
                self._view_all_outputs(selected_collection)
    
    def _modify_data_tab(self):
        col1, col2 = st.columns([1, 2], border=True)
        
        with col1:
            if 'database' not in st.session_state:
                st.warning("Please connect to a database first")
                return
                
            collections = self._get_collections()
            if not collections:
                return
                
            selected_collection = st.radio("Select Collection", collections, key="modify_collection_radio")
        
        with col2:
            if selected_collection:
                self._modify_collection_data(selected_collection)
    
    def _delete_data_tab(self):
        col1, col2 = st.columns([1, 2], border=True)
        
        with col1:
            if 'database' not in st.session_state:
                st.warning("Please connect to a database first")
                return
                
            delete_option = st.radio("Delete Option", 
                                   ["Delete Collection", "Delete Documents"],
                                   key="delete_option_radio")
        
        with col2:
            if delete_option == "Delete Collection":
                self._delete_collection_ui()
            elif delete_option == "Delete Documents":
                self._delete_documents_ui()
    
    def _add_media_tab(self):
        col1, col2 = st.columns([1, 2], border=True)
        
        with col1:
            if 'database' not in st.session_state:
                st.warning("Please connect to a database first")
                return
                
            collections = self._get_collections()
            if not collections:
                return
                
            selected_collection = st.selectbox("Select Collection", collections, key="media_collection_select")
        
        with col2:
            if selected_collection:
                self._add_media_ui(selected_collection)
    
    def _view_complaints_tab(self):
        col1, col2 = st.columns([1, 2], border=True)
        
        with col1:
            if 'database' not in st.session_state:
                st.warning("Please connect to a database first")
                return
                
            try:
                complaints_col = st.session_state['database']['complaints']
                complaints = list(complaints_col.find({}, {'id_number': 1}))
                
                if not complaints:
                    st.warning("No complaints found")
                    return
                    
                complaint_options = [comp['id_number'] for comp in complaints]
                selected_complaint = st.radio("Select Complaint", complaint_options,
                                             key="complaints_radio")
            
            except Exception as e:
                st.error(f"Error accessing complaints: {e}")
                return
        
        with col2:
            if 'selected_complaint' in locals():
                self._display_complaint_details(selected_complaint)
    
    def _display_complaint_details(self, complaint_id):
        try:
            complaints_col = st.session_state['database']['complaints']
            complaint = complaints_col.find_one({'id_number': complaint_id})
            
            if not complaint:
                st.error("Complaint not found")
                return
            
            st.write(f"**Name:** {complaint.get('name', 'N/A')}")
            st.write(f"**Collection:** {complaint.get('collection', 'N/A')}")
            st.write(f"**Complaint On:** {complaint.get('complaint_on', 'N/A')}")
            st.write(f"**Complaint:** {complaint.get('complaint', 'N/A')}")
            
            # Display the actual data being complained about
            collection_name = complaint.get('collection')
            complaint_on = complaint.get('complaint_on')
            
            if collection_name and complaint_on:
                try:
                    target_col = st.session_state['database'][collection_name]
                    target_doc = target_col.find_one({'key': complaint_on})
                    
                    if target_doc:
                        st.subheader("Complained Data", divider='blue')
                        
                        if 'data' in target_doc:
                            st.dataframe(pd.DataFrame(target_doc['data']))
                        elif 'image' in target_doc:
                            img_bytes = base64.b64decode(target_doc['image'])
                            st.image(img_bytes, caption=target_doc.get('description', ''), 
                                   use_column_width=True)
                        else:
                            st.write("No displayable data found in the document")
                    else:
                        st.warning("The complained document was not found")
                except Exception as e:
                    st.error(f"Error fetching complained data: {e}")
            
        except Exception as e:
            st.error(f"Error displaying complaint details: {e}")
    
    def _connect_database_ui(self):
        st.subheader("Connect to Database")
        db_name = st.text_input("Database Name", key="db_name_input")
        password = st.text_input("Password", type="password", key="db_password_input")
        
        if st.button("Connect", key="connect_db_button"):
            if not db_name:
                st.error("Please enter a database name")
                return
                
            try:
                db = self.client[db_name]
                authenticator = db['Authenticator']
                
                if db_name in self.client.list_database_names():
                    auth_doc = authenticator.find_one()
                    if auth_doc and auth_doc.get('password') == password:
                        st.session_state['database'] = db
                        st.success("Successfully connected to existing database")
                    else:
                        st.error("Password does not match. Connection failed.")
                else:
                    authenticator.insert_one({'password': password})
                    st.session_state['database'] = db
                    st.success("New database created successfully")
                    
            except Exception as e:
                st.error(f"Error connecting to database: {e}")
    
    def _add_collections_ui(self):
        st.subheader("Add Collections")
        
        if 'database' not in st.session_state:
            st.warning("Please connect to a database first")
            return
            
        collection_name = st.text_input("Collection Name", key="new_collection_name")
        
        if st.button("Add Collection", key="add_collection_button"):
            if not collection_name:
                st.error("Please enter a collection name")
                return
                
            try:
                if collection_name in st.session_state['database'].list_collection_names():
                    st.warning(f"Collection '{collection_name}' already exists")
                else:
                    st.session_state['database'].create_collection(collection_name)
                    st.success(f"Collection '{collection_name}' created successfully")
            except Exception as e:
                st.error(f"Error creating collection: {e}")
    
    def _add_data_ui(self):
        st.subheader("Add Data to Collection")
        
        if 'database' not in st.session_state:
            st.warning("Please connect to a database first")
            return
            
        if 'allData' not in st.session_state:
            st.warning("No data available in session state")
            return
            
        collections = self._get_collections()
        if not collections:
            return
            
        selected_collection = st.selectbox("Select Collection", collections, key="add_data_collection_select")
        data_options = list(st.session_state['allData'].keys())
        selected_data = st.selectbox("Select Data", data_options, key="add_data_data_select")
        
        if selected_data:
            st.dataframe(st.session_state['allData'][selected_data])
            
        key = st.text_input("Enter a key for this data", key="add_data_key_input")
        description = st.text_area("Enter description", key="add_data_description_area")
        
        if st.button("Add Data", key="add_data_submit_button"):
            if not key or not selected_data:
                st.error("Please provide both a key and select data")
                return
                
            try:
                collection = st.session_state['database'][selected_collection]
                
                if collection.find_one({'key': key}):
                    st.warning(f"Key '{key}' already exists in this collection")
                    return
                    
                doc = {
                    'key': key,
                    'description': description,
                    'data': st.session_state['allData'][selected_data].to_dict('records')
                }
                
                collection.insert_one(doc)
                st.success("Data added successfully to collection")
            except Exception as e:
                st.error(f"Error adding data: {e}")
    
    def _add_media_ui(self, collection_name):
        st.subheader("Add Media to Collection")
        
        uploaded_file = st.file_uploader("Choose an image file", 
                                       type=['png', 'jpg', 'jpeg'],
                                       key=f"media_uploader_{collection_name}")
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_container_width=True)
            
            key = st.text_input("Enter a key for this image", key=f"media_key_{collection_name}")
            description = st.text_area("Enter description", key=f"media_desc_{collection_name}")
            
            if st.button("Add Media", key=f"add_media_button_{collection_name}"):
                if not key:
                    st.error("Please provide a key")
                    return
                    
                try:
                    collection = st.session_state['database'][collection_name]
                    
                    if collection.find_one({'key': key}):
                        st.warning(f"Key '{key}' already exists in this collection")
                        return
                        
                    # Convert image to binary
                    buffered = io.BytesIO()
                    image.save(buffered, format=image.format)
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    doc = {
                        'key': key,
                        'description': description,
                        'image': img_str,
                        'image_format': image.format.lower()
                    }
                    
                    collection.insert_one(doc)
                    st.success("Media added successfully to collection")
                except Exception as e:
                    st.error(f"Error adding media: {e}")
    
    def _view_selected_output(self, collection_name):
        st.subheader("View Selected Output")
        
        collection = st.session_state['database'][collection_name]
        documents = list(collection.find({}, {'key': 1}))
        
        if not documents:
            st.warning("No documents found in this collection")
            return
            
        key_options = [doc['key'] for doc in documents]
        selected_key = st.selectbox("Select Key", key_options, key=f"view_key_select_{collection_name}")
        
        if selected_key:
            doc = collection.find_one({'key': selected_key})
            
            st.subheader(selected_key, divider='blue')
            
            if 'data' in doc:
                st.dataframe(pd.DataFrame(doc['data']))
                st.write("**Description:**", doc.get('description', 'No description available'))
            elif 'image' in doc:
                img_bytes = base64.b64decode(doc['image'])
                st.image(img_bytes, caption=doc.get('description', ''), use_container_width=True)
                st.write("**Format:**", doc.get('image_format', 'Unknown'))
    
    def _view_all_outputs(self, collection_name):
        st.subheader("View All Outputs")
        
        collection = st.session_state['database'][collection_name]
        documents = list(collection.find())
        
        if not documents:
            st.warning("No documents found in this collection")
            return
            
        for doc in documents:
            st.subheader(doc['key'], divider='blue')
            
            if 'data' in doc:
                st.dataframe(pd.DataFrame(doc['data']))
                st.write("**Description:**", doc.get('description', 'No description available'))
            elif 'image' in doc:
                img_bytes = base64.b64decode(doc['image'])
                st.image(img_bytes, caption=doc.get('description', ''), use_container_width=True)
                st.write("**Format:**", doc.get('image_format', 'Unknown'))
            
            st.divider()
    
    def _modify_collection_data(self, collection_name):
        st.subheader(f"Modify Data in {collection_name}")
        
        collection = st.session_state['database'][collection_name]
        documents = list(collection.find({}, {'key': 1}))
        
        if not documents:
            st.warning("No documents found in this collection")
            return
            
        key_options = [doc['key'] for doc in documents]
        selected_key = st.selectbox("Select Document to Modify", key_options, 
                                  key=f"modify_key_select_{collection_name}")
        
        if selected_key:
            doc = collection.find_one({'key': selected_key})
            
            st.subheader("Current Values", divider='blue')
            st.text_input("Current Key", value=doc['key'], disabled=True,
                         key=f"current_key_{selected_key}")
            
            if 'data' in doc:
                st.text_area("Current Description", value=doc.get('description', ''), disabled=True,
                            key=f"current_desc_{selected_key}")
                st.dataframe(pd.DataFrame(doc['data']), use_container_width=True)
            elif 'image' in doc:
                img_bytes = base64.b64decode(doc['image'])
                st.image(img_bytes, caption=doc.get('description', ''), use_column_width=True)
                st.write("**Format:**", doc.get('image_format', 'Unknown'))
            
            st.subheader("New Values", divider='blue')
            new_key = st.text_input("New Key", value=doc['key'],
                                   key=f"new_key_{selected_key}")
            new_description = st.text_area("New Description", value=doc.get('description', ''),
                                         key=f"new_desc_{selected_key}")
            
            if 'data' in doc and 'allData' in st.session_state:
                data_options = list(st.session_state['allData'].keys())
                selected_data = st.selectbox("Select New Data (optional)", [""] + data_options,
                                           key=f"new_data_{selected_key}")
            else:
                selected_data = ""
            
            if st.button("Update Document", key=f"update_button_{selected_key}"):
                update_data = {}
                
                if new_key != doc['key']:
                    if collection.find_one({'key': new_key}):
                        st.error(f"Key '{new_key}' already exists in this collection")
                        return
                    update_data['key'] = new_key
                
                if new_description != doc.get('description', ''):
                    update_data['description'] = new_description
                
                if selected_data and selected_data != "" and 'data' in doc:
                    update_data['data'] = st.session_state['allData'][selected_data].to_dict('records')
                
                if update_data:
                    collection.update_one({'key': selected_key}, {'$set': update_data})
                    st.success("Document updated successfully")
                else:
                    st.warning("No changes detected")
    
    def _delete_collection_ui(self):
        st.subheader("Delete Collection")
        
        collections = self._get_collections()
        if not collections:
            return
            
        selected_collections = st.multiselect("Select Collections to Delete", collections,
                                            key="delete_collections_multiselect")
        
        if st.button("Delete Selected Collections", type="primary", key="delete_collections_button"):
            for col_name in selected_collections:
                try:
                    st.session_state['database'].drop_collection(col_name)
                    st.success(f"Collection '{col_name}' deleted successfully")
                except Exception as e:
                    st.error(f"Error deleting collection '{col_name}': {e}")
    
    def _delete_documents_ui(self):
        st.subheader("Delete Documents")
        
        collections = self._get_collections()
        if not collections:
            return
            
        selected_collection = st.selectbox("Select Collection", collections,
                                         key="delete_docs_collection_select")
        
        if selected_collection:
            collection = st.session_state['database'][selected_collection]
            documents = list(collection.find({}, {'key': 1}))
            
            if not documents:
                st.warning("No documents found in this collection")
                return
                
            document_keys = [doc['key'] for doc in documents]
            selected_docs = st.multiselect("Select Documents to Delete", document_keys,
                                         key="delete_docs_multiselect")
            
            if st.button("Delete Selected Documents", type="primary", key="delete_docs_button"):
                for doc_key in selected_docs:
                    try:
                        collection.delete_one({'key': doc_key})
                        st.success(f"Document '{doc_key}' deleted successfully")
                    except Exception as e:
                        st.error(f"Error deleting document '{doc_key}': {e}")
    
    def _get_collections(self):
        if 'database' not in st.session_state:
            return []
            
        collections = [col for col in st.session_state['database'].list_collection_names() 
                      if col != 'Authenticator']
        
        if not collections:
            st.warning("No collections available (except Authenticator)")
            
        return collections
