"""
Workflow Engine
يدير تدفق المهام المتسلسلة والمتوازية
"""

from typing import List, Dict, Callable
import asyncio
import uuid
import json
import os

class WorkflowEngine:
    def __init__(self, agent_manager):
        self.agent_manager = agent_manager
        self.workflows = {}
        self.tasks = {}

    def create_workflow(self, name: str, steps: List[Dict]) -> str:
        """إنشاء سير عمل جديد"""
        workflow_id = str(uuid.uuid4())
        self.workflows[workflow_id] = {
            "name": name,
            "steps": steps,
            "status": "pending",
            "current_step": 0,
            "results": []
        }
        return workflow_id

    def create_project_workflow(self, description: str) -> str:
        """إنشاء سير عمل افتراضي لمشروع كامل"""
        steps = [
            {
                "agent": "plandex",
                "description": f"خطط لمشروع: {description}",
                "depends_on": []
            },
            {
                "agent": "openhands",
                "description": f"نفذ المشروع: {description}",
                "depends_on": ["plandex"]
            },
            {
                "agent": "aider",
                "description": f"حسن الكود بدقة: {description}",
                "depends_on": ["openhands"]
            },
            {
                "agent": "swe",
                "description": f"أصلح أي أخطاء في: {description}",
                "depends_on": ["aider"]
            },
            {
                "agent": "continue",
                "description": f"اختبر المشروع: {description}",
                "depends_on": ["swe"]
            }
        ]
        return self.create_workflow(f"Project: {description[:50]}...", steps)

    async def execute_workflow(self, workflow_id: str) -> Dict:
        """تنفيذ سير العمل"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {"status": "error", "message": "Workflow not found"}

        workflow["status"] = "running"
        results = []
        completed = set()

        for step in workflow["steps"]:
            # التحقق من الاعتماديات
            deps_met = all(dep in completed for dep in step.get("depends_on", []))
            if not deps_met:
                continue

            # تنفيذ المهمة
            result = self.agent_manager.execute_task(
                step["agent"],
                {"description": step["description"], "workspace": f"workspaces/{workflow_id}"}
            )
            
            results.append({
                "step": step,
                "result": result
            })
            
            if result.get("status") == "success":
                completed.add(step["agent"])
            else:
                workflow["status"] = "failed"
                break

        if workflow["status"] != "failed":
            workflow["status"] = "completed"
        
        workflow["results"] = results
        self.workflows[workflow_id] = workflow
        
        return {
            "workflow_id": workflow_id,
            "status": workflow["status"],
            "results": results
        }

    def get_workflow_status(self, workflow_id: str) -> Dict:
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {"status": "error", "message": "Workflow not found"}
        return {
            "workflow_id": workflow_id,
            "name": workflow["name"],
            "status": workflow["status"],
            "current_step": workflow["current_step"],
            "total_steps": len(workflow["steps"])
        }

    def save_workflows(self, path: str = "workspaces/workflows.json"):
        """حفظ حالة سير العمل"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.workflows, f, indent=2)

    def load_workflows(self, path: str = "workspaces/workflows.json"):
        """تحميل حالة سير العمل"""
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.workflows = json.load(f)
