from flask import Flask, render_template, jsonify, request
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)


load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Load embedding model
emb_model = download_embeddings()

# Pinecone index name
index_name = "medical-chatbot"

#Loading existing index
docsearch_exist=PineconeVectorStore.from_existing_index(
  index_name=index_name,
  embedding=emb_model
)

retriever=docsearch_exist.as_retriever(search_type="similarity",search_kwargs={"k":3})

#Model
chatModel = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

#Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

#RAG chain
Q_A_Chain=create_stuff_documents_chain(chatModel,prompt)
rag_chain=create_retrieval_chain(retriever,Q_A_Chain)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get",methods=["GET","POST"])
def chat():
    msg=request.form["msg"]
    response=rag_chain.invoke({"input":msg})
    print("Response: ",response["answer"])
    return str(response["answer"])



if __name__ == "__main__":
    app.run(debug=True)

