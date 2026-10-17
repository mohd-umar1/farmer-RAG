import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import(
    DirectoryLoader,
    PyPDFLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
from farmer_proj.api.geocoding import get_coordinates

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    raise ValueError("groq api  key not found")

print("loading pdfs")

loader = DirectoryLoader(
    "D:\\farmer_proj_RAG\\farmer-proj\\src\\farmer_proj\\Data",
    glob="*.pdf",
    loader_cls=PyPDFLoader 
)

documents = loader.load()

for doc in documents:
    source = doc.metadata.get("source","")
    filename = os.path.basename(source)
    district = os.path.splitext(filename)[0]
    doc.metadata["district"] = district



splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80
)

chunks = splitter.split_documents(documents)

print(f"{len(chunks)} number of chunks created")


embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

persist_directory = "chroma_db"

if os.path.exists(persist_directory):
    print("loading existing vector database")

    db=Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding
    )
else:
    print("creating vector database")

    db=Chroma.from_documents(
        chunks,
        embedding,
        persist_directory=persist_directory
    )

data = db.get(include=["metadatas"])

print("Number of documents:", len(data["metadatas"]))

for metadata in data["metadatas"][:10]:
    print(metadata)

lang = input("enter your prefered language: ")

state = input("enter your State: ")

city = input("enter your city: ")

coordinates = get_coordinates(state,city)

print(coordinates['lat'],coordinates['lon'])

retriever = db.as_retriever(search_kwargs={"k":8
                                           })

llm =ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.4
)

prompt = ChatPromptTemplate.from_template(
f"""
You are an expert agricultural assistant.

Answer the user's question using the retrieved context as your primary source.

Answer in {lang} language

Instructions:
- district is {city}
- Carefully read all of the retrieved context.
- Use the retrieved context as your PRIMARY source.
- If the answer is present, explain it clearly and naturally.
- Answer the questions based on the context
- Be as helpful as possible
- If the context is incomplete, clearly state which parts came from the documents and which parts are general agricultural knowledge.
- If the information is only partially available, answer with what you know from the context and mention that some details are not available.
- If no info is known explain it with your own knowledge
- Answer in plain text only and dont output any table answer in paragraph format

Retrieved Context:
{{context}}

Question:
{{input}}

"""
)

document_chain = create_stuff_documents_chain(
    llm,
    prompt
)

retreval_chain = create_retrieval_chain(
    retriever,
    document_chain
)

print("\nRAG Ready!")
print("Type exit to quit.\n")

while True:

    question = input("You: ")

    if question == "exit":
        break

    response = retreval_chain.invoke({
        "input": question
    })
   
    print("\nAssistant:\n")

    print(response["answer"])

    print("\nSources:")

    for doc in response["context"]:
        print(doc.metadata["source"])
