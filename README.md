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


## 📄 License

This project is licensed under the [MIT License](LICENSE).
