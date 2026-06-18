"""
UI Layer
واجهة مستخدم لإدخال أوصاف المشاريع
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import json

# إنشاء مجلد القوالب
os.makedirs("orchestrator/templates", exist_ok=True)

# قالب HTML
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Engineering OS</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #e6edf3; min-height: 100vh; display: flex; justify-content: center; align-items: center; }
        .container { max-width: 800px; width: 100%; padding: 2rem; }
        .card { background: #161b22; border-radius: 16px; padding: 2rem; border: 1px solid #30363d; }
        h1 { font-size: 2rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #58a6ff, #f0883e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { color: #8b949e; margin-bottom: 2rem; }
        textarea { width: 100%; padding: 1rem; background: #0d1117; border: 1px solid #30363d; border-radius: 8px; color: #e6edf3; font-size: 1rem; resize: vertical; min-height: 120px; }
        textarea:focus { outline: none; border-color: #58a6ff; }
        select { width: 100%; padding: 0.75rem; background: #0d1117; border: 1px solid #30363d; border-radius: 8px; color: #e6edf3; font-size: 1rem; margin-top: 0.5rem; }
        button { background: #238636; color: white; border: none; padding: 0.75rem 2rem; border-radius: 8px; font-size: 1rem; cursor: pointer; margin-top: 1rem; transition: all 0.2s; width: 100%; }
        button:hover { background: #2ea043; }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        .result { margin-top: 1.5rem; background: #0d1117; border-radius: 8px; padding: 1rem; border: 1px solid #30363d; display: none; }
        .result.show { display: block; }
        .result pre { white-space: pre-wrap; word-wrap: break-word; font-size: 0.85rem; color: #e6edf3; }
        .status { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: bold; }
        .status.success { background: #238636; color: white; }
        .status.failed { background: #da3633; color: white; }
        .status.running { background: #d29922; color: white; }
        .agents-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; margin: 0.5rem 0 1rem 0; }
        .agent-tag { background: #21262d; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.7rem; text-align: center; border: 1px solid #30363d; }
        .form-group { margin-bottom: 1rem; }
        label { display: block; margin-bottom: 0.25rem; color: #8b949e; font-size: 0.9rem; }
        .loading { display: none; text-align: center; padding: 1rem; }
        .loading.show { display: block; }
        .spinner { display: inline-block; width: 24px; height: 24px; border: 3px solid #30363d; border-top-color: #58a6ff; border-radius: 50%; animation: spin 0.8s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .workflow-list { margin-top: 1rem; }
        .workflow-item { background: #0d1117; padding: 0.75rem; border-radius: 6px; margin-bottom: 0.5rem; border: 1px solid #21262d; display: flex; justify-content: space-between; align-items: center; }
        .workflow-item .name { color: #e6edf3; }
        .workflow-item .status { font-size: 0.7rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🧠 AI Engineering OS</h1>
            <p class="subtitle">Distributed Autonomous Software Engineering Platform</p>
            
            <form id="projectForm">
                <div class="form-group">
                    <label for="description">📝 وصف المشروع</label>
                    <textarea id="description" name="description" placeholder="مثال: ابنِ لي منصة تعليمية تفاعلية متكاملة بها نظام فيديو وتقييم..."></textarea>
                </div>
                
                <div class="form-group">
                    <label>🤖 الوكلاء المتاحون</label>
                    <div class="agents-grid" id="agentsGrid">
                        <span class="agent-tag">plandex</span>
                        <span class="agent-tag">openhands</span>
                        <span class="agent-tag">aider</span>
                        <span class="agent-tag">swe</span>
                        <span class="agent-tag">continue</span>
                        <span class="agent-tag">bolt</span>
                        <span class="agent-tag">gemini</span>
                        <span class="agent-tag">hermes</span>
                    </div>
                </div>
                
                <button type="submit" id="submitBtn">🚀 بناء المشروع</button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 0.5rem; color: #8b949e;">جاري بناء المشروع...</p>
            </div>
            
            <div class="result" id="result">
                <h3 style="margin-bottom: 0.5rem;">📊 نتيجة التنفيذ</h3>
                <div id="resultContent"></div>
            </div>
        </div>
    </div>

    <script>
        const form = document.getElementById('projectForm');
        const resultDiv = document.getElementById('result');
        const resultContent = document.getElementById('resultContent');
        const loadingDiv = document.getElementById('loading');
        const submitBtn = document.getElementById('submitBtn');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const description = document.getElementById('description').value.trim();
            if (!description) {
                alert('الرجاء إدخال وصف للمشروع');
                return;
            }

            // إظهار التحميل
            loadingDiv.classList.add('show');
            resultDiv.classList.remove('show');
            submitBtn.disabled = true;

            try {
                const response = await fetch('/api/project', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ description })
                });

                const data = await response.json();
                
                // عرض النتيجة
                resultContent.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                resultDiv.classList.add('show');
            } catch (error) {
                resultContent.innerHTML = `<pre style="color: #da3633;">Error: ${error.message}</pre>`;
                resultDiv.classList.add('show');
            } finally {
                loadingDiv.classList.remove('show');
                submitBtn.disabled = false;
            }
        });
    </script>
</body>
</html>
"""

# كتابة القالب
with open("orchestrator/templates/index.html", "w") as f:
    f.write(HTML_TEMPLATE)
