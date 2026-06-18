from typing import Dict, List, Callable
from enum import Enum
import asyncio

class EventType(Enum):
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    AGENT_CRASHED = "agent_crashed"
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"

class EventSystem:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.event_queue = asyncio.Queue()

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    async def publish(self, event_type: str, data: dict):
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                await callback(event_type, data)

    async def run(self):
        while True:
            event_type, data = await self.event_queue.get()
            await self.publish(event_type, data)
