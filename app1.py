#Setting up Environment variable

from dotenv import load_dotenv
import os
from os import listdir
from os.path import isfile, join


load_dotenv()
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
groq_api_key=os.getenv("GROQ_API_KEY")

#os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

#Reading Multiple files from the given path
import PyPDF2


mypath = r"C:\Users\bhoom\OneDrive\Documents\simpleprojects\2pdfQ&Ausingastradb\pdfs"
text=''
# Get list of PDF files
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Process each PDF file
for file in onlyfiles:
    try:
        # Open the PDF file
        file_path = join(mypath, file)
        fileReader = PyPDF2.PdfReader(open(file_path, 'rb'))

        # Extract text from the first 3 pages
        for count in range(len(fileReader.pages)):  # Handle short PDFs
            pageObj = fileReader.pages[count]  # Use 'pages' instead of 'getPage()'
            text+= pageObj.extract_text()  # Use 'extract_text()' in PyPDF2 v3+

            #print(f"\n--- Text from {file} (Page {count+1}) ---\n")
            print(text)  
            #print("\n--------------------------------------\n")

    except Exception as e:
        print(f"Error processing {file}: {e}")

#Recursive Character chunk splitter: Used to convert documnet into small chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=50000, chunk_overlap=100)
documents = text_splitter.split_text(text)

#Converting chunks into embeddings
from langchain_openai import OpenAIEmbeddings

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)
embeddings.embed_documents(documents)

#Storing it in vector Faiss DB

from langchain_community.vectorstores import FAISS
db = FAISS.from_texts(documents,embedding=embeddings)
db.save_local("faiss_index")

#Defining AI model
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

prompt_template = """
    Answer the question  from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n
    Answer:
    """
from langchain_groq import ChatGroq
model=ChatGroq(model="gemma2-9b-it",groq_api_key=groq_api_key)
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)


#Streamlit webapp

import streamlit as st
st.set_page_config("Multi PDF Chatbot", page_icon=":scroll:")
st.header("Multi-PDF's - Chat Agent ")
user_question = st.text_input("Ask a Question from the PDF Files uploaded")
if user_question:
    Qn_embeddings=OpenAIEmbeddings(model="text-embedding-3-large")
    new_db = FAISS.load_local("faiss_index", Qn_embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True
    )
    st.write("Answer: ", response["output_text"])

    st.markdown("""
        <div style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: #0E1117; padding: 15px; text-align: center;">
            © <a href="https://github.com/gurpreetkaurjethra" target="_blank">Gurpreet Kaur Jethra</a> | Made with 
        </div>
    """, unsafe_allow_html=True)