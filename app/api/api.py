from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain import HuggingFacePipeline, PromptTemplate
from langchain.chains import RetrievalQA
from huggingface_hub import notebook_login
import torch
import pinecone
import boto3
import fitz
from io import BytesIO
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline
import os
import shutil
import sys



def hr_llm():
  def download_pdf_files_from_folder(local_download_path):
    AWS_ACCESS_KEY_ID = os.environ.get('S3_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_KEY')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    S3_FOLDER_NAME = os.environ.get('COMPANY_NAME')

    # Create an S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # Get the list of objects in the folder.
    objects = s3.list_objects(Bucket=S3_BUCKET_NAME, Prefix=S3_FOLDER_NAME)['Contents']

    # Filter the objects to only include PDF files.
    pdf_objects = [obj for obj in objects if obj['Key'].endswith('.pdf')]

    # Download the PDF files to the local path.
    for obj in pdf_objects:
      s3.download_file(S3_BUCKET_NAME, obj['Key'], os.path.join(local_download_path, obj['Key'][len(S3_FOLDER_NAME):]))


  if not os.path.exists(r'temp'):
      os.makedirs(r'temp')
  local_download_path = r'temp'

  # Download the PDF files in the folder.
  download_pdf_files_from_folder(local_download_path)

  loader = PyPDFDirectoryLoader("temp")
  data = loader.load()
  print(data)
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
  docs = text_splitter.split_documents(data)
  

  PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', '1f554ddc-6243-47fd-9bc7-70cb75370517')
  PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'gcp-starter')

  pinecone.init(
      api_key=PINECONE_API_KEY,  # find at app.pinecone.io
      environment=PINECONE_API_ENV  # next to api key in console
  )
  index_name = "hrllm" # put in the name of your pinecone index here

  

  

  model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf",
                                             device_map='auto',
                                             torch_dtype=torch.float16,
                                             use_auth_token="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",
                                             load_in_8bit=True
                                             )
  tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token="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")


  pipe = pipeline("text-generation",
                  model=model,
                  tokenizer= tokenizer,
                  torch_dtype=torch.bfloat16,
                  device_map="auto",
                  max_new_tokens = 512,
                  do_sample=True,
                  top_k=30,
                  num_return_sequences=1,
                  eos_token_id=tokenizer.eos_token_id
                  )

  embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
  query_result = embeddings.embed_query("Hello World")
  docsearch=Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=index_name)
  llm=HuggingFacePipeline(pipeline=pipe, model_kwargs={'temperature':0.1})
  

  SYSTEM_PROMPT = """Use the following pieces of context to answer the question briefly at the end.
  If you don't know the answer, just say that you don't know, don't try to make up an answer."""

  B_INST, E_INST = "[INST]", "[/INST]"
  B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

  SYSTEM_PROMPT = B_SYS + SYSTEM_PROMPT + E_SYS

  instruction = """
  {context}

  Question: {question}
  """

  template = B_INST + SYSTEM_PROMPT + instruction + E_INST

  prompt = PromptTemplate(template=template, input_variables=["context", "question"])

  qa_chain = RetrievalQA.from_chain_type(
      llm=llm,
      chain_type="stuff",
      retriever=docsearch.as_retriever(search_kwargs={"k": 2}),
      return_source_documents=True,
      chain_type_kwargs={"prompt": prompt}
  )

  return qa_chain
