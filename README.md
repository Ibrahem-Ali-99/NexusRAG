# NexusRAG 🤖✨

A multimodal Retrieval-Augmented Generation (RAG) system that understands both text and images in PDF documents, built with Streamlit and the Groq API.

<img width="1896" height="587" alt="image" src="https://github.com/user-attachments/assets/28fea4da-923a-4847-b110-2213e7b3c31b" />


## Key Features

*   **Process Multimodal PDFs**: Extracts and analyzes both text and images from any uploaded PDF document.
*   **Automatic Image Captioning**: Uses a BLIP model to generate descriptive captions for images, providing richer context for retrieval.
*   **Fast Answer Generation**: Leverages the high-performance Groq LPU™ Inference Engine for real-time answers.
*   **Interactive UI**: A simple and user-friendly web interface built with Streamlit.

## How It Works

The system follows a standard RAG pipeline optimized for multimodal data:

1.  **Ingestion**: A user uploads a PDF. The system extracts text chunks and image objects in memory.
2.  **Caption & Embed**: Images are captioned, and both text chunks and the images themselves are converted into vector embeddings using a CLIP model.
3.  **Store**: Embeddings and their corresponding content are stored in an in-memory ChromaDB vector database for the session.
4.  **Retrieve**: When a user asks a question, the query is used to retrieve the most relevant text and image contexts from the database.
5.  **Generate**: The retrieved context is passed to a Large Language Model via the Groq API to generate a concise, context-aware answer.

## 🚀 Getting Started (Local Development)

Follow these steps to run the project on your local machine.

### Prerequisites

*   Python 3.9+
*   Git

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Ibrahem-Ali-99/NexusRAG.git
    cd NexusRAG
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    *   Create a file named `.env` in the root of the project.
    *   Add your Groq API key to this file:
        ```
        GROQ_API_KEY="grq_YourSecretKeyGoesHere"
        ```

4.  **Run the Streamlit app:**
    ```bash
    streamlit run app/streamlit_app.py
    ```
