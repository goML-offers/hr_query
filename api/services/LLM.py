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
load_dotenv()

def store(path):
    loader = PyPDFLoader(path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    OPEN_API_KEY = os.getenv('OPEN_API_KEY')
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')

    embeddings = OpenAIEmbeddings(openai_api_key=OPEN_API_KEY)

    pinecone.init(
        api_key=PINECONE_API_KEY,  # find at app.pinecone.io
        environment=PINECONE_API_ENV  # next to api key in console
    )
    index_name = "websc" # put in the name of your pinecone index here
    
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

    return docsearch

def chat(query):
    OPEN_API_KEY = os.getenv('OPEN_API_KEY')
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')
    embeddings = OpenAIEmbeddings(openai_api_key=OPEN_API_KEY)
    pinecone.init(
        api_key=PINECONE_API_KEY,  # find at app.pinecone.io
        environment=PINECONE_API_ENV  # next to api key in console
    )
    index_name = "websc" # put in the name of your pinecone index here
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    llm = OpenAI(temperature=0, openai_api_key=OPEN_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")
    
    # while True:
    # query = input("prompt:") 
    docs = docsearch.similarity_search(query)
    result = chain.run(input_documents=docs, question=query+"first give one line of explanation and followed by answer in points")
    print(result)
    # conversation = "You:Your are a chatbot assistant, you need to help me with elaborating the text?\nGPT-3.5:"
    # user_input = "Brief this context:"+result
    # return openai.Completion.create(engine="text-davinci-002", prompt=conversation, max_tokens=150).choices[0].text.strip()

# Example usage:
    
    return result



#store("C:/Users/krv66/Downloads/output 2.pdf")
# store("D:\LLM webscrap\api\services\data_scrap\output.pdf")
# chat()