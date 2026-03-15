# AI Code Reviewer – Intelligent Static Code Analysis Tool

A modern, intelligent code analysis tool that provides instant feedback on **code quality, security vulnerabilities, and performance issues**. Built with Flask and vanilla JavaScript, this application features a sleek SaaS-style interface and supports multiple programming languages.

The goal of this project is to help developers quickly identify issues in their code and improve maintainability, security, and performance.

---

# ✨ Features

### Multi-Language Support

Analyze code written in:

Python (.py)
JavaScript (.js)
Java (.java)
C (.c)
C++ (.cpp)
Go (.go)
Rust (.rs)
TypeScript (.ts)
Ruby (.rb)
PHP (.php)
Swift (.swift)
Kotlin (.kt)

### Comprehensive Code Analysis

The system performs multiple types of analysis:

**Quality Checks**

- Detects long functions
- Identifies unused variables and imports
- Flags poor naming conventions
- Detects overly long lines

**Security Scanning**

- Hardcoded passwords or API keys
- Dangerous function usage (eval, exec)
- SQL injection patterns
- Unsafe deserialization risks
- OS command injection patterns

**Performance Detection**

- Nested loops (O(n²) complexity)
- Inefficient string operations
- Repeated function calls inside loops
- Unnecessary type conversions

### Smart Scoring System

Each file and project receives a **quality score from 0–10** with a letter grade.

```
Base Score: 10

CRITICAL issue  → -2 points
WARNING issue   → -1 point
SUGGESTION      → -0.25 points

Final score is clamped between 0 and 10
```

Grades:

A+ → 9.0+
A → 8.0+
B → 7.0+
C → 6.0+
D → 5.0+
F → below 5.0

### Additional Features

- Severity filtering (Critical / Warning / Suggestion)
- Per-file issue breakdown
- Real-time analysis results
- File upload or direct code paste
- Export analysis reports
- Dark and Light theme toggle
- Responsive UI for desktop, tablet, and mobile
- Keyboard shortcuts (Ctrl + Enter to analyze)

---

# 🧰 Tech Stack

### Backend

- Python
- Flask
- Python AST module for code analysis

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript

### Design

- Responsive layout
- SaaS-style UI design
- Dark / Light theme support
- CSS animations and modern styling

---

# 🚀 Quick Start

## Prerequisites

Python 3.8 or higher
pip (Python package manager)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/ayush28-5/ai-code-reviewer.git
cd ai-code-reviewer
```

Create and activate a virtual environment (recommended):

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

# 📖 Usage

## Using the Web Interface

1. Paste code directly into the editor
2. Upload source code files
3. Click **Review Code** or press **Ctrl + Enter**
4. Review analysis results including score and detected issues
5. Filter issues by severity
6. Export the report if needed

---

# 🏗️ Project Architecture

```
ai-code-reviewer/
├── app.py
├── requirements.txt
├── analyzer/
│   ├── __init__.py
│   ├── quality_checker.py
│   ├── security_checker.py
│   └── performance_checker.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   ├── script.js
│   └── favicon.svg
└── uploads/
```

The application is structured using a **modular analysis engine** that separates different types of code checks.

---

# 🔍 How It Works

### Quality Checker

Detects structural and style issues such as:

- Functions longer than 30 lines
- Unused variables
- Poor naming conventions
- Excessively long lines

### Security Checker

Scans for common security risks:

- Hardcoded credentials
- Dangerous function usage
- SQL injection patterns
- Unsafe serialization

### Performance Checker

Identifies inefficient code patterns:

- Nested loops
- Repeated function calls
- Inefficient string operations
- Redundant type conversions

---

# 🖥 API Endpoints

### POST `/api/analyze`

Analyzes code and returns structured results.

Example response:

```json
{
  "success": true,
  "data": {
    "overall_score": 8.5,
    "total_files": 1,
    "total_issues": 2
  }
}
```

### GET `/api/health`

Health check endpoint.

Response:

```json
{
  "status": "ok"
}
```

---

# 🌐 Deployment

For production deployment consider:

- Using a production WSGI server such as **Gunicorn**
- Running behind **Nginx reverse proxy**
- Enabling HTTPS
- Setting `DEBUG=False`

Example:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

# 🌍 Live Demo

Live demo deployment coming soon.

---

# 🔧 Development

Run the application in development mode:

```bash
flask run --host 127.0.0.1 --port 5000 --reload
```

Test the API with curl:

```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -F "code=def hello(): pass"
```

---

# 💡 Future Enhancements

- Database support for result history
- GitHub pull request integration
- Custom rule engine
- Machine learning based analysis
- Team collaboration features
- Browser extension for IDE integration
- Docker containerization

---

# 🤝 Contributing

Contributions are welcome. Suggestions for new rules, language support, and feature improvements are encouraged.

---

# 📄 License

This project is licensed under the MIT License.

---

Built with Python, Flask, and modern web technologies.
