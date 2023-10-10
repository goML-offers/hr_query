import sys
from fastapi import FastAPI, File,  UploadFile
from fastapi import APIRouter, HTTPException, Response
from services.csv_scrap import scrap_main
from services.scrap import scrape_website
from services.LLM import chat,store
import os
from fastapi.responses import JSONResponse
import json
from dotenv import load_dotenv
load_dotenv()


router = APIRouter()
@router.post('/goml/LLM marketplace/Web data chat bot/upload_file', status_code=201)
def data_generator(file: UploadFile):
    try:
        UPLOAD_DIR = "/api/uploads"

        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        # Generate a unique file name to avoid overwriting existing files
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as f:
            f.write(file.file.read())
            f.close()
        
        data_loc = scrap_main(file_path)

        os.remove(file_path)
        # store(data_loc)
        os.remove(data_loc)
        return True
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
            return False 
   
@router.post('/goml/LLM marketplace/Web data chat bot/link_extractor', status_code=201)
async def accuracy_generator(url: str):
    try:
        output_pdf_path = scrape_website(url)
        
        # return output_pdf_path
        # store(output_pdf_path)
        os.remove(output_pdf_path)
        return True
    except Exception as e:
            
            raise HTTPException(status_code=400, detail=str(e))
            return False


@router.post('/goml/LLM marketplace/Web data chat bot/chatbot', status_code=201)
def validating_test(query: str):
    try:
        
        answer = chat(query)
    
        return answer
    except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

