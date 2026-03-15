# AI Code Reviewer

A modern, intelligent code analysis tool that provides instant feedback on code quality, security vulnerabilities, and performance issues. Built with Flask and vanilla JavaScript, featuring a sleek SaaS-style interface.

## ✨ Features

- **Multi-Language Support**: Analyze Python, JavaScript, Java, C++, Go, Rust, TypeScript, Ruby, PHP, Swift, and Kotlin
- **Comprehensive Analysis**:
  - Quality checks (long functions, unused variables, poor naming, etc.)
  - Security scanning (hardcoded secrets, dangerous functions, injection patterns)
  - Performance detection (nested loops, inefficient patterns, repeated calls)
- **Smart Scoring**: Per-file and overall quality scores (0-10 scale) with letter grades (A+ to F)
- **Severity Filtering**: Filter issues by Critical, Warning, or Suggestion severity levels
- **Real-Time Results**: Instant analysis with organized issue breakdowns
- **Multiple Input Methods**: Paste code directly or upload files
- **Export Results**: Download analysis reports as text files
- **Dark/Light Theme**: Toggle between sleek dark and clean light themes
- **Responsive Design**: Works flawlessly on desktop, tablet, and mobile devices
- **Keyboard Shortcuts**: Press Ctrl+Enter to analyze code quickly

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-code-reviewer.git
   cd ai-code-reviewer
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   cd ai-code-reviewer
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://127.0.0.1:5000
   ```

## 📖 Usage

### Via Web Interface

1. **Paste Code**: Switch to "Paste Code" tab and copy/paste your source code
2. **Upload Files**: Click the upload area to select files from your computer
3. **Analyze**: Click "Review Code" or press Ctrl+Enter
4. **Review Results**:
   - View overall quality score and grade
   - See critical, warning, and suggestion counts
   - Filter issues by severity
   - Review per-file breakdowns
5. **Export**: Save results as a text file

### Supported Languages

```
Python (.py)          C++ (.cpp)           Ruby (.rb)
JavaScript (.js)      Go (.go)             PHP (.php)
Java (.java)          Rust (.rs)           Swift (.swift)
C (.c)                TypeScript (.ts)     Kotlin (.kt)
```

## 🏗️ Architecture

```
ai-code-reviewer/
├── app.py                          # Flask backend server
├── requirements.txt                # Python dependencies
├── analyzer/                       # Code analysis engine
│   ├── __init__.py                # Analysis coordinator
│   ├── quality_checker.py         # Quality issue detection
│   ├── security_checker.py        # Security vulnerability scanning
│   └── performance_checker.py     # Performance issue identification
├── templates/
│   └── index.html                 # Single-page HTML interface
├── static/
│   ├── style.css                  # Modern SaaS-style design system
│   ├── script.js                  # Interactive frontend logic
│   └── favicon.svg                # App icon
└── uploads/                       # Temporary file storage
```

## 🔍 How It Works

### Quality Checker

Detects structural and style issues:

- Functions exceeding 30 lines
- Unused variables and imports
- Poor variable naming conventions
- Lines exceeding 120 characters

### Security Checker

Identifies security vulnerabilities:

- Hardcoded passwords and API keys
- Dangerous function usage (eval, exec, etc.)
- SQL injection patterns
- Unsafe deserialization (pickle)
- OS command injection risks

### Performance Checker

Flags performance bottlenecks:

- Nested loops (O(n²) complexity)
- Inefficient string operations
- Repeated function calls in loops
- Type conversion inefficiencies

### Scoring Algorithm

```
Base Score: 10/10
- CRITICAL issue: -2 points each
- WARNING issue: -1 point each
- SUGGESTION issue: -0.25 points each
- Final score: clamped between 0-10
- Grade: A+ (9.0+), A (8.0+), B (7.0+), C (6.0+), D (5.0+), F (<5.0)
```

## 🎨 Design Highlights

- **Modern SaaS Aesthetic**: Glassmorphism panels with backdrop blur effects
- **Dark/Light Modes**: Automatic theme persistence via localStorage
- **Responsive Breakpoints**: Optimized layouts for 560px (mobile), 768px (tablet), 1024px+ (desktop)
- **Accessible**: Focus states, ARIA labels, semantic HTML5
- **Smooth Animations**: Fade-in cards, progress bars, loading spinners
- **Professional Typography**: Inter font family with fluid scaling

## 🔧 Development

### Running in Debug Mode

```bash
cd ai-code-reviewer
flask run --host 127.0.0.1 --port 5000 --reload
```

### Testing the API

```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -F "code=def hello(): pass"
```

### Health Check

```bash
curl http://127.0.0.1:5000/api/health
```

## 📦 Dependencies

Core packages:

- **Flask** (2.0+) - Web framework
- **Werkzeug** - File handling and security utilities
- **Python AST module** - Code analysis (built-in)

See `requirements.txt` for complete list.

## 🌐 Deployment

For production deployment, consider:

- Use a production WSGI server (Gunicorn, uWSGI)
- Set `DEBUG=False` in Flask
- Deploy behind Nginx or Apache reverse proxy
- Enable HTTPS/SSL certificates
- Configure environment variables for sensitive settings
- Use a cloud platform (Heroku, AWS, DigitalOcean, etc.)

Example Gunicorn launch:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 API Endpoints

### POST `/api/analyze`

Analyze code and return comprehensive results.

**Request:**

```
Content-Type: multipart/form-data
- code (optional): String of code to analyze
- files (optional): Multiple files to analyze
```

**Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "overall_score": 8.5,
    "total_files": 1,
    "total_issues": 2,
    "critical_count": 0,
    "warning_count": 2,
    "suggestion_count": 0,
    "files": {
      "example.py": {
        "filename": "example.py",
        "score": 8.5,
        "total_issues": 2,
        "issues": [
          {
            "type": "Long Function",
            "severity": "WARNING",
            "message": "Function 'process' is 45 lines long",
            "line": 12,
            "file": "example.py"
          }
        ]
      }
    }
  }
}
```

### GET `/api/health`

Health check endpoint.

**Response (200 OK):**

```json
{
  "status": "ok"
}
```

## 🖼️ Screenshots

**Dark Theme - Analysis Results**

- Clean two-column workspace layout
- Real-time score visualization
- Severity-based filtering
- Per-file issue breakdown

**Light Theme - File Upload**

- Professional light background
- Drag-and-drop file upload
- Multiple language badges
- Smart file selection counter

## 🤝 Contributing

Contributions are welcome! Areas for expansion:

- Additional language support (Go, Rust, async patterns)
- More sophisticated rule engines
- Machine learning-based analysis
- Custom rule configuration
- Result persistence and history
- Team collaboration features
- CI/CD integration (GitHub Actions, GitLab CI)

## 📄 License

This project is open source and available under the MIT License.

## 💡 Future Enhancements

- [ ] Database integration for result history
- [ ] User authentication and team accounts
- [ ] Custom analysis rule builder
- [ ] GitHub/GitLab integration for PR reviews
- [ ] API rate limiting and analytics
- [ ] Advanced caching for performance
- [ ] Docker containerization
- [ ] Microservices architecture
- [ ] WebSocket real-time analysis
- [ ] Browser extensions for IDE integration

## 🐛 Issues & Feedback

Found a bug or have a feature request? [Open an issue](https://github.com/YOUR_USERNAME/ai-code-reviewer/issues) on GitHub.

## 📧 Contact

For questions or feedback, reach out via GitHub issues or email.

---

**Built with ❤️ using Flask, Python, and modern web technologies**

_Last updated: March 15, 2026_
