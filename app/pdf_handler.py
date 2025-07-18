import fitz  
from PIL import Image
import io

def process_pdf_from_upload(uploaded_file):
    all_chunks = []
    
    file_bytes = uploaded_file.getvalue()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    
    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        text_chunks = text.split('\n\n')
        for chunk in text_chunks:
            if len(chunk.strip()) > 150: 
                all_chunks.append({
                    "type": "text",
                    "content": chunk.strip(),
                    "page_num": page_num + 1
                })

    for page_num, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images(full=True)):
            try:
                base_image = doc.extract_image(img[0])
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                
                all_chunks.append({
                    "type": "image",
                    "content": f"[Image on page {page_num + 1}]", 
                    "image_obj": image,
                    "page_num": page_num + 1
                })
            except Exception as e:
                print(f"Skipping image on page {page_num + 1} due to error: {e}")
    
    print(f"Extracted {len(all_chunks)} chunks from the PDF.")
    return all_chunks