"""
AI Evaluation Layer
تقييم جودة الكود والبنية بشكل مستقل
"""

import os
import json
import ast
import subprocess

class Evaluator:
    def __init__(self, config):
        self.config = config
        self.min_score = config.get("min_evaluation_score", 8.0)

    def evaluate_code(self, code_path: str) -> dict:
        """تقييم جودة الكود"""
        results = {
            "architecture": 0,
            "code_quality": 0,
            "performance": 0,
            "ux_consistency": 0,
            "technical_debt": 0,
            "over_engineering": 0,
            "overall": 0,
            "issues": []
        }

        # 1. تحليل البنية
        results["architecture"] = self._evaluate_architecture(code_path)
        
        # 2. جودة الكود
        results["code_quality"] = self._evaluate_code_quality(code_path)
        
        # 3. الأداء
        results["performance"] = self._evaluate_performance(code_path)
        
        # 4. الديون التقنية
        results["technical_debt"] = self._evaluate_technical_debt(code_path)
        
        # 5. التقييم الشامل
        results["overall"] = sum([
            results["architecture"] * 0.25,
            results["code_quality"] * 0.25,
            results["performance"] * 0.20,
            results["technical_debt"] * 0.30
        ])
        
        results["passed"] = results["overall"] >= self.min_score
        
        return results

    def _evaluate_architecture(self, code_path: str) -> float:
        """تقييم البنية"""
        score = 8.0
        
        # التحقق من وجود ملفات أساسية
        required_files = ["main.py", "requirements.txt", "README.md"]
        for file in required_files:
            if not os.path.exists(os.path.join(code_path, file)):
                score -= 1.0
        
        # التحقق من هيكل المجلدات
        required_dirs = ["src", "tests", "docs"]
        for dir_name in required_dirs:
            if not os.path.exists(os.path.join(code_path, dir_name)):
                score -= 0.5
        
        return max(0, min(10, score))

    def _evaluate_code_quality(self, code_path: str) -> float:
        """تقييم جودة الكود"""
        score = 8.0
        
        # استخدام pylint أو flake8
        try:
            result = subprocess.run(
                ["pylint", "--exit-zero", code_path],
                capture_output=True,
                text=True
            )
            # تحليل النتيجة
            if "Your code has been rated at" in result.stdout:
                rating = float(result.stdout.split("rated at ")[1].split("/")[0])
                score = rating * 2
        except:
            pass
        
        return max(0, min(10, score))

    def _evaluate_performance(self, code_path: str) -> float:
        """تقييم الأداء"""
        # تقييم بسيط بناءً على حجم الكود
        total_lines = 0
        total_files = 0
        
        for root, dirs, files in os.walk(code_path):
            for file in files:
                if file.endswith(".py"):
                    total_files += 1
                    with open(os.path.join(root, file), 'r') as f:
                        total_lines += len(f.readlines())
        
        # كلما قل الكود كان أفضل (معقولة)
        if total_lines < 100:
            return 9.0
        elif total_lines < 500:
            return 8.0
        elif total_lines < 1000:
            return 7.0
        else:
            return 6.0

    def _evaluate_technical_debt(self, code_path: str) -> float:
        """تقييم الديون التقنية"""
        score = 8.0
        
        # البحث عن علامات الديون التقنية
        debt_patterns = [
            "TODO",
            "FIXME",
            "HACK",
            "XXX",
            "deprecated",
            "legacy"
        ]
        
        debt_count = 0
        for root, dirs, files in os.walk(code_path):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                        for pattern in debt_patterns:
                            debt_count += content.count(pattern)
        
        # كلما قل عدد الديون كان أفضل
        if debt_count == 0:
            return 10.0
        elif debt_count < 5:
            return 8.0
        elif debt_count < 20:
            return 6.0
        else:
            return 4.0

    def should_improve(self, evaluation: dict) -> bool:
        """هل يحتاج الكود إلى تحسين؟"""
        return not evaluation.get("passed", False)
