import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rag.router import router as rag_chat_router


# Initialize application container object

app = FastAPI(
    title="Pizzeria RAG Service",
    description="Dedicated asynchronous analytics processing pipeline for operator assist utilities.",
    version="1.0.0"
)


# Enforce Cross-Origin Resource Sharing rules (Crucial for React connection loops)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows requests from local React development environments safely
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connect your fresh modular text search path router

app.include_router(rag_chat_router)

@app.get("/healthz", tags=["System Monitoring"])
async def check_liveness_probe():


    """Simple status check used by monitoring engines to verify endpoint connectivity."""

    return {"status": "healthy", "service": "Pizzeria RAG Service Active"}

if __name__ == "__main__":

    # Boot server line on port 8005 so it runs independently next to Django (8000)

    uvicorn.run("main.py:app", host="127.0.0.1", port=8005, reload=True)
