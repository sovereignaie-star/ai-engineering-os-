import os
import shutil
import uuid
from pathlib import Path

class WorkspaceManager:
    def __init__(self, base_path: str = "workspaces"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self.active_workspaces = {}

    def create_workspace(self, project_id: str = None) -> str:
        if not project_id:
            project_id = str(uuid.uuid4())[:8]
        workspace_path = self.base_path / project_id
        workspace_path.mkdir(exist_ok=True)
        self.active_workspaces[project_id] = workspace_path
        return str(workspace_path)

    def get_workspace(self, project_id: str) -> str:
        workspace_path = self.base_path / project_id
        if workspace_path.exists():
            return str(workspace_path)
        return None

    def cleanup_workspace(self, project_id: str):
        workspace_path = self.base_path / project_id
        if workspace_path.exists():
            shutil.rmtree(workspace_path)
            del self.active_workspaces[project_id]

    def cleanup_all(self):
        for project_id in list(self.active_workspaces.keys()):
            self.cleanup_workspace(project_id)
