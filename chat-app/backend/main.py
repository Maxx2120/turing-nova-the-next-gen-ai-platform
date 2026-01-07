from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.models import init_db
from websocket import router as websocket_router
from utils.logger import logger
import uvicorn

app = FastAPI(
    title="AI Chat Backend",
    description="Production-grade AI Chat Backend using FastAPI & Ollama",
    version="1.0.0"
)

# CORS Configuration
# Allow all origins for dev simplicity, restrict in real production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database on Startup
@app.on_event("startup")
def on_startup():
    logger.info("Starting up application...")
    init_db()
    logger.info("Database initialized.")

# Include Routers
app.include_router(websocket_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "AI Chat Backend"}

if __name__ == "__main__":
    # Usually run via 'uvicorn main:app' but this allows direct python execution
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
