
# Multi-PDF-s 📚ChatApp 

 MultiPDF Chat App Chat  with Multiple PDFs using Langchain,gemma2,FAISS Vector DB with Seamless Streamlit Deployment. Get instant, Accurate responses from Awesome gemma2 OpenSource language Model. 

## 📝 Description
The Multi-PDF's Chat App is a Streamlit-based web application designed to facilitate interactive conversations with a chatbot. The app allows users to upload multiple PDF documents, extract text information from them, and train a chatbot using this extracted content. Users can then engage in real-time conversations with the chatbot.

 ![Image Alt](https://github.com/samuelsekhar1/pdfQA/blob/19996e60d4401c16b78bd47f00f6ed4242306a3d/Architecture.jpg)

The application follows these steps to provide responses to your questions:

1. **PDF Loading** : The app reads multiple PDF documents and extracts their text content.

2. **Text Chunking** : The extracted text is divided into smaller chunks that can be processed effectively.

3. **Language Model** : The application utilizes a language model to generate vector representations (embeddings) of the text chunks.

4. **Similarity Matching** : When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones.

5. **Response Generation** : The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs.

 ## ▶️Installation

Clone the repository:

`git clone https://github.com/samuelsekhar1/pdfQA

Install the required Python packages:

`pip install -r requirements.txt`

Create Open AI API key from `https://platform.openai.com/settings/organization/api-keys`

Create ChatGroq API key from `https://console.groq.com/keys` 

paste these API keys in the .env file in the root directory of the project with the following contents:

OPENAI_API_KEY= "paste open AI API Key"

GROQ_API_KEY= "paste chat groq AI API Key"

Run the Streamlit app:

`streamlit run app1.py`


