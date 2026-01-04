# AI Research Assistant Agent

Multi-agent system that researches topics, summarizes findings, and fact-checks information using LangChain.

## 🎯 What It Does

User asks a question → System researches → Summarizes → Fact-checks → Returns verified report

## 🏗️ Architecture

**Three-Agent System:**
- **Researcher Agent**: Searches web using DuckDuckGo, finds relevant sources
- **Summarizer Agent**: Creates concise summaries from research
- **Fact-Checker Agent**: Validates claims against original sources

## 🛠️ Tech Stack

- **LangChain** - Agent orchestration framework
- **Gemini** - LLM for agent reasoning
- **DuckDuckGo Search** - Web search tool
- **FastAPI** - REST API endpoint
- **Python 3.10+**

## 📅 Development Timeline

### Week 1: Core Agents (Jan 4-10, 2026)
- [x] Day 0: Project setup ✅
- [ ] Day 1: Architecture planning
- [ ] Day 2: Web search tool
- [ ] Day 3: Researcher agent
- [ ] Day 4: Summarizer agent  
- [ ] Day 5: Fact-checker agent
- [ ] Day 6: Multi-agent orchestration
- [ ] Day 7: FastAPI endpoint + testing

## 🚀 Current Status

**Day 0 Complete** - Project initialized, ready to build agents

## 📝 Notes

Built as portfolio project for AI/DS hiring pipeline. Target: Production-ready by Feb 15, 2026.
