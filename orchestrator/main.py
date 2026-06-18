"""
AI Engineering OS - Orchestrator API
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import json
import asyncio

from agents.agent_manager import AgentManager
from agents.adapters import *
from orchestrator.workflow_engine import WorkflowEngine
from orchestrator.workspace_manager import WorkspaceManager
from communication.event_system import EventSystem, EventType
from memory.vector_store import VectorStore
from evaluation.evaluator import Evaluator
from monitoring.metrics import MetricsCollector

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
# Event System
event_system = EventSystem()

# Agent Manager
agent_manager = AgentManager(config)
agent_manager.register_agent("aider", AiderAdapter(config))
agent_manager.register_agent("openhands", OpenHandsAdapter(config))
# ... سجل باقي الوكلاء

# Workflow Engine
workflow_engine = WorkflowEngine(agent_manager)

# Workspace Manager
workspace_manager = WorkspaceManager()

# Vector Store
vector_store = VectorStore()

# Evaluator
evaluator = Evaluator(config)

# Metrics
metrics_collector = MetricsCollector()

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
# Event Handlers
# ============================================================
async def handle_task_started(event_type: str, data: dict):
    print(f"📌 Task Started: {data.get('task_id')} by {data.get('agent')}")

async def handle_task_completed(event_type: str, data: dict):
    print(f"✅ Task Completed: {data.get('task_id')} in {data.get('duration')}s")

async def handle_task_failed(event_type: str, data: dict):
    print(f"❌ Task Failed: {data.get('task_id')} - {data.get('error')}")

# التسجيل
event_system.subscribe(EventType.TASK_STARTED.value, handle_task_started)
event_system.subscribe(EventType.TASK_COMPLETED.value, handle_task_completed)
event_system.subscribe(EventType.TASK_FAILED.value, handle_task_failed)

# ============================================================
# API Endpoints
# ============================================================
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/agents")
async def list_agents():
    return {"agents": agent_manager.get_all_agents()}

@app.get("/api/metrics")
async def get_metrics():
    return metrics_collector.get_summary()

@app.post("/api/task")
async def execute_task(request: TaskRequest):
    start_time = datetime.now()
    
    # نشر حدث بدء المهمة
    task_id = f"task_{start_time.timestamp()}"
    await event_system.publish(EventType.TASK_STARTED.value, {
        "task_id": task_id,
        "agent": request.agent_name,
        "description": request.description
    })
    
    try:
        result = await agent_manager.execute_task(
            request.agent_name,
            {"description": request.description, "workspace": request.workspace}
        )
        
        # تسجيل المقاييس
        metrics_collector.record_execution(
            request.agent_name,
            result.status == "success",
            result.duration,
            result.error
        )
        
        # نشر حدث اكتمال المهمة
        await event_system.publish(EventType.TASK_COMPLETED.value, {
            "task_id": task_id,
            "agent": request.agent_name,
            "status": result.status,
            "duration": result.duration
        })
        
        return result.to_dict()
        
    except Exception as e:
        await event_system.publish(EventType.TASK_FAILED.value, {
            "task_id": task_id,
            "agent": request.agent_name,
            "error": str(e)
        })
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.post("/api/project")
async def execute_project(request: ProjectRequest):
    # 1. إنشاء workspace
    workspace_id = workspace_manager.create_workspace()
    
    # 2. نشر حدث بدء المشروع
    await event_system.publish(EventType.WORKFLOW_STARTED.value, {
        "workspace_id": workspace_id,
        "description": request.description
    })
    
    # 3. إنشاء وتنفيذ سير العمل
    workflow_id = workflow_engine.create_project_workflow(request.description)
    result = await workflow_engine.execute_workflow(workflow_id)
    
    # 4. تقييم النتيجة
    evaluation = evaluator.evaluate_code(workspace_manager.get_workspace(workspace_id))
    result["evaluation"] = evaluation
    
    # 5. تخزين الذاكرة
    vector_store.store_project_memory(workflow_id, {
        "description": request.description,
        "workspace_id": workspace_id,
        "status": result["status"],
        "evaluation": evaluation,
        "timestamp": str(datetime.now())
    })
    
    # 6. نشر حدث اكتمال المشروع
    await event_system.publish(EventType.WORKFLOW_COMPLETED.value, {
        "workspace_id": workspace_id,
        "status": result["status"]
    })
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/api/metrics/agents")
async def get_agent_metrics():
    return metrics_collector.get_summary()

@app.get("/api/metrics/agent/{agent_name}")
async def get_single_agent_metrics(agent_name: str):
    summary = metrics_collector.get_summary()
    if agent_name in summary:
        return summary[agent_name]
    return {"error": "Agent not found"}
