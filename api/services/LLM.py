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
    try:
        # print(path)
        
        loader = PyPDFLoader(path)
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        texts = text_splitter.split_documents(data)
        OPEN_API_KEY = os.getenv('OPEN_API_KEY')
        PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
        PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')
        print(PINECONE_API_KEY)
        embeddings = OpenAIEmbeddings(openai_api_key=OPEN_API_KEY)
        print("embedding started")
        print(PINECONE_API_KEY,PINECONE_API_ENV,OPEN_API_KEY)
        pinecone.init(
            api_key=PINECONE_API_KEY,  # find at app.pinecone.io
            environment=PINECONE_API_ENV  # next to api key in console
        )
        index_name = "websc" # put in the name of your pinecone index here
        
        docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

        return docsearch
    except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail=str(e))
            return False 

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
    # print(result)
    # conversation = "You:Your are a chatbot assistant, you need to help me with elaborating the text?\nGPT-3.5:"
    # user_input = "Brief this context:"+result
    # return openai.Completion.create(engine="text-davinci-002", prompt=conversation, max_tokens=150).choices[0].text.strip()

# Example usage:
    
    return result



#store("C:/Users/krv66/Downloads/output 2.pdf")
# store("D:\LLM webscrap\api\services\data_scrap\output.pdf")
# chat()
##################################################################################################################################
# import fitz  # PyMuPDF

# def divide_pdf_content_by_character_count(pdf_file_path, max_chars_per_string=30000):
#     # Initialize the list to store divided content
#     divided_content = []

#     # Open the PDF file
#     pdf_document = fitz.open(pdf_file_path)

#     # Iterate through each page and extract text
#     for page_num in range(pdf_document.page_count):
#         page = pdf_document.load_page(page_num)
#         text = page.get_text()

#         # Split the text into chunks of specified character count
#         chunks = [text[i:i+max_chars_per_string] for i in range(0, len(text), max_chars_per_string)]

#         # Add the chunks to the divided content list
#         divided_content.extend(chunks)

#     # Close the PDF document
#     pdf_document.close()

#     return divided_content

# # Example usage
# pdf_file_path = 'output.pdf'  # Replace with the actual PDF file path
# divided_content = divide_pdf_content_by_character_count(pdf_file_path)

# # Print the divided content
# for i, chunk in enumerate(divided_content, start=1):
#     print(f'Chunk {i}:\n{chunk}\n')