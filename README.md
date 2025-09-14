# 🔍 AI Research Agent - Multi-Source Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green.svg)](https://openai.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-purple.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Professional AI-powered research assistant** that aggregates and synthesizes information from multiple web sources using advanced language models and intelligent workflows.

## 🚀 **Live Demo**
**[🔗 Access the Application](https://research-ai-engine.streamlit.app)**

---

## 📋 **Table of Contents**
- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Configuration](#api-configuration)
- [Performance](#performance)
- [Contributing](#contributing)

---

## 🎯 **Overview**

The AI Research Agent is a sophisticated multi-source intelligence platform that revolutionizes how users gather and analyze information. By leveraging cutting-edge AI technologies and parallel processing workflows, it delivers comprehensive research insights in seconds rather than hours.

### **Key Capabilities:**
- 🔍 **Multi-Source Search**: Simultaneously queries Google, Bing, and Reddit
- 🧠 **AI-Powered Analysis**: Uses GPT-4 for intelligent content synthesis  
- ⚡ **High Performance**: Optimized workflows with 3x speed improvements
- 🎨 **Interactive Interface**: Professional Streamlit web application
- 🔄 **Real-time Streaming**: Live response generation for immediate feedback

---

### **Architecture Components:**

#### **1. 🎨 Frontend Layer**
- **Streamlit Web App**: Professional UI with custom CSS styling
- **Real-time Streaming**: Live response generation and progress tracking
- **Responsive Design**: Mobile-friendly interface with dark/light themes

#### **2. 🧠 Orchestration Layer**
- **LangGraph Workflow**: State-based execution engine with parallel processing
- **State Management**: TypedDict-based state tracking across workflow nodes
- **Error Handling**: Graceful degradation with fallback mechanisms

#### **3. 🌐 Data Acquisition Layer**
- **BrightData Integration**: Enterprise-grade web scraping infrastructure
- **Multi-Engine Search**: Google, Bing, and Reddit API integrations
- **Parallel Processing**: Concurrent data fetching with timeout management

#### **4. 🤖 AI Processing Layer**
- **Model Selection**: GPT-4o-mini for analysis, GPT-4o for synthesis
- **Parallel Analysis**: Simultaneous processing of multiple data sources
- **Structured Outputs**: Pydantic models for consistent data formatting

#### **5. 📊 Performance Layer**
- **Caching Strategy**: In-memory caching for repeated queries
- **Timeout Management**: Aggressive timeouts to prevent bottlenecks
- **Quality Optimization**: Smart filtering for high-value content

---

## 🛠️ **Tech Stack**

### **Core Technologies**
| Category | Technology | Purpose | Version |
|----------|------------|---------|---------|
| **Language** | Python | Core development language | 3.12+ |
| **AI/ML** | OpenAI GPT-4o/4o-mini | Language model inference | Latest |
| **Workflow** | LangGraph | AI workflow orchestration | 0.0.40+ |
| **Web Framework** | Streamlit | Interactive web application | 1.28+ |
| **Data Processing** | Pydantic | Data validation and parsing | 2.0+ |

### **Infrastructure & APIs**
| Service | Purpose | Integration |
|---------|---------|-------------|
| **BrightData** | Web scraping and data collection | REST API |
| **OpenAI API** | Language model access | Python SDK |
| **Streamlit Cloud** | Application hosting | Git-based deployment |

### **Development Tools**
| Tool | Purpose |
|------|---------|
| **UV** | Fast Python package management |
| **Git** | Version control and CI/CD |
| **Docker** | Containerization (optional) |
| **Concurrent.futures** | Parallel processing |

---

## ✨ **Features**

### **🔍 Intelligent Research**
- **Multi-Source Aggregation**: Combines results from Google, Bing, and Reddit
- **Quality Filtering**: Automatically selects highest-value content
- **Context-Aware Analysis**: Understands query intent and provides relevant insights

### **⚡ Performance Optimizations**
- **Parallel Processing**: 3x faster than sequential processing
- **Smart Timeouts**: Prevents slow APIs from blocking entire workflow
- **Efficient Data Handling**: Processes only essential information

### **🎨 User Experience**
- **Real-time Feedback**: Live progress updates during research
- **Streaming Responses**: Immediate output as analysis completes
- **Professional Interface**: Clean, intuitive design with custom styling

### **🔧 Technical Excellence**
- **Error Resilience**: Graceful handling of API failures
- **Scalable Architecture**: Easily extensible for new data sources
- **Production Ready**: Comprehensive logging and monitoring

---

## 🚀 **Installation**

### **Prerequisites**
- Python 3.12 or higher
- Git
- API keys for OpenAI and BrightData

### **Local Development Setup**

```bash
# Clone the repository
git clone https://github.com/GalaxyMatrix/Advanced-AI-research-Agent-.git
cd Advanced-AI-research-Agent-

# Install UV (recommended) or use pip
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
uv sync

# Alternative: Using pip
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### **Environment Configuration**

Create a `.env` file with your API credentials:

```env
OPENAI_API_KEY=your_openai_api_key_here
BRIGHTDATA_API_KEY=your_brightdata_api_key_here
```

---

## 📖 **Usage**

### **Local Development**

```bash
# Activate virtual environment (if using UV)
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Run the Streamlit application
streamlit run streamlit.py

# Or using UV
uv run streamlit run streamlit.py
```

### **Command Line Interface**

```bash
# Run the chatbot directly
python main.py
```

### **Docker Deployment**

```bash
# Build and run with Docker
docker build -t ai-research-agent .
docker run -p 8501:8501 --env-file .env ai-research-agent
```

---

## 🔑 **API Configuration**

### **OpenAI Setup**
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an API key
3. Add to `.env` file or Streamlit secrets

### **BrightData Setup**
1. Sign up at [BrightData](https://brightdata.com/)
2. Create a web scraping zone
3. Get your API token
4. Configure dataset IDs in `webOperations.py`

### **Streamlit Cloud Secrets**
For production deployment, add secrets in TOML format:

```toml
OPENAI_API_KEY = "your_key_here"
BRIGHTDATA_API_KEY = "your_key_here"
```

---

## 📊 **Performance Metrics**

### **Speed Optimizations**
| Component | Original | Optimized | Improvement |
|-----------|----------|-----------|-------------|
| **Total Research Time** | 96.9s | ~35s | **65% faster** |
| **Web Scraping** | 44s | 15-25s | **45% faster** |
| **AI Analysis** | 30s | 8-12s | **70% faster** |
| **Parallel Processing** | Sequential | Concurrent | **3x speedup** |

### **Quality Improvements**
- **Reduced API Costs**: 60% lower through smart model selection
- **Higher Accuracy**: Focus on top-quality sources
- **Better UX**: Real-time streaming responses

---

## 🏆 **Advanced Features**

### **Intelligent URL Selection**
```python
# Smart Reddit URL filtering
selected_urls = analysis.selected_reddit_urls[:3]  # Top 3 most relevant
```

### **Adaptive Timeout Management**
```python
# Progressive timeout strategy
search_timeout = 25s    # Total search phase
analysis_timeout = 15s  # Per analysis task
synthesis_timeout = 20s # Final synthesis
```

### **Quality-First Data Processing**
```python
# Sort by engagement for quality
parsed_data.sort(key=lambda x: x.get("score", 0) + x.get("num_comments", 0), reverse=True)
```

---

## 🔮 **Future Enhancements**

- [ ] **Additional Sources**: Twitter, LinkedIn, academic papers
- [ ] **Caching Layer**: Redis for improved performance
- [ ] **User Accounts**: Personalized research history
- [ ] **Export Options**: PDF, Word, markdown reports
- [ ] **API Endpoints**: RESTful API for programmatic access
- [ ] **Analytics Dashboard**: Usage metrics and insights

---

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Development Workflow**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📜 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 **Author**

**GalaxyMatrix**
- GitHub: [@GalaxyMatrix](https://github.com/GalaxyMatrix)
- Project: [AI Research Agent](https://github.com/GalaxyMatrix/Advanced-AI-research-Agent-)

---

## 🔗 **Links**

- **Live Application**: [https://research-ai-engine.streamlit.app](https://research-ai-engine.streamlit.app)
- **GitHub Repository**: [Advanced-AI-research-Agent-](https://github.com/GalaxyMatrix/Advanced-AI-research-Agent-)
- **Documentation**: [Wiki](https://github.com/GalaxyMatrix/Advanced-AI-research-Agent-/wiki)

---

## 📊 **Project Stats**

![GitHub stars](https://img.shields.io/github/stars/GalaxyMatrix/Advanced-AI-research-Agent-?style=social)
![GitHub forks](https://img.shields.io/github/forks/GalaxyMatrix/Advanced-AI-research-Agent-?style=social)
![GitHub issues](https://img.shields.io/github/issues/GalaxyMatrix/Advanced-AI-research-Agent-)
![GitHub pull requests](https://img.shields.io/github/issues-pr/GalaxyMatrix/Advanced-AI-research-Agent-)

---

