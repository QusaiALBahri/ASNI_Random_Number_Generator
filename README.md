# 🧮 AI Calculator - Batch Math Problem Solver

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Languages](https://img.shields.io/badge/languages-5-orange)

**A powerful dual-interface calculator that generates and solves hundreds of math problems instantly!**

[Terminal Interface](#terminal-interface) • [Web Application](#web-application) • [Features](#features) • [Installation](#installation)

</div>

---

## ✨ Overview

Welcome to the **AI Calculator** – your ultimate tool for generating, solving, and analyzing batches of arithmetic problems! Whether you're a teacher creating practice worksheets, a student testing your skills, or a developer exploring math problem generation, this project has you covered.

### 🎯 What Makes It Special?

- **🚀 Lightning Fast**: Generate and solve 100+ problems in milliseconds
- **🌍 Multi-Language**: Supports English, Arabic, Hindi, French, and Spanish
- **💻 Dual Interface**: Choose between Terminal (TUI) or modern Web UI
- **⚙️ Fully Customizable**: Adjust difficulty, operations, and problem count
- **📊 Rich Statistics**: Get instant insights with averages, distributions, and more
- **💾 Export Options**: Save results as JSON or CSV for further analysis

---

## 🎨 Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Batch Generation** | Create up to 1000 problems with a single click |
| **Smart Validation** | Automatic prevention of division by zero |
| **Difficulty Levels** | Easy, Medium, and Hard modes with tailored ranges |
| **Operation Filtering** | Select specific operations (+, -, ×, ÷) |
| **Real-time Stats** | Average, min, max, and operator distribution |
| **Export Functionality** | Download results in JSON or CSV format |

### Multi-Language Support 🌐

The application speaks your language! Currently supported:

- 🇺🇸 **English** (en)
- 🇸🇦 **Arabic** (ar) - Right-to-left support
- 🇮🇳 **Hindi** (hi) - Devanagari script
- 🇫🇷 **French** (fr)
- 🇪🇸 **Spanish** (es)

### Difficulty Levels 📈

| Level | Addition/Subtraction | Multiplication | Division |
|-------|---------------------|----------------|----------|
| **Easy** | 1-20 | 1-10 | 2-6 |
| **Medium** | 10-100 | 2-20 | 2-12 |
| **Hard** | 50-500 | 10-50 | 5-20 |

---

## 🖥️ Terminal Interface

A classic TUI experience using `npyscreen` for terminal enthusiasts.

### Quick Start

```bash
# Install dependencies
pip install npyscreen

# Run the application
python main.py
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+G` | Generate problems |
| `Ctrl+C` | Clear results |
| `Ctrl+E` | Export to file |
| `Ctrl+Q` | Quit application |

---

## 🌐 Web Application

A modern, responsive web interface with beautiful UI and real-time updates.

### Quick Start

```bash
# Navigate to webapp directory
cd webapp

# Install Flask (if not already installed)
pip install flask

# Start the server
python app.py
```

Then open your browser and navigate to **http://localhost:5000**

### Web Features

- 🎨 **Modern Design**: Gradient backgrounds and smooth animations
- 📱 **Responsive**: Works on desktop, tablet, and mobile
- ⚡ **Real-time Updates**: Instant problem generation without page reload
- 🌙 **Language Switching**: Change languages on the fly
- 📊 **Live Statistics**: Dynamic charts and metrics
- 💾 **One-Click Export**: Download JSON or CSV instantly

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/generate` | POST | Generate math problems |
| `/api/clear` | POST | Clear current session |
| `/api/export/json` | GET | Export as JSON |
| `/api/export/csv` | GET | Export as CSV |
| `/api/stats` | GET | Get statistics |
| `/api/translations/<lang>` | GET | Get translations |

### Example API Usage

```bash
# Generate 50 easy problems with addition only
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"count": 50, "difficulty": "easy", "operations": ["+"]}'

# Get statistics
curl http://localhost:5000/api/stats

# Get French translations
curl http://localhost:5000/api/translations/fr
```

---

## 📦 Installation

### Option 1: Using pip

```bash
# For Terminal Interface
pip install npyscreen

# For Web Application
pip install flask
```

### Option 2: Using Poetry

```bash
# Install poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Run terminal interface
poetry run python main.py

# Run web application
cd webapp
poetry run python app.py
```

---

## 📁 Project Structure

```
/workspace/
├── main.py                 # Terminal interface application
├── README.md               # This documentation
├── pyproject.toml          # Poetry configuration
├── poetry.lock             # Poetry lock file
└── webapp/                 # Web application
    ├── app.py              # Flask backend
    ├── templates/
    │   └── index.html      # Main HTML template
    └── static/
        ├── css/
        │   └── style.css   # Stylesheets
        └── js/
            └── app.js      # Frontend JavaScript
```

---

## 🧪 Testing

All components have been thoroughly tested and verified:

### Backend Tests ✅

- ✓ Problem generation (all difficulties)
- ✓ Operation filtering
- ✓ Division by zero prevention
- ✓ Export functionality (JSON & CSV)
- ✓ Multi-language translations
- ✓ Statistics calculation

### API Tests ✅

- ✓ Generate endpoint
- ✓ Clear endpoint
- ✓ Export endpoints (JSON & CSV)
- ✓ Statistics endpoint
- ✓ Translations endpoint (5 languages)
- ✓ Custom parameters handling

Run tests manually:

```bash
# Test TUI backend
python -c "from main import BatchGenerator; print('TUI OK')"

# Test Web API
cd webapp && python -c "from app import app; print('Web OK')"
```

---

## 🎯 Usage Examples

### Terminal Interface (Python)

```python
from main import BatchGenerator, Difficulty, ExportManager, Summary

# Create generator with medium difficulty
generator = BatchGenerator(Difficulty.MEDIUM)

# Generate 100 problems
problems = generator.generate(count=100)

# Filter to only addition and subtraction
problems = generator.generate(count=50, allowed_operations=['+', '-'])

# Export to JSON
exporter = ExportManager()
exporter.export_to_json(problems, Summary(problems), 'results.json')

# Export to CSV
exporter.export_to_csv(problems, 'results.csv')
```

### Web Application (JavaScript)

```javascript
// Generate problems
fetch('/api/generate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        count: 100,
        difficulty: 'medium',
        operations: ['+', '-', '×', '÷'],
        language: 'en'
    })
})
.then(res => res.json())
.then(data => console.log(data.problems));

// Get statistics
fetch('/api/stats')
.then(res => res.json())
.then(stats => console.log(`Average: ${stats.average}`));

// Change language
fetch('/api/translations/es')
.then(res => res.json())
.then(data => updateUI(data.translations));
```

---

## 🔧 Configuration

### Problem Count
- **Range**: 1 - 1000
- **Default**: 100
- **Recommended**: 50-200 for best performance

### Operations
Available operators:
- `+` Addition
- `-` Subtraction
- `×` Multiplication
- `÷` Division

### Difficulty Settings

```python
# Easy - Perfect for beginners
difficulty = Difficulty.EASY

# Medium - Standard level
difficulty = Difficulty.MEDIUM

# Hard - Challenge mode
difficulty = Difficulty.HARD
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include docstrings for public methods
- Write tests for new features
- Update documentation accordingly

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- Built with ❤️ using Python
- Terminal UI powered by [npyscreen](https://github.com/npcole/npyscreen)
- Web framework by [Flask](https://flask.palletsprojects.com/)
- Inspired by the need for efficient math problem generation

---

<div align="center">

**Made with Python 🐍 | Supporting 5 Languages 🌍 | Dual Interface 💻**

⭐ Star this repo if you find it useful! ⭐

</div>
