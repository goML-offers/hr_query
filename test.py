from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
import pinecone
import openai
import tiktoken
import sys
def process_and_upload_embeddings(path):
    print("Processing and uploading embeddings...")
    loader = PyPDFLoader(path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    OPEN_API_KEY = "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"
    PINECONE_API_KEY = "51f89ba4-0704-4d6f-b329-19d5c3f8e955"
    PINECONE_API_ENV = "gcp-starter"

    embeddings = OpenAIEmbeddings(openai_api_key=OPEN_API_KEY)
    print("Embedding started")
    print(PINECONE_API_KEY, PINECONE_API_ENV, OPEN_API_KEY)

    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_API_ENV
    )
    index_name = "websc"  # put in the name of your Pinecone index here

    # Check if the index exists, and delete if it does
    if index_name in pinecone.list_indexes():
        print("Deleting existing index...")
        pinecone.delete_index(index_name)

    # Create a new index
    print("Creating a new index...")
    pinecone.create_index(index_name,dimension=1536)

    # Embed and upload the texts to the new index
    print("Embedding and uploading documents...")
    embeddings_data = embeddings.embed([t.page_content for t in texts])
    pinecone.embed(index_name, embeddings_data, ids=range(len(texts)))

    print("Processing and uploading completed.")




process_and_upload_embeddings("C:/Users/Akash/Downloads/output 2.pdf")