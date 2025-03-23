import boto3
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get AWS credentials from environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")  # Only needed if required
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Initialize S3 Client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=AWS_REGION
)

# Streamlit UI
st.title("📂 Upload Receipt to S3")

uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "pdf"])
if uploaded_file is not None:
    file_name = uploaded_file.name
    bucket_name = "monthly-expense-receipts"

    try:
        # Upload file to S3
        s3.upload_fileobj(uploaded_file, bucket_name, file_name)
        st.success(f"File '{file_name}' uploaded successfully to S3!")
    except Exception as e:
        st.error(f"Error uploading file: {e}")
