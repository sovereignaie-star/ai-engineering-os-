"""
AI Engineering OS - Orchestrator API
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from agents.agent_manager import AgentManager
from orchestrator.workflow_engine import WorkflowEngine
from memory.vector_store import VectorStore
from evaluation.evaluator import Evaluator
import os
import json

# ============================================================
# Config
# ============================================================
config = {
    "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
    "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
    "google_api_key": os.getenv("GOOGLE_API_KEY", ""),
    "model": os.getenv("DEFAULT_MODEL", "gpt-4"),
    "min_evaluation_score": float(os.getenv("MIN_EVALUATION_SCORE", "8.0")),
}

# ============================================================
# Components
# ============================================================
agent_manager = AgentManager(config)
workflow_engine = WorkflowEngine(agent_manager)
vector_store = VectorStore()
evaluator = Evaluator(config)

# ============================================================
# FastAPI App
# ============================================================
app = FastAPI(
    title="AI Engineering OS",
    description="Distributed Autonomous Software Engineering Platform",
    version="1.0.0"
)

# ============================================================
# Templates
# ============================================================
templates = Jinja2Templates(directory="orchestrator/templates")

# ============================================================
# Models
# ============================================================
class TaskRequest(BaseModel):
    agent_name: str
    description: str
    workspace: str = "."

class ProjectRequest(BaseModel):
    description: str

# ============================================================
# UI Endpoints
# ============================================================
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ============================================================
# API Endpoints
# ============================================================
@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/agents")
async def list_agents():
    return {"agents": agent_manager.get_all_agents()}

@app.post("/api/task")
async def execute_task(request: TaskRequest):
    result = agent_manager.execute_task(
        request.agent_name,
        {"description": request.description, "workspace": request.workspace}
    )
    return result

@app.post("/api/project")
async def execute_project(request: ProjectRequest):
    # 1. إنشاء سير العمل
    workflow_id = workflow_engine.create_project_workflow(request.description)
    
    # 2. تنفيذ سير العمل
    result = await workflow_engine.execute_workflow(workflow_id)
    
    # 3. تقييم النتيجة
    evaluation = evaluator.evaluate_code("workspaces/" + workflow_id)
    result["evaluation"] = evaluation
    
    # 4. تخزين الذاكرة
    vector_store.store_project_memory(workflow_id, {
        "description": request.description,
        "workflow_id": workflow_id,
        "status": result["status"],
        "evaluation": evaluation,
        "timestamp": str(datetime.now())
    })
    
    return result

@app.get("/api/workflow/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    return workflow_engine.get_workflow_status(workflow_id)

# ============================================================
# Import datetime
# ============================================================
from datetime import datetime

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
