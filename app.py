# -*- coding: utf-8 -*-
"""
Created on Mon May 20 01:30:17 2024

@author: ACER
"""

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextSendMessage, TextMessage, FollowEvent
from linebot.exceptions import InvalidSignatureError

from langchain.vectorstores import Chroma

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain import PromptTemplate
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA

import torch

import os
#set this if want to use GPU
os.environ['CUDA_VISIBLE_DEVICES'] = "GPU-c4cf6995-a8c6-b26b-966c-53edffcd1111"

#Directory for model related file
os.environ['HF_HOME'] = 'D:/Huggingface_cache'
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-large", cache_folder='D:/Huggingface_cache', device = 'cuda')


app = Flask(__name__)
CHANNEL_SECRET = ''
CHANNEL_ACCESS_TOKEN = ''
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
llm = Ollama(model="nxphi47/seallm-7b-v2:q4_0", 
             callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),)

# Define the prompt template once
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

#Load data
vectorstore = Chroma(collection_name='v_db',persist_directory='./vector_db',embedding_function=HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large", cache_folder='D:/Huggingface_cache/'))

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"
@app.route("/update_v_db", methods=["POST"])
def update_v_db():
    global vectorstore
    try:
        vectorstore = Chroma(collection_name='v_db',persist_directory='./vector_db',embedding_function=HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large", cache_folder='D:/Huggingface_cache/'))
        return "Updating data: Success!"
    except Exception as e:
        return "Opps! Something went wrong/n",e
    
#ส่งคำแนะนำตัวเมื่อมีการแอดเพื่อใหม่
@handler.add(FollowEvent)
def handle_add_friend(event):
    user_id = event.source.user_id
    line_bot_api.push_message(user_id, TextSendMessage("สวัสดีครับ/ค่ะ ทางเราเป็นผู้ช่วยอัจฉริยะ เพื่อตอบคำถามของคุณเกี่ยวกับด้านทรัพยากรณ์บุคคลครับฝค่ะ"))

#รับข้อความจากผู้ใช้เพื่อตอบคำถาม
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    text = event.message.text
    torch.cuda.empty_cache()
    template = """Answer the question based ONLY on the following context:
{context}

Question: {question}
"""
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )
    res = qa_chain({'query':text})
    line_bot_api.push_message(user_id, TextSendMessage(res['result']))
    
if __name__ == "__main__":
    app.run()
                              