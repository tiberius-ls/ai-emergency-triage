## 🚀 Live Demo
- **App:** https://tiberius-ls.github.io/ai-emergency-triage
- **API:** https://ai-emergency-triage-production.up.railway.app
- **API Docs:** https://ai-emergency-triage-production.up.railway.app/docs
# AI Emergency Triage Assistant

An AI-powered patient triage system that analyses symptoms and classifies severity.

## What it does
- Accepts patient symptoms as input
- Uses LLM AI to diagnose and classify severity (CRITICAL, URGENT, STABLE)
- Returns structured JSON with condition, severity, and immediate action
- Sends email alerts for CRITICAL cases automatically
- Logs all triage results to Google Sheets

## Tech stack
- Python 3
- Groq API (LLaMA 3.3)
- Prompt engineering (chain-of-thought, JSON output, few-shot)
- n8n workflow automation
- Google Sheets API
- Gmail API

## Files
- `hello_groq.py` — basic API connection
- `chain.py` — 3-step AI diagnosis pipeline
- `tools.py` — AI-powered drug dose calculator

## Author
Chukwuemeka Ogbonna — Student Paramedic & AI Automation Developer