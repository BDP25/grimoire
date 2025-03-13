import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from langchain.schema import Document  

# Load the Markdown document as text
current_wd = os.getcwd()
file_directory = os.path.join(current_wd, "files")

def load_markdown_files(directory):
    """Loads all Markdown files from a given directory"""
    files_content = []
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                files_content.append(file.read())
    return files_content

# Load all Markdown files
raw_documents = load_markdown_files(file_directory)

# Convert the read strings into langchain Document objects
documents = [Document(page_content=doc) for doc in raw_documents]

# Split the text into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
split_texts = text_splitter.split_documents(documents)

# NLTK Tokenization and Stemming
nltk.download('punkt')  # Ensures that the punkt module for tokenization is available - divides a text into a list of sentences by using an unsupervised algorithm
stemmer = PorterStemmer()

def tokenize_and_stem(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Apply stemming to the tokens
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    return " ".join(stemmed_tokens)

# Apply tokenization and stemming to the texts
processed_texts = [tokenize_and_stem(text.page_content) for text in split_texts]


# TODO: ingest into pgvector database

