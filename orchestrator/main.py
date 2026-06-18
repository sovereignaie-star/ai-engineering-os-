"""
AI Engineering OS - Orchestrator API
"""

from fastapi import FastAPI

app = FastAPI(
    title="AI Engineering OS",
    description="Distributed Autonomous Software Engineering Platform",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "AI Engineering OS is running",
        "status": "ok",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
