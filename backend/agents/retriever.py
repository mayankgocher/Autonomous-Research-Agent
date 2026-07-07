from agents.state import ResearchState
from database.chroma_db import get_vector_store
from langchain.text_splitter import RecursiveCharacterTextSplitter

def retriever_agent(state: ResearchState) -> ResearchState:
    """Chunk extracted texts and store in ChromaDB."""
    try:
        vectorstore = get_vector_store(f"research_{state['research_id']}")
        
        texts_to_add = []
        metadatas = []
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        
        for paper_id, text in state.get('extracted_texts', {}).items():
            if not text:
                continue
                
            chunks = text_splitter.split_text(text)
            for chunk in chunks:
                texts_to_add.append(chunk)
                metadatas.append({"source": paper_id})
                
        # Also add web results text
        for idx, web_res in enumerate(state.get('web_results', [])):
            if web_res.get('snippet'):
                texts_to_add.append(web_res['snippet'])
                metadatas.append({"source": f"web_{idx}", "url": web_res['url']})
                
        if texts_to_add:
            vectorstore.add_texts(texts=texts_to_add, metadatas=metadatas)
            
    except Exception as e:
        print(f"Retriever error: {e}")
        state['errors'].append(f"Retriever error: {e}")
        
    return state
