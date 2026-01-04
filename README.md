# AI Research Assistant Agent

Multi-agent system that researches topics, summarizes findings, and fact-checks information using LangChain.

## 🎯 What It Does

User asks a question → System researches → Summarizes → Fact-checks → Returns verified report

## 🏗️ Architecture

**Three-Agent System:**
- **Researcher Agent**: Searches web using DuckDuckGo, finds relevant sources
- **Summarizer Agent**: Creates concise summaries from research
- **Fact-Checker Agent**: Validates claims against original sources
## 🏛️ Detailed Architecture

### System Flow
User Question
↓
Researcher Agent (DuckDuckGo search)
↓
Raw sources + URLs
↓
Summarizer Agent (LLM processing)
↓
Concise summary
↓
Fact-Checker Agent (Validation)
↓
Final verified report


### Agent Responsibilities

**Researcher Agent**
- Input: User question (string)
- Tool: DuckDuckGo search API
- Output: List of {url, title, snippet} objects
- Logic: Take question → search web → return top 5-10 results

**Summarizer Agent**  
- Input: Search results from Researcher
- Tool: LLM (Gemini)
- Output: 3-5 sentence summary
- Logic: Read all sources → extract key points → create coherent summary

**Fact-Checker Agent**
- Input: Summary + original sources
- Tool: LLM (Gemini)
- Output: Validation report with confidence score
- Logic: Compare summary claims → check against sources → flag unsupported statements

### Tech Implementation
- **LangChain**: Agent framework, tool calling, orchestration
- **Gemini Pro**: LLM for reasoning and text generation
- **DuckDuckGo API**: Free web search (no API key needed)
- **FastAPI**: REST endpoint for external access
- **Python asyncio**: Async agent execution for speed


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
