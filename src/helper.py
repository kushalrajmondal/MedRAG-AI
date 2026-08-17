from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from typing import List
from langchain.schema import Document

#Extract text from PDF file
def load_pdf(data):
    loader = DirectoryLoader(
        data,
        glob="*.pdf",#load all pdfs from "data" folder
        loader_cls=PyPDFLoader
    )

    documents = loader.load()
    return documents


#Extracting source and page content
def filter_content(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Document objects
    containing only 'source' in metadata and the original page_content.
    """

    filtered_docs: List[Document] = []

    for doc in docs:
        src = doc.metadata.get("source")

        filtered_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )

    return filtered_docs


# Split the documents into smaller chunks
def make_chunk(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )

    texts_chunk = text_splitter.split_documents(minimal_docs)

    return texts_chunk


#Embedding Model
from langchain.embeddings import HuggingFaceEmbeddings


def download_embeddings():
    """
    Download and return the HuggingFace embeddings model.
    """

    model_name = "sentence-transformers/all-MiniLM-L6-v2"

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name
    )

    return embeddings

