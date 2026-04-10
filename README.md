# ANSI-based AI Calculator (TUI & Web App)

## Description

### English
This repository contains an ANSI-powered AI calculator implemented in Python with **dual interfaces**:
1. **Terminal User Interface (TUI)** - Built with the `npyscreen` library for terminal-based operation
2. **Modern Web Application** - Built with Flask for browser-based access with a beautiful responsive UI

Both interfaces generate and solve arithmetic problems at the press of a button, with full multi-language support and export capabilities.

**Features:**
- **Dual GUI Support**: Terminal (TUI) and Modern Web Interface
- Configurable problem count (default: 100, max: 1000)
- Input validation to prevent division by zero
- Export functionality to save results to JSON or CSV files
- Difficulty levels (Easy, Medium, Hard)
- Operation filtering options (Addition, Subtraction, Multiplication, Division)
- **Multi-language support** (English, Arabic, Hindi, French, Spanish)
- Keyboard shortcuts for common actions
- Progress indicators during generation
- Clear/reset functionality
- Comprehensive type hints and error handling
- Logging support
- Responsive design for mobile and desktop (Web App)
- Real-time statistics display

### Arabic
يحتوي هذا المستودع على حاسبة تعتمد على الذكاء الاصطناعي ومبنية باستخدام ANSI في الطرفية. تُولِّد الواجهة النصية (باستخدام مكتبة `npyscreen`) مسائل حسابية وتحلها تلقائياً بضغطة زر، ثم تعرض الحلول والإحصاءات داخل الطرفية لاستكشاف المجموعة الناتجة.

**المميزات:**
- عدد مسائل قابل للتكوين (الافتراضي: 100)
- التحقق من المدخلات لمنع القسمة على صفر
- وظيفة التصدير لحفظ النتائج في ملفات JSON أو CSV
- مستويات الصعوبة (سهل، متوسط، صعب)
- خيارات تصفية العمليات
- دعم متعدد اللغات (الإنجليزية، العربية، الهندية)
- اختصارات لوحة المفاتيح للإجراءات الشائعة
- مؤشرات التقدم أثناء التوليد
- وظيفة المسح/إعادة التعيين
- تلميحات شاملة للنوع ومعالجة الأخطاء
- دعم التسجيل

### Hindi
यह रिपॉजिटरी एक ANSI आधारित एआई कैलकुलेटर प्रदान करती है। `npyscreen` लाइब्रेरी से बना यह टर्मिनल यूज़र इंटरफ़ेस गणितीय समस्याएँ तैयार करता है और उन्हें हल कर देता है। समाधान और त्वरित सांख्यिकीय जानकारी उसी टर्मिनल में दिखाई जाती हैं ताकि आप स्वतः उत्पन्न परिणामों को आसानी से देख सकें।

**विशेषताएँ:**
- विन्यास योग्य समस्या संख्या (डिफ़ॉल्ट: 100)
- शून्य से विभाजन को रोकने के लिए इनपुट सत्यापन
- JSON या CSV फ़ाइलों में परिणाम सहेजने के लिए निर्यात कार्य
- कठिनाई स्तर (आसान, मध्यम, कठिन)
- ऑपरेशन फ़िल्टरिंग विकल्प
- बहु-भाषा समर्थन (अंग्रेज़ी, अरबी, हिंदी)
- सामान्य कार्यों के लिए कीबोर्ड शॉर्टकट
- जनरेशन के दौरान प्रगति संकेतक
- स्पष्ट/रीसेट कार्यक्षमता
- व्यापक प्रकार संकेत और त्रुटि हैंडलिंग
- लॉगिंग समर्थन

## How to Run

### Terminal Interface (TUI)

