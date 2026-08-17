from dotenv import load_dotenv
import os

from src.helper import load_pdf,filter_content,make_chunk,download_embeddings
    

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore


# Load environment variables
load_dotenv()


# Get API keys
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


# Set environment variables
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


# Load PDF files
extracted_data = load_pdf(data="data/")


# Filter documents
final_content = filter_content(extracted_data)


# Split documents into chunks
content_chunk = make_chunk(final_content)


# Load embedding model
emb_model = download_embeddings()


# Initialize Pinecone
pinecone_client = Pinecone(
    api_key=PINECONE_API_KEY
)


# Pinecone index name
index_name = "medical-chatbot"


# Create index if it doesn't exist
if not pinecone_client.has_index(index_name):
    pinecone_client.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )


# Connect to the index
index = pinecone_client.Index(index_name)


# Store documents and embeddings in Pinecone
docsearch = PineconeVectorStore.from_documents(
    documents=content_chunk,
    embedding=emb_model,
    index_name=index_name
)