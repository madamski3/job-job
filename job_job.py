"""
Job Search AI - Main application logic using LangChain
"""
import os
from typing import Optional
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import config
from document_manager import DocumentManager

class JobSearchAI:
    def __init__(self):
        self.document_manager = DocumentManager()
        self.llm = ChatOpenAI(
            openai_api_key=config.OPENAI_API_KEY,
            model_name=config.DEFAULT_MODEL,
            temperature=0.7
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        self.qa_chain = None
        self._setup_qa_chain()
    
    def _get_personal_context(self) -> str:
        """Get personal context to include in prompts"""
        try:
            # Read directly from the personal context file
            context_file_path = os.path.join('context', 'background', 'personal_context.txt')
            with open(context_file_path, 'r') as f:
                context = f.read().strip()
            return f"\n\nPersonal Context: {context}\n" if context else ""
        except FileNotFoundError:
            return ""
    def _setup_qa_chain(self):
        """Setup the QA chain with custom prompts"""
        if self.document_manager.get_vectorstore() is not None:
            # Custom prompt template for job search
            template = """You are a professional career advisor AI. Use the following pieces of context about the user's experience, skills, and background to answer their question. Always provide specific, actionable advice based on their actual experience.

Context from documents: {context}

{chat_history}

Question: {question}

Instructions:
- Use specific examples from the user's experience when possible
- Provide concrete, actionable advice
- If asked about resume optimization, suggest specific changes
- If asked about cover letters, write personalized content
- If asked about interview prep, provide relevant questions and answers
- If asked about application questions, provide authentic responses based on their background
- Be professional but conversational

Answer:"""

            prompt = PromptTemplate(
                input_variables=["context", "chat_history", "question"],
                template=template
            )
            
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.document_manager.get_vectorstore().as_retriever(
                    search_kwargs={"k": 4}
                ),
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": prompt},
                return_source_documents=True,
                verbose=True
            )
    
    def add_documents(self, file_paths: list):
        """Add new documents to the knowledge base"""
        documents = self.document_manager.process_documents(file_paths)
        self.document_manager.create_vectorstore(documents)
        self._setup_qa_chain()  # Recreate chain with updated vectorstore
    
    def optimize_resume(self, job_description: str, sections: Optional[list] = None) -> str:
        """Analyze resume and suggest optimizations for a specific job"""

        with open(os.path.join(config.PROMPT_DIR, 'resume_optimization.txt')) as f_in:
            prompt = f_in.read()

        query = f"""
        Analyze my resume for this job description and suggest specific optimizations:
        
        Job Description: {job_description}
        
        {prompt}
        """
        
        if self.qa_chain:
            # Include personal context in the question
            context = self._get_personal_context()
            modified_query = f"{context} {query}" if context else query
            result = self.qa_chain({"question": modified_query})
            return result["answer"]
        else:
            return "Please upload your resume and experience documents first."
    
    def prepare_interview_questions(self, job_description: str, interview_type: str = "general") -> str:
        """Generate likely interview questions and suggested answers"""

        with open(os.path.join(config.PROMPT_DIR, 'interview_prep.txt')) as f_in:
            prompt = f_in.read()

        query = f"""
        Based on this job description: {job_description}
        
        Please help me prepare for a {interview_type} interview by:
        
        {prompt}
        """
        
        if self.qa_chain:
            # Include personal context in the question
            context = self._get_personal_context()
            modified_query = f"{context} {query}" if context else query
            result = self.qa_chain({"question": modified_query})
            return result["answer"]
        else:
            return "Please upload your resume and experience documents first."
    
    def draft_application_response(self, question: str, job_description: str = "") -> str:
        """Draft a response to a job application question"""
        job_context = f"\n\nJob Description: {job_description}" if job_description.strip() else ""
        
        with open(os.path.join(config.PROMPT_DIR, 'application_question.txt')) as f_in:
            prompt = f_in.read()

        query = f"""
        I'm filling out a job application and need help drafting a response to this question: "{question}"
        
        Please help me draft an answer that meets these criteria:
        {prompt}
        
        Here is job description that the company provided:
        {job_context}
        """
        
        if self.qa_chain:
            # Include personal context in the question
            context = self._get_personal_context()
            modified_query = f"{context} {query}" if context else query
            result = self.qa_chain({"question": modified_query})
            return result["answer"]
        else:
            return "Please upload your resume and experience documents first."
    
    def save_personal_context(self, content: str) -> bool:
        """Save personal context file"""
        return self.document_manager.save_personal_context(content)
    
    def get_personal_context(self) -> str:
        """Get current personal context"""
        # Get the existing context
        context = self.document_manager.load_personal_context()
        return context if context else ""
    
    def clear_all_data(self):
        """Clear all documents and reset"""
        self.document_manager.clear_vectorstore()
        self.memory.clear()
        self.qa_chain = None
    
    def get_document_count(self) -> int:
        """Get number of documents in the knowledge base"""
        if self.document_manager.get_vectorstore():
            return len(self.document_manager.get_vectorstore().docstore._dict)
        return 0