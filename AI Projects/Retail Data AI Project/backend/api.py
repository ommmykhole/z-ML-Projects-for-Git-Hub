from fastapi import FastAPI, HTTPException
from backend.schema import ChatRequest, ChatResponse
from backend.agent import ask_ai

app = FastAPI(title="Retail Sales Agentic AI API")


chat_history = []

# 1. GET Endpoint
@app.get("/")
def home():
    return {"status": "Retail AI Agent API is live!"}

# 2. POST Endpoint
@app.post("/chat", response_model=ChatResponse)
def chat_with_data(request: ChatRequest):
    try:
        answer, queries = ask_ai(request.question)
        
        # History save
        chat_history.append({
            "question": request.question,
            "answer": answer,
            "sql_queries": queries
        })
        
        return ChatResponse(
            question=request.question,
            answer=answer,
            sql_queries=queries
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. GET Endpoint: For View All Chat History
@app.get("/history")
def get_chat_history():
    return {"total_chats": len(chat_history), "history": chat_history}