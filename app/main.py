from fastapi import FastAPI, File, UploadFile, Query
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv
import boto3
from botocore.exceptions import NoCredentialsError
from typing import List
import uvicorn
import shutil
import sys
from api.api import hr_llm


# Load environment variables from .env file
load_dotenv(find_dotenv())

AWS_ACCESS_KEY_ID = os.environ.get("S3_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_KEY")
company_name = os.environ.get("COMPANY_NAME")

app = FastAPI()

# Allow all origins (you can tighten this security in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")  # Replace with your actual S3 bucket name

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@app.get("/")
def root():
    return {"message": "Fast API in Python"}

@app.post("/upload/")
async def upload_files(company_name: str = Query(..., description="Company name"), files: List[UploadFile] = File(...)):
    try:
        with open(".env","w") as f:
            f.write(f"""S3_BUCKET_NAME = 'gomloffers'\nS3_ACCESS_KEY = '{AWS_ACCESS_KEY_ID}'\nS3_SECRET_KEY = '{AWS_SECRET_ACCESS_KEY}'""")
            f.write(f"\nCOMPANY_NAME= '{company_name}/'")
        s3_urls = []
        for file in files:
            # Generate a unique key for the S3 object
            s3_key = f"{company_name}/{file.filename}"
            # Upload the file to S3
            s3.upload_fileobj(file.file, S3_BUCKET_NAME, s3_key)
            # Generate the S3 URL
            s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
            s3_urls.append(s3_url)
        return {"message": "Files uploaded successfully", "s3_urls": s3_urls}
    except NoCredentialsError:
        return {"error": "AWS credentials not found."}

# Updated API for processing files and returning results
@app.get("/query/")
def process_files(prompt:str):
    try:
        # List objects in the company's folder
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=f"{company_name}/")
        files = []
        
        qa_chain=hr_llm()
        while True:
            user_input=prompt
            if user_input=='exit':
                print('Exiting')
                shutil.rmtree('/temp')
                sys.exit()
            if user_input=='':
                continue
            result=qa_chain({'query':user_input})
            print(f"Answer:{result['result']}")
            return {"message": "Files fetched and processed successfully", "files": files}
    except NoCredentialsError:
        return {"error": "AWS credentials not found."}

# ...

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)