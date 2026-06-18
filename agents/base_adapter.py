from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

class BaseAgentAdapter(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    async def execute_task(self, task: dict) -> dict:
        """تنفيذ مهمة معينة"""
        pass

    @abstractmethod
    async def health_check(self) -> dict:
        """التحقق من صحة الوكيل"""
        pass

    @abstractmethod
    async def stop_task(self, task_id: str) -> bool:
        """إيقاف مهمة قيد التنفيذ"""
        pass

    def get_metadata(self) -> dict:
        return {
            "name": self.__class__.__name__,
            "version": getattr(self, "version", "1.0.0"),
            "type": getattr(self, "agent_type", "generic")
        }
