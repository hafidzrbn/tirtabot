import os
import json
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import RAG system
from rag_system import DoctorTirtaRAG

app = FastAPI(title="TirtaBot AI Server", description="FastAPI Server for TirtaBot RAG Chatbot")

# Mount static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# History Storage File
HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history_data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)

# Initialize RAG Engine
rag_engine = None

@app.on_event("startup")
def startup_event():
    global rag_engine
    print("Starting TirtaBot FastAPI Server & Loading RAG Engine...")
    rag_engine = DoctorTirtaRAG()
    print("RAG Engine loaded successfully!")

class ChatRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "<h1>Index.html not found</h1>"

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    global rag_engine
    if not req.prompt or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt tidak boleh kosong.")
        
    if rag_engine is None:
        rag_engine = DoctorTirtaRAG()
        
    start_t = time.time()
    try:
        reply, sources, sent_counts = rag_engine.generate_rag_response(req.prompt)
    except Exception as e:
        print(f"RAG Error: {e}")
        raise HTTPException(status_code=500, detail=f"Gagal memproses RAG: {str(e)}")
        
    elapsed = round(time.time() - start_t, 2)
    timestamp = datetime.now().strftime("%H:%M - %d/%m/%Y")
    hist_id = f"hist_{int(time.time() * 1000)}"
    
    chat_item = {
        "id": hist_id,
        "prompt": req.prompt.strip(),
        "reply": reply,
        "sentiment_counts": sent_counts,
        "total_relevant": len(sources),
        "sources": sources,
        "timestamp": timestamp,
        "response_time_sec": elapsed
    }
    
    # Save to history
    history = load_history()
    history.insert(0, chat_item) # Insert at top
    save_history(history)
    
    return chat_item

@app.get("/api/history")
async def get_history():
    return load_history()

@app.delete("/api/history")
async def clear_history():
    save_history([])
    return {"message": "Riwayat analisis berhasil dihapus."}

@app.delete("/api/history/{item_id}")
async def delete_history_item(item_id: str):
    history = load_history()
    updated_history = [item for item in history if item.get("id") != item_id]
    save_history(updated_history)
    return {"message": f"Item {item_id} berhasil dihapus."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=7860, reload=True)
