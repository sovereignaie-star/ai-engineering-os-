import uuid
import json
import os
from datetime import datetime

class WorkflowEngine:
    def __init__(self, agent_manager):
        self.agent_manager = agent_manager
        self.workflows = {}

    def create_workflow(self, name, steps):
        workflow_id = str(uuid.uuid4())
        self.workflows[workflow_id] = {
            "name": name,
            "steps": steps,
            "status": "pending",
            "results": []
        }
        return workflow_id

    def create_project_workflow(self, description):
        steps = [
            {"agent": "plandex", "description": f"خطط: {description}", "depends_on": []},
            {"agent": "openhands", "description": f"نفذ: {description}", "depends_on": ["plandex"]},
            {"agent": "aider", "description": f"حسن: {description}", "depends_on": ["openhands"]},
            {"agent": "swe", "description": f"أصلح: {description}", "depends_on": ["aider"]},
            {"agent": "continue", "description": f"اختبر: {description}", "depends_on": ["swe"]}
        ]
        return self.create_workflow(f"Project: {description[:50]}...", steps)

    async def execute_workflow(self, workflow_id):
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {"status": "error", "message": "Workflow not found"}

        workflow["status"] = "running"
        results = []
        completed = set()

        for step in workflow["steps"]:
            deps_met = all(dep in completed for dep in step.get("depends_on", []))
            if not deps_met:
                continue

            result = self.agent_manager.execute_task(
                step["agent"],
                {"description": step["description"], "workspace": f"workspaces/{workflow_id}"}
            )
            results.append({"step": step, "result": result})
            if result.get("status") == "success":
                completed.add(step["agent"])
            else:
                workflow["status"] = "failed"
                break

        if workflow["status"] != "failed":
            workflow["status"] = "completed"

        workflow["results"] = results
        return {"workflow_id": workflow_id, "status": workflow["status"], "results": results}

    def get_workflow_status(self, workflow_id):
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {"status": "error", "message": "Workflow not found"}
        return {
            "workflow_id": workflow_id,
            "name": workflow["name"],
            "status": workflow["status"],
            "total_steps": len(workflow["steps"])
        }
