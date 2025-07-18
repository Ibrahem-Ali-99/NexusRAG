import os
import chromadb
from transformers import CLIPProcessor, CLIPModel, BlipProcessor, BlipForConditionalGeneration
import torch
import groq

class MultimodalRAGProcessor:
    def __init__(self, collection_name="multimodal_rag"):
        print("Initializing models...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        self.caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(self.device)

        self.db_client = chromadb.Client()
        self.collection = self.db_client.get_or_create_collection(name=collection_name)
        print("Models and database are ready.")

    def _get_text_embedding(self, text):
        inputs = self.clip_processor(text=text, return_tensors="pt", truncation=True, padding=True, max_length=77).to(self.device)
        with torch.no_grad():
            outputs = self.clip_model.get_text_features(**inputs)
        return outputs.cpu().numpy().flatten()

    def _get_image_embedding(self, image_obj):
        image = image_obj.convert("RGB")
        inputs = self.clip_processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.clip_model.get_image_features(**inputs)
        return outputs.cpu().numpy().flatten()

    def get_image_description(self, image_obj):
        image = image_obj.convert("RGB")
        inputs = self.caption_processor(image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            out = self.caption_model.generate(**inputs, max_new_tokens=50)
        return self.caption_processor.decode(out[0], skip_special_tokens=True)

    def store_chunks(self, chunks):
        all_ids, all_embeddings, all_documents, all_metadata = [], [], [], []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"chunk_{i}"
            doc = chunk['content']
            metadata = {'type': chunk['type'], 'page': chunk['page_num']}

            if chunk['type'] == 'text':
                embedding = self._get_text_embedding(doc)
            elif chunk['type'] == 'image':
                embedding = self._get_image_embedding(chunk['image_obj'])
            
            all_ids.append(chunk_id)
            all_embeddings.append(embedding.tolist())
            all_documents.append(doc)
            all_metadata.append(metadata)

        if all_ids:
            self.collection.add(ids=all_ids, embeddings=all_embeddings, documents=all_documents, metadatas=all_metadata)
            print(f"Stored {len(all_ids)} text and image chunks in the database.")

    def query_rag(self, user_query, n_results=5):
        text_embedding = self._get_text_embedding(user_query).tolist()
        
        results = self.collection.query(
            query_embeddings=[text_embedding],
            n_results=n_results
        )
        
        unique_docs = set(doc for doc_list in results['documents'] for doc in doc_list)
        context = "\n\n---\n\n".join(list(unique_docs))
        return context

    def generate_answer(self, user_query, context):
        client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
        prompt = f"""You are an expert AI assistant. Answer the user's question based ONLY on the provided context. If the information is not in the context, say so. Be concise.

CONTEXT:
---
{context}
---

USER QUESTION: {user_query}

ANSWER:"""
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                temperature=0.1,
                max_tokens=1024
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f" Error generating answer with Groq: {e}"