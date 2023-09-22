# goML - LLM marketplace ( hr_llm)

### This hr_llm main goal is to generates a user-input query's answer from HR PDF documents based on the organisation HR pdf docments.

 

### model input:

Upload a organisation HR pdf documents.

 

### model output:

The model generates a user-input query's answer from HR PDF documents.

 

### Execution

> run requirements.txt

> run app.py (run uvicorn api.main:app --reload)

> open this url on a browser http://127.0.0.1:8000/docs

> provide the necessary inputs, here we upload the image in s3 bucket.

> Read pdf docments from s3 location and model generates a user-input query's answer from HR PDF documents.