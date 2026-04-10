"""Web-based AI Calculator with Multi-GUI and Multi-language Support.

This module provides a Flask web application that serves as a modern
web interface for the batch math problem generator and solver.
It supports multiple languages, difficulty levels, and export options.
"""

from __future__ import annotations

import json
import logging
import os
import random
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', template_folder='templates')


class Language(Enum):
    """Supported languages for the UI."""
    ENGLISH = "en"
    ARABIC = "ar"
    HINDI = "hi"
    FRENCH = "fr"
    SPANISH = "es"


class Difficulty(Enum):
    """Difficulty levels for problem generation."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass(frozen=True)
class MathProblem:
    """Representation of a single arithmetic problem and its solution."""

    expression: str
    result: float
    operator_symbol: str
    difficulty: Difficulty = Difficulty.MEDIUM
    left_operand: int = 0
    right_operand: int = 0

    def formatted_result(self) -> str:
        """Return a human-friendly representation of result."""
        if self.result.is_integer():
            return f"{int(self.result)}"
        return f"{self.result:.2f}"

    def to_dict(self) -> dict:
        """Convert problem to dictionary for API responses."""
        return {
            "expression": self.expression,
            "result": self.result,
            "formatted_result": self.formatted_result(),
            "operator": self.operator_symbol,
            "difficulty": self.difficulty.value,
            "left_operand": self.left_operand,
            "right_operand": self.right_operand
        }


@dataclass
class AppSettings:
    """Application configuration settings."""
    problem_count: int = 100
    language: Language = Language.ENGLISH
    difficulty: Difficulty = Difficulty.MEDIUM
    operations: List[str] = field(default_factory=lambda: ["+", "-", "×", "÷"])
    
    @classmethod
    def get_translations(cls) -> dict:
        """Return translations for UI elements."""
        return {
            Language.ENGLISH: {
                "title": "AI Calculator - Batch Solver",
                "subtitle": "Solve randomly generated math problems at once",
                "generate_btn": "Generate & Solve",
                "clear_btn": "Clear",
                "export_json": "Export JSON",
                "export_csv": "Export CSV",
                "problem_count": "Problem Count",
                "difficulty": "Difficulty",
                "operations": "Operations",
                "language": "Language",
                "results": "Results",
                "statistics": "Statistics",
                "total_problems": "Total Problems",
                "average_result": "Average Result",
                "min_result": "Minimum",
                "max_result": "Maximum",
                "distribution": "Distribution",
                "no_problems": "Press Generate to create math problems",
                "success": "Successfully generated {count} problems",
                "error": "Error: {message}",
                "addition": "Addition (+)",
                "subtraction": "Subtraction (-)",
                "multiplication": "Multiplication (×)",
                "division": "Division (÷)",
            },
            Language.ARABIC: {
                "title": "حاسبة الذكاء الاصطناعي - حل دفعي",
                "subtitle": "حل مسائل رياضية مولدة عشوائياً دفعة واحدة",
                "generate_btn": "توليد وحل",
                "clear_btn": "مسح",
                "export_json": "تصدير JSON",
                "export_csv": "تصدير CSV",
                "problem_count": "عدد المسائل",
                "difficulty": "الصعوبة",
                "operations": "العمليات",
                "language": "اللغة",
                "results": "النتائج",
                "statistics": "الإحصائيات",
                "total_problems": "إجمالي المسائل",
                "average_result": "متوسط النتائج",
                "min_result": "الحد الأدنى",
                "max_result": "الحد الأقصى",
                "distribution": "التوزيع",
                "no_problems": "اضغط توليد لإنشاء مسائل رياضية",
                "success": "تم توليد {count} مسألة بنجاح",
                "error": "خطأ: {message}",
                "addition": "الجمع (+)",
                "subtraction": "الطرح (-)",
                "multiplication": "الضرب (×)",
                "division": "القسمة (÷)",
            },
            Language.HINDI: {
                "title": "एआई कैलकुलेटर - बैच सोल्वर",
                "subtitle": "एक साथ यादृच्छिक गणितीय समस्याओं को हल करें",
                "generate_btn": "उत्पन्न और हल करें",
                "clear_btn": "साफ़ करें",
                "export_json": "JSON निर्यात",
                "export_csv": "CSV निर्यात",
                "problem_count": "समस्या संख्या",
                "difficulty": "कठिनाई",
                "operations": "संचालन",
                "language": "भाषा",
                "results": "परिणाम",
                "statistics": "आंकड़े",
                "total_problems": "कुल समस्याएं",
                "average_result": "औसत परिणाम",
                "min_result": "न्यूनतम",
                "max_result": "अधिकतम",
                "distribution": "वितरण",
                "no_problems": "गणितीय समस्याएं बनाने के लिए उत्पन्न दबाएं",
                "success": "{count} समस्याएं सफलतापूर्वक उत्पन्न",
                "error": "त्रुटि: {message}",
                "addition": "जोड़ (+)",
                "subtraction": "घटाव (-)",
                "multiplication": "गुणा (×)",
                "division": "विभाजन (÷)",
            },
            Language.FRENCH: {
                "title": "Calculatrice IA - Résolveur par lots",
                "subtitle": "Résoudre des problèmes mathématiques générés aléatoirement",
                "generate_btn": "Générer et résoudre",
                "clear_btn": "Effacer",
                "export_json": "Exporter JSON",
                "export_csv": "Exporter CSV",
                "problem_count": "Nombre de problèmes",
                "difficulty": "Difficulté",
                "operations": "Opérations",
                "language": "Langue",
                "results": "Résultats",
                "statistics": "Statistiques",
                "total_problems": "Total des problèmes",
                "average_result": "Résultat moyen",
                "min_result": "Minimum",
                "max_result": "Maximum",
                "distribution": "Distribution",
                "no_problems": "Appuyez sur Générer pour créer des problèmes",
                "success": "{count} problèmes générés avec succès",
                "error": "Erreur: {message}",
                "addition": "Addition (+)",
                "subtraction": "Soustraction (-)",
                "multiplication": "Multiplication (×)",
                "division": "Division (÷)",
            },
            Language.SPANISH: {
                "title": "Calculadora IA - Solucionador por lotes",
                "subtitle": "Resolver problemas matemáticos generados aleatoriamente",
                "generate_btn": "Generar y resolver",
                "clear_btn": "Limpiar",
                "export_json": "Exportar JSON",
                "export_csv": "Exportar CSV",
                "problem_count": "Cantidad de problemas",
                "difficulty": "Dificultad",
                "operations": "Operaciones",
                "language": "Idioma",
                "results": "Resultados",
                "statistics": "Estadísticas",
                "total_problems": "Total de problemas",
                "average_result": "Resultado promedio",
                "min_result": "Mínimo",
                "max_result": "Máximo",
                "distribution": "Distribución",
                "no_problems": "Presione Generar para crear problemas",
                "success": "{count} problemas generados exitosamente",
                "error": "Error: {message}",
                "addition": "Suma (+)",
                "subtraction": "Resta (-)",
                "multiplication": "Multiplicación (×)",
                "division": "División (÷)",
            }
        }


class BatchGenerator:
    """Create batches of arithmetic problems ready for display."""

    def __init__(self, difficulty: Difficulty = Difficulty.MEDIUM) -> None:
        self.operations: Sequence[Tuple[str, Callable[[int, int], float]]] = (
            ("+", lambda x, y: x + y),
            ("-", lambda x, y: x - y),
            ("×", lambda x, y: x * y),
            ("÷", lambda x, y: x / y if y != 0 else float('inf')),
        )
        self.difficulty = difficulty
        self._operand_ranges = {
            Difficulty.EASY: {"add_sub": (1, 20), "mul": (1, 10), "div": (2, 6)},
            Difficulty.MEDIUM: {"add_sub": (10, 100), "mul": (2, 20), "div": (2, 12)},
            Difficulty.HARD: {"add_sub": (50, 500), "mul": (10, 50), "div": (5, 20)},
        }

    def generate(
        self,
        count: int = 100,
        allowed_operations: Optional[List[str]] = None
    ) -> List[MathProblem]:
        """Generate count arithmetic problems with calculated answers."""
        if count < 0:
            raise ValueError(f"Problem count cannot be negative: {count}")
        if count == 0:
            return []

        ops = self.operations
        if allowed_operations:
            ops = tuple(op for op in self.operations if op[0] in allowed_operations)
            if not ops:
                raise ValueError("No valid operations selected")

        problems: List[MathProblem] = []
        for _ in range(count):
            symbol, func = random.choice(ops)
            left, right = self._generate_operands(symbol)
            
            # Validate division to prevent division by zero
            if symbol == "÷" and right == 0:
                logger.warning("Attempted division by zero, regenerating operands")
                left, right = self._generate_operands(symbol)
            
            try:
                result = func(left, right)
                if result == float('inf'):
                    continue
            except ZeroDivisionError as e:
                logger.error(f"Division by zero occurred: {e}")
                continue

            problems.append(
                MathProblem(
                    expression=f"{left} {symbol} {right}",
                    result=result,
                    operator_symbol=symbol,
                    difficulty=self.difficulty,
                    left_operand=left,
                    right_operand=right,
                )
            )
        
        logger.info(f"Generated {len(problems)} problems with difficulty {self.difficulty.value}")
        return problems

    def _generate_operands(self, symbol: str) -> Tuple[int, int]:
        """Produce operands tailored to symbol for tidy results."""
        ranges = self._operand_ranges[self.difficulty]

        if symbol == "÷":
            max_divisor = ranges["div"][1]
            divisor = random.randint(max(2, ranges["div"][0]), max_divisor)
            quotient = random.randint(max(2, ranges["div"][0]), max_divisor)
            dividend = divisor * quotient
            return dividend, divisor
        
        if symbol == "×":
            return (
                random.randint(*ranges["mul"]),
                random.randint(max(2, ranges["mul"][0]), ranges["mul"][1])
            )
        
        if symbol == "-":
            min_val, max_val = ranges["add_sub"]
            left = random.randint(min_val, max_val)
            right = random.randint(max(1, min_val // 2), max_val // 2)
            if right > left:
                left, right = right, left
            return left, right
        
        # Addition
        min_val, max_val = ranges["add_sub"]
        return random.randint(min_val, max_val), random.randint(max(1, min_val // 2), max_val // 2)

    def set_difficulty(self, difficulty: Difficulty) -> None:
        """Update the difficulty level for problem generation."""
        self.difficulty = difficulty
        logger.info(f"Difficulty changed to {difficulty.value}")


class Summary:
    """Compute quick stats over generated problems."""

    def __init__(self, problems: Iterable[MathProblem]):
        self.problems = list(problems)

    def counts_by_operator(self) -> dict[str, int]:
        """Count occurrences of each operator type."""
        counts: dict[str, int] = {}
        for problem in self.problems:
            counts[problem.operator_symbol] = counts.get(problem.operator_symbol, 0) + 1
        return counts

    def average_result(self) -> float:
        """Calculate the average result across all problems."""
        if not self.problems:
            return 0.0
        return sum(problem.result for problem in self.problems) / len(self.problems)

    def min_result(self) -> float:
        """Find the minimum result value."""
        if not self.problems:
            return 0.0
        return min(problem.result for problem in self.problems)

    def max_result(self) -> float:
        """Find the maximum result value."""
        if not self.problems:
            return 0.0
        return max(problem.result for problem in self.problems)

    def to_dict(self) -> dict:
        """Convert summary statistics to dictionary."""
        return {
            "total_problems": len(self.problems),
            "average_result": round(self.average_result(), 2),
            "min_result": round(self.min_result(), 2),
            "max_result": round(self.max_result(), 2),
            "operator_distribution": self.counts_by_operator()
        }


class ExportManager:
    """Handle exporting of problem batches to various formats."""

    @staticmethod
    def export_to_json(
        problems: Sequence[MathProblem],
        summary: Summary
    ) -> str:
        """Export problems and summary to JSON string."""
        data = {
            "timestamp": datetime.now().isoformat(),
            "problems": [p.to_dict() for p in problems],
            "summary": summary.to_dict()
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def export_to_csv(problems: Sequence[MathProblem]) -> str:
        """Export problems to CSV string."""
        lines = ["ID,Expression,Result,Operator,Difficulty"]
        for idx, problem in enumerate(problems, start=1):
            lines.append(
                f"{idx},{problem.expression},{problem.formatted_result()},"
                f"{problem.operator_symbol},{problem.difficulty.value}"
            )
        return "\n".join(lines)


# Global storage for current session (in production, use proper session management)
current_session = {
    "problems": [],
    "summary": None,
    "settings": AppSettings()
}


@app.route('/')
def index():
    """Serve the main application page."""
    translations = AppSettings.get_translations()[Language.ENGLISH]
    return render_template('index.html', translations=translations, languages=Language)


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint to generate math problems."""
    try:
        data = request.get_json() or {}
        
        # Parse parameters
        count = int(data.get('count', 100))
        difficulty_str = data.get('difficulty', 'medium')
        operations = data.get('operations', ['+', '-', '×', '÷'])
        language_str = data.get('language', 'en')
        
        # Validate
        if count <= 0 or count > 1000:
            return jsonify({"error": "Count must be between 1 and 1000"}), 400
        
        try:
            difficulty = Difficulty(difficulty_str)
        except ValueError:
            return jsonify({"error": "Invalid difficulty level"}), 400
        
        try:
            language = Language(language_str)
        except ValueError:
            language = Language.ENGLISH
        
        # Generate problems
        generator = BatchGenerator(difficulty)
        problems = generator.generate(count, operations)
        summary = Summary(problems)
        
        # Store in session
        current_session["problems"] = problems
        current_session["summary"] = summary
        current_session["settings"] = AppSettings(
            problem_count=count,
            language=language,
            difficulty=difficulty,
            operations=operations
        )
        
        # Return results
        translations = AppSettings.get_translations()[language]
        return jsonify({
            "success": True,
            "problems": [p.to_dict() for p in problems],
            "summary": summary.to_dict(),
            "message": translations["success"].format(count=len(problems))
        })
        
    except Exception as e:
        logger.error(f"Generation error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/clear', methods=['POST'])
def api_clear():
    """API endpoint to clear current results."""
    current_session["problems"] = []
    current_session["summary"] = None
    return jsonify({"success": True, "message": "Results cleared"})


@app.route('/api/export/json', methods=['GET'])
def api_export_json():
    """API endpoint to export results as JSON."""
    if not current_session["problems"]:
        return jsonify({"error": "No results to export"}), 400
    
    json_data = ExportManager.export_to_json(
        current_session["problems"],
        current_session["summary"]
    )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    response = app.make_response(json_data)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = f'attachment; filename=results_{timestamp}.json'
    return response


@app.route('/api/export/csv', methods=['GET'])
def api_export_csv():
    """API endpoint to export results as CSV."""
    if not current_session["problems"]:
        return jsonify({"error": "No results to export"}), 400
    
    csv_data = ExportManager.export_to_csv(current_session["problems"])
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    response = app.make_response(csv_data)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=results_{timestamp}.csv'
    return response


@app.route('/api/translations/<lang_code>', methods=['GET'])
def api_get_translations(lang_code):
    """API endpoint to get translations for a specific language."""
    try:
        language = Language(lang_code)
        translations = AppSettings.get_translations()[language]
        return jsonify({"success": True, "translations": translations})
    except ValueError:
        return jsonify({"error": "Invalid language code"}), 400


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
