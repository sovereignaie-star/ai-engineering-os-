from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class AgentResult(BaseModel):
    agent: str
    status: str  # "success", "failed", "running", "cancelled"
    stdout: str
    stderr: str
    duration: float
    files_changed: List[str] = []
    artifacts: List[str] = []
    metadata: Dict[str, any] = {}
    started_at: datetime = datetime.now()
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return self.model_dump()