1. Ensure you have Python installed on your system (Python 3.10 or newer).
2. Install the dependencies (the project uses [Poetry](https://python-poetry.org/) for dependency management).
   ```bash
   poetry install
   ```
   Or using pip:
   ```bash
   pip install npyscreen
   ```
3. Run the terminal application.
   ```bash
   poetry run python main.py
   ```
   Or:
   ```bash
   python main.py
   ```

### Web Application

1. Install Flask dependency:
   ```bash
   pip install flask
   ```
   Or with Poetry:
   ```bash
   poetry install
   ```

2. Navigate to the webapp directory and run:
   ```bash
   cd webapp
   python app.py
   ```

3. Open your browser and go to:
   ```
   http://localhost:5000
   ```

## Usage

### Terminal Interface (TUI)

#### Basic Usage
- Press the "Generate and Solve" button or use **Ctrl+G** to generate and solve problems
- Enter a custom problem count in the "Problem Count" field before generating
- Use **Ctrl+C** to clear results
- Use **Ctrl+E** to export results to a JSON file
- Use **Ctrl+X** to exit the application

#### Keyboard Shortcuts (TUI)
| Shortcut | Action |
|----------|--------|
| Ctrl+G   | Generate and solve problems |
| Ctrl+C   | Clear current results |
| Ctrl+E   | Export results to JSON |
| Ctrl+X   | Exit application |

### Web Application

#### Basic Usage
1. Select your preferred language from the dropdown (supports English, Arabic, Hindi, French, Spanish)
2. Choose difficulty level (Easy, Medium, Hard)
3. Set the number of problems to generate (1-1000)
4. Select which operations to include (Addition, Subtraction, Multiplication, Division)
5. Click "Generate & Solve" or press **Ctrl+G**
6. View results and statistics in real-time
7. Export results as JSON or CSV using the export buttons

#### Keyboard Shortcuts (Web)
| Shortcut | Action |
|----------|--------|
| Ctrl+G / Cmd+G | Generate and solve problems |
| Ctrl+C / Cmd+C | Clear current results |
| Ctrl+E / Cmd+E | Export results to JSON |

#### Features
- **Language Switching**: Change UI language instantly without page reload
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Statistics**: View average, min, max results and operator distribution
- **Export Options**: Download results as JSON (with full metadata) or CSV (for spreadsheet import)
- **Visual Feedback**: Loading indicators and status messages

### Features in Detail

#### Configurable Problem Count
You can specify any positive number of problems to generate. Simply enter the desired count in the "Problem Count" field before clicking Generate.

#### Difficulty Levels
The application supports three difficulty levels that affect the range of operands:
- **Easy**: Smaller numbers (1-20 for addition/subtraction, 1-10 for multiplication, 2-6 for division)
- **Medium**: Moderate numbers (10-100 for addition/subtraction, 2-20 for multiplication, 2-12 for division)
- **Hard**: Larger numbers (50-500 for addition/subtraction, 10-50 for multiplication, 5-20 for division)

#### Export Functionality
Results can be exported to JSON format with a timestamp. The export includes:
- All generated problems with expressions and solutions
- Summary statistics (average, min, max results)
- Operator distribution
- Generation timestamp

#### Input Validation
The application validates inputs to prevent errors:
- Negative or zero problem counts are rejected
- Division by zero is prevented through careful operand generation
- Invalid inputs display helpful error messages

## Project Structure

```
/workspace/
├── main.py              # Terminal UI application (TUI)
├── webapp/
│   ├── app.py           # Flask web application
│   ├── templates/
│   │   └── index.html   # Main HTML template
│   └── static/
│       ├── css/
│       │   └── style.css    # Modern responsive styles
│       └── js/
│           └── app.js       # Client-side JavaScript
├── pyproject.toml       # Poetry configuration and dependencies
├── README.md            # This file
└── poetry.lock          # Locked dependency versions
```

## Configuration

Edit `pyproject.toml` to customize:
- Python version requirements
- Dependencies
- Code quality tools (Pyright, Ruff)

## Error Handling

The application includes comprehensive error handling:
- Logging for debugging and monitoring
- User-friendly error messages in the status line
- Graceful degradation when operations fail

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.
