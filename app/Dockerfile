FROM python:3.11

WORKDIR /app
COPY requirements.txt .

RUN pip install  -r requirements.txt
#RUN  alembic revision --autogenerate -m "goml-services" 
#RUN  alembic upgrade head
RUN pip install uvicorn


#RUN pip install boto3
COPY awscli-1.29.21-py3-none-any.whl .
COPY boto3-1.28.21-py3-none-any.whl .
COPY botocore-1.31.21-py3-none-any.whl .


RUN pip install --no-build-isolation --force-reinstall awscli-*-py3-none-any.whl boto3-*-py3-none-any.whl botocore-*-py3-none-any.whl
RUN pip install pandas==1.1.5
# RUN pip install dotenv
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

#uvicorn main:app --host 0.0.0.0 --port 8001