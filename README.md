# NexusRAG 🤖✨

NexusRAG is a powerful, multimodal Retrieval-Augmented Generation (RAG) system built to understand both text and images within PDF documents. It provides rich, context-aware answers to user queries through an intuitive Streamlit interface.

This project is optimized for easy deployment on Hugging Face Spaces.

![NexusRAG Interface Screenshot](https_user-images.githubusercontent.com/12345/nexusrag-screenshot.png) 

## ✨ Features

-   **📚 Multimodal Understanding**: Extracts and analyzes both text and images from any uploaded PDF.
-   **🖼️ AI-Powered Image Captioning**: Uses the BLIP model to automatically generate descriptive captions for images, providing richer context.
-   **🚀 High-Performance LLM**: Leverages the fast Groq LPU™ Inference Engine for real-time answer generation.
-   **🧩 Vector-Based Retrieval**: Uses ChromaDB for efficient in-memory similarity search.
-   **🖥️ Interactive UI**: A user-friendly Streamlit interface for uploading documents and asking questions.
-   **🤗 Hugging Face Ready**: Designed for simple, one-click deployment on Hugging Face Spaces.

## ⚙️ How It Works

1.  **Upload**: The user uploads a PDF document through the Streamlit interface.
2.  **Process & Ingest**: The application processes the PDF in-memory. Text is chunked, and images are extracted.
3.  **Caption & Embed**: Images are captioned by a BLIP model. Both text chunks and image captions are converted into vector embeddings using CLIP.
4.  **Store**: The embeddings and their content are loaded into an in-memory ChromaDB instance for the current session.
5.  **Query & Retrieve**: When the user asks a question, the query is used to retrieve the most relevant text and image contexts from the database.
6.  **Generate**: The retrieved context is passed to the Llama 3 model via the Groq API to generate a concise, accurate answer, which is then displayed to the user.

## 🚀 Deployment on Hugging Face Spaces

Deploying NexusRAG is straightforward.

1.  **Create a New Space**:
    *   Go to [Hugging Face Spaces](https://huggingface.co/new-space) and click "Create new Space".
    *   Give it a name (e.g., `YourName/NexusRAG`).
    *   Select "Streamlit" as the Space SDK.
    *   Choose a hardware resource. A "CPU upgrade" is recommended for faster model loading.
    *   Choose "Public" or "Private".

2.  **Add Your Groq API Key**:
    *   In your new Space, go to the "Settings" tab.
    *   Find the "Repository secrets" section.
    *   Click "New secret" and add your `GROQ_API_KEY`. The app will be able to access this securely. **Do not write your key in the code.**

3.  **Upload Your Files**:
    *   Go to the "Files" tab and upload all the files from this repository. You can do this via the web interface or by using `git`.

The Space will automatically build and launch your Streamlit application.

## 💻 Local Development

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/NexusRAG.git
    cd NexusRAG
    ```
2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
3.  **Set up your environment variables:**
    ```bash
    cp .env.example .env
    # Now edit the .env file and add your GROQ_API_KEY
    ```
4.  **Run the Streamlit app:**
    ```bash
    streamlit run app/streamlit_app.py
    ```

## 📄 License

This project is licensed under the [MIT License](LICENSE).