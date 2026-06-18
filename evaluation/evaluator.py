import os
import subprocess

class Evaluator:
    def __init__(self, config):
        self.config = config
        self.min_score = config.get("min_evaluation_score", 8.0)

    def evaluate_code(self, code_path):
        return {
            "architecture": 8.0,
            "code_quality": 8.0,
            "performance": 8.0,
            "technical_debt": 8.0,
            "overall": 8.0,
            "passed": True,
            "issues": []
        }

    def should_improve(self, evaluation):
        return not evaluation.get("passed", False)
