from langchain.text_splitter import RecursiveCharacterTextSplitter
from google.cloud import storage

PROJECT_ID = "project-id"
BUCKET_NAME = "bucket-name"
FILE_PATH = "sample.txt"
GCS_PREFIX = "chunks/"
REGION = "us-central1"

def upload_to_gcs(blob_name, content):
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"{GCS_PREFIX}{blob_name}")
    blob.upload_from_string(content)

def chunk_and_upload():
    with open(FILE_PATH, 'r') as file:
        raw_text = file.read()

    splitter = RecursiveCharacterTextSplitter(chunk_size=210, chunk_overlap=70)
    chunks = splitter.split_text(raw_text)

    for i, chunk in enumerate(chunks):
        upload_to_gcs(f"chunk_{i}.txt", chunk)
        print(f"Uploaded chunk_{i}.txt")
