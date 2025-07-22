# JobJob the Jobot 🤖

A personalized AI assistant built with LangChain to help with job search activities including resume optimization, cover letter generation, interview preparation, and job fit analysis.

## Features

- **📝 Resume Optimizer**: Get personalized suggestions to tailor your resume for specific jobs
- **🎤 Interview Preparation**: Generate likely interview questions with personalized answers
- **📋 Application Questions**: Draft responses to job application questions with your context
- **⚙️ Personal Context**: Maintain a permanent context file to personalize all responses

## Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
job-search-ai/
├── app.py                   # Streamlit web interface
├── job_search_ai.py        # Main AI application logic
├── document_manager.py     # Document processing and vector storage
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── personal_context.txt   # Your personal context (created automatically)
├── README.md              # This file
└── context/
    ├── prompts/           # Additional instruction for each task
    ├── uploads/           # Uploaded documents
    └── vectorstore/       # Vector database files
```

## How to Use

### 1. Upload Your Documents
- In the sidebar, upload your resume, cover letters, project descriptions, or any relevant experience documents
- Supported formats: PDF, TXT, MD
- Click "Process Documents" to add them to your knowledge base

### 2. Set Up Personal Context

**Create your personal context file:**
- The app will create a `personal_context.txt` template file
- Edit this file with your career goals, interests, work style, and background
- Or use the "Personal Context Management" section in the app interface
- This information personalizes all AI responses to your specific situation

### 3. Use the Features

**Resume Optimizer:**
- Paste a job description
- Optionally specify sections to focus on
- Get personalized optimization suggestions

**Interview Prep:**
- Paste the job description
- Select interview type (General, Technical, Behavioral, etc.)
- Get likely questions with personalized answers

**Application Questions:**
- Enter any job application question
- Optionally include the job description for context
- Get authentic, personalized responses based on your background

## Technical Details

### Architecture
- **LangChain**: Framework for building LLM applications
- **FAISS**: Vector database for document similarity search
- **OpenAI**: GPT models for text generation
- **Streamlit**: Web interface framework

### Data Processing
1. Documents are split into chunks using RecursiveCharacterTextSplitter
2. Chunks are converted to embeddings using OpenAI's embedding model
3. Embeddings are stored in FAISS vector database
4. Relevant chunks are retrieved based on query similarity
5. Retrieved context is used with GPT to generate personalized responses

### Privacy & Data
- All documents are processed locally
- No data is shared externally except API calls to OpenAI
- You can clear all data anytime using the "Clear All Data" button

## Configuration Options

Edit `config.py` to customize:
- Model selection (GPT-3.5-turbo, GPT-4, etc.)
- Chunk size and overlap for document processing
- Vector store location
- Other processing parameters

## Troubleshooting

**"Please set your OpenAI API key" error:**
- Make sure you've created a `.env` file with your API key
- Verify the key is correct and has sufficient credits

**"No documents loaded" warning:**
- Upload documents in the sidebar first
- Supported formats: PDF, TXT, MD only

**Slow response times:**
- Try using GPT-3.5-turbo instead of GPT-4
- Reduce chunk size in config.py for faster processing

**Import errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using a compatible Python version (3.8+)

## Customization

You can extend the application by:
- Adding new document types in `document_manager.py`
- Creating new features in `job_search_ai.py`
- Modifying prompts for different output styles
- Adding new tabs in the Streamlit interface

## Cost Considerations

- Document processing (embeddings): ~$0.0001 per 1000 tokens
- Query responses: GPT-3.5-turbo ~$0.002 per 1000 tokens, GPT-4 ~$0.03 per 1000 tokens
- Typical usage costs $0.10-$1.00 per session depending on document size and queries

## License

This project is open source. Feel free to modify and distribute as needed.