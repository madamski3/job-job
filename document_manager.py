"""
Document Manager for handling resume and experience documents
"""

import os
import shutil
from typing import List, Optional
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import config

class DocumentManager:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
        )
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=config.OPENAI_API_KEY,
            model=config.EMBEDDING_MODEL
        )
        self.vectorstore = None
        self.load_existing_vectorstore()
    
    def load_existing_vectorstore(self) -> None:
        """Load existing vector store if it exists"""
        vectorstore_path = os.path.join(config.VECTOR_STORE_PATH, "index.faiss")
        if os.path.exists(vectorstore_path):
            try:
                self.vectorstore = FAISS.load_local(
                    config.VECTOR_STORE_PATH, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print("Loaded existing vector store")
            except Exception as e:
                print(f"Error loading vector store: {e}")
                self.vectorstore = None
    
    def save_uploaded_file(self, uploaded_file) -> str:
        """Save uploaded file and return the path"""
        file_path = os.path.join(config.UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        return file_path
    
    def load_document(self, file_path: str) -> List[Document]:
        """Load a document based on file extension"""
        _, ext = os.path.splitext(file_path)
        
        if ext.lower() == '.pdf':
            loader = PyPDFLoader(file_path)
        elif ext.lower() in ['.txt', '.md']:
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        return loader.load()
    
    def process_documents(self, file_paths: List[str]) -> List[Document]:
        """Process multiple documents and split into chunks"""
        all_documents = []
        
        for file_path in file_paths:
            try:
                docs = self.load_document(file_path)
                # Add metadata
                for doc in docs:
                    doc.metadata['source_file'] = os.path.basename(file_path)
                all_documents.extend(docs)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        # Split documents into chunks
        splits = self.text_splitter.split_documents(all_documents)
        return splits
    
    def create_vectorstore(self, documents: List[Document]) -> None:
        """Create or update vector store with documents"""
        if not documents:
            print("No documents to process")
            return
        
        try:
            if self.vectorstore is None:
                # Create new vector store
                self.vectorstore = FAISS.from_documents(
                    documents=documents,
                    embedding=self.embeddings
                )
            else:
                # Add to existing vector store
                new_vectorstore = FAISS.from_documents(
                    documents=documents,
                    embedding=self.embeddings
                )
                self.vectorstore.merge_from(new_vectorstore)
            
            # Save the vector store
            self.vectorstore.save_local(config.VECTOR_STORE_PATH)
            print(f"Successfully processed {len(documents)} document chunks")
            
        except Exception as e:
            print(f"Error creating vector store: {e}")
    
    def get_vectorstore(self):
        """Get the vector store"""
        return self.vectorstore

    def get_document_count(self):
        """Get the number of original documents uploaded"""
        if os.path.exists(config.UPLOAD_DIR):
            return len([f for f in os.listdir(config.UPLOAD_DIR) if os.path.isfile(os.path.join(config.UPLOAD_DIR, f))])
        return 0
        
    def clear_vectorstore(self):
        """Clear the vector store and remove all stored files"""
        self.vectorstore = None
        # Remove the vectorstore directory if it exists
        if os.path.exists(config.VECTOR_STORE_PATH):
            shutil.rmtree(config.VECTOR_STORE_PATH)
        # Clear uploaded files
        if os.path.exists(config.UPLOAD_DIR):
            for file in os.listdir(config.UPLOAD_DIR):
                file_path = os.path.join(config.UPLOAD_DIR, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    
    def search_documents(self, query: str, k: int = 4) -> List[Document]:
        """Search for relevant documents"""
        if self.vectorstore is None:
            return []
        
        return self.vectorstore.similarity_search(query, k=k)
    
    def load_personal_context(self) -> Optional[str]:
        """Load personal context file if it exists"""
        if os.path.exists(config.CONTEXT_FILE_PATH):
            try:
                with open(config.CONTEXT_FILE_PATH, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error loading personal context: {e}")
        return None
    
    def save_personal_context(self, content: str) -> bool:
        """Save personal context to file"""
        try:
            with open(config.CONTEXT_FILE_PATH, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error saving personal context: {e}")
            return False
        """Clear the vector store and uploaded files"""
        # Remove vector store files
        if os.path.exists(config.VECTOR_STORE_PATH):
            shutil.rmtree(config.VECTOR_STORE_PATH)
            os.makedirs(config.VECTOR_STORE_PATH, exist_ok=True)
        
        # Remove uploaded files
        if os.path.exists(config.UPLOAD_DIR):
            shutil.rmtree(config.UPLOAD_DIR)
            os.makedirs(config.UPLOAD_DIR, exist_ok=True)
        
        self.vectorstore = None
        print("Cleared all documents and vector store")