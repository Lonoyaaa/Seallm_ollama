# -*- coding: utf-8 -*-
"""
Update data in vector database by running this script
"""

from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import UnstructuredCSVLoader

import torch
import chromadb
persistent_client = chromadb.PersistentClient(path='./vector_db')


import os
os.environ['CUDA_VISIBLE_DEVICES'] = "GPU-c4cf6995-11111111111111111111"
os.environ['HF_HOME'] = 'D:/Huggingface_cache'
torch.cuda.empty_cache()
DATA_PATH = './dataset'
text_splitter = RecursiveCharacterTextSplitter(['\n\n', '\n'], chunk_size=1024, chunk_overlap=200)
documents =[]
for filename in os.listdir(DATA_PATH):
        filepath = os.path.join(DATA_PATH, filename)
        if os.path.isfile(filepath):
            if filepath.endswith('.docx'):
                loader = UnstructuredWordDocumentLoader(filepath)
            if filepath.endswith('.csv'):
                loader = UnstructuredCSVLoader(filepath, {
                    'delimiter': ',',
                    'quotechar': '"'
                    })
            data = loader.load()
            data = text_splitter.split_documents(data)
            documents.extend(data)
collections = persistent_client.list_collections()
for collection in collections:
    print(collection)
if any(collection.name == 'v_db' for collection in collections):
    Chroma(collection_name='v_db').delete_collection()
    print('delete_old_data')
db = Chroma.from_documents(documents = documents, embedding=HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large"), collection_name='v_db',persist_directory='./vector_db')
db.persist()
