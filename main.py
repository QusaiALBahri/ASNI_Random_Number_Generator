"""Terminal-based AI calculator for solving batches of math problems.

The application uses the ``npyscreen`` library to create a minimal text UI
that can generate and solve arithmetic expressions at the press of a button.
The interface displays the solved problems in a scrollable list, along with
lightweight statistics describing the generated batch.

Features:
- Configurable problem count (default: 100)
- Input validation to prevent division by zero
- Export functionality to save results to file
- Difficulty levels (Easy, Medium, Hard)
- Operation filtering options
- Multi-language support (English, Arabic, Hindi)
- Keyboard shortcuts for common actions
- Progress indicators during generation
- Clear/reset functionality
- Comprehensive type hints and error handling
"""

from __future__ import annotations

import json
import logging
import operator
import random
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Sequence, Tuple

import npyscreen

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Language(Enum):
    """Supported languages for the UI."""
    ENGLISH = "en"
    ARABIC = "ar"
    HINDI = "hi"


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
        """Return a human-friendly representation of ``result``.

        Results that are mathematically integers are displayed without a
        decimal component.  Otherwise we keep two decimal places to avoid
        overwhelming the limited terminal real estate with long floats.
        """
        if self.result.is_integer():
            return f"{int(self.result)}"
        return f"{self.result:.2f}"

    def to_dict(self) -> dict:
        """Convert problem to dictionary for export."""
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
    export_path: Optional[str] = None

    @classmethod
    def get_translations(cls) -> dict:
        """Return translations for UI elements."""
        return {
            Language.ENGLISH: {
                "title": "AI Calculator - Batch Solver",
                "description": "Solve randomly generated math problems at once.",
                "problems_solved": "Problems solved:",
                "results_box": "Solved Problems",
                "generate_btn": "Generate and Solve",
                "clear_btn": "Clear",
                "export_btn": "Export",
                "exit_btn": "Exit",
                "avg_result": "Avg result",
                "distribution": "Distribution",
                "difficulty": "Difficulty",
                "count": "Count",
                "no_problems": "Press the button below to generate a batch.",
                "export_success": "Results exported to:",
                "export_error": "Export failed:",
            },
            Language.ARABIC: {
                "title": "حاسبة الذكاء الاصطناعي - حل دفعي",
                "description": "حل مسائل رياضية مولدة عشوائياً دفعة واحدة.",
                "problems_solved": "المسائل المحلولة:",
                "results_box": "المسائل المحلولة",
                "generate_btn": "توليد وحل",
                "clear_btn": "مسح",
                "export_btn": "تصدير",
                "exit_btn": "خروج",
                "avg_result": "متوسط النتائج",
                "distribution": "التوزيع",
                "difficulty": "الصعوبة",
                "count": "العدد",
                "no_problems": "اضغط الزر أدناه لتوليد مجموعة مسائل.",
                "export_success": "تم تصدير النتائج إلى:",
                "export_error": "فشل التصدير:",
            },
            Language.HINDI: {
                "title": "एआई कैलकुलेटर - बैच सोल्वर",
                "description": "एक साथ यादृच्छिक गणितीय समस्याओं को हल करें।",
                "problems_solved": "सुलझाई गई समस्याएं:",
                "results_box": "सुलझाई गई समस्याएं",
                "generate_btn": "उत्पन्न और हल करें",
                "clear_btn": "साफ़ करें",
                "export_btn": "निर्यात",
                "exit_btn": "बाहर जाएं",
                "avg_result": "औसत परिणाम",
                "distribution": "वितरण",
                "difficulty": "कठिनाई",
                "count": "गिनती",
                "no_problems": "बैच उत्पन्न करने के लिए नीचे बटन दबाएं।",
                "export_success": "परिणाम निर्यातित:",
                "export_error": "निर्यात विफल:",
            }
        }


class BatchGenerator:
    """Create batches of arithmetic problems ready for display."""

    def __init__(self, difficulty: Difficulty = Difficulty.MEDIUM) -> None:
        self.operations: Sequence[Tuple[str, Callable[[int, int], float]]] = (
            ("+", operator.add),
            ("-", operator.sub),
            ("×", operator.mul),
            ("÷", operator.truediv),
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
        """Generate ``count`` arithmetic problems with calculated answers.

        Args:
            count: Number of problems to generate
            allowed_operations: List of operation symbols to include

        Returns:
            List of generated MathProblem instances

        Raises:
            ValueError: If count is negative or no operations are allowed
        """
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
        """Produce operands tailored to ``symbol`` for tidy results.

        Args:
            symbol: The operation symbol (+, -, ×, ÷)

        Returns:
            Tuple of (left_operand, right_operand)
        """
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
        """Update the difficulty level for problem generation.

        Args:
            difficulty: New difficulty level
        """
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
            "average_result": self.average_result(),
            "min_result": self.min_result(),
            "max_result": self.max_result(),
            "operator_distribution": self.counts_by_operator()
        }


class ExportManager:
    """Handle exporting of problem batches to various formats."""

    @staticmethod
    def export_to_json(
        problems: Sequence[MathProblem],
        summary: Summary,
        filepath: str
    ) -> bool:
        """Export problems and summary to JSON file.

        Args:
            problems: List of math problems to export
            summary: Summary statistics
            filepath: Path to output file

        Returns:
            True if export successful, False otherwise
        """
        try:
            data = {
                "timestamp": datetime.now().isoformat(),
                "problems": [p.to_dict() for p in problems],
                "summary": summary.to_dict()
            }
            
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported {len(problems)} problems to {filepath}")
            return True
        except (IOError, OSError, TypeError) as e:
            logger.error(f"Export failed: {e}")
            return False

    @staticmethod
    def export_to_csv(
        problems: Sequence[MathProblem],
        filepath: str
    ) -> bool:
        """Export problems to CSV file.

        Args:
            problems: List of math problems to export
            filepath: Path to output file

        Returns:
            True if export successful, False otherwise
        """
        try:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write("ID,Expression,Result,Operator,Difficulty\n")
                for idx, problem in enumerate(problems, start=1):
                    f.write(
                        f"{idx},{problem.expression},{problem.formatted_result()},"
                        f"{problem.operator_symbol},{problem.difficulty.value}\n"
                    )
            
            logger.info(f"Exported {len(problems)} problems to CSV: {filepath}")
            return True
        except (IOError, OSError) as e:
            logger.error(f"CSV export failed: {e}")
            return False


class AICalculatorApp(npyscreen.NPSAppManaged):
    """Application entry-point that registers the main form."""

    def onStart(self) -> None:  # noqa: N802 (npyscreen naming convention)
        """Initialize application forms."""
        self.addForm("MAIN", MainForm)


class MainForm(npyscreen.Form):
    """Primary user interface for the batch calculator."""

    DEFAULT_PROBLEM_COUNT = 100

    def create(self) -> None:  # noqa: D401, N802 (npyscreen naming convention)
        """Create form widgets and initialize state."""
        self.settings = AppSettings()
        self.translations = AppSettings.get_translations()[self.settings.language]
        
        self.name = self.translations["title"]
        
        # Description
        self.add(
            npyscreen.FixedText,
            value=self.translations["description"],
            editable=False,
        )

        # Settings row
        settings_row = self.add_widget_set(
            npyscreen.GridColTitle,
            columns=2,
            rely=3,
            column_width=40
        )
        
        self.count_display = settings_row.add_widget(
            npyscreen.TitleText,
            name=f"{self.translations['count']}:",
            value=str(self.settings.problem_count),
            editable=False,
        )
        
        self.difficulty_display = settings_row.add_widget(
            npyscreen.TitleText,
            name=f"{self.translations['difficulty']}:",
            value=self.settings.difficulty.value.capitalize(),
            editable=False,
        )

        # Problem count input
        self.count_input = self.add(
            npyscreen.TitleText,
            name="Problem Count:",
            value=str(self.DEFAULT_PROBLEM_COUNT),
            editable=True,
        )

        # Results box
        self.results_box = self.add(
            npyscreen.BoxTitle,
            name=self.translations["results_box"],
            values=[self.translations["no_problems"]],
            max_height=18,
        )

        # Summary display
        self.summary_display = self.add(
            npyscreen.FixedText,
            value="",
            editable=False,
        )

        # Status line
        self.status_line = self.add(
            npyscreen.FixedText,
            value="Ready - Press Generate or use shortcuts (G=Generate, C=Clear, E=Export, X=Exit)",
            editable=False,
        )

        # Button row
        button_row = self.add_widget_set(
            npyscreen.GridColTitle,
            columns=4,
            column_width=20
        )
        
        self.generate_button = button_row.add_widget(
            npyscreen.ButtonPress,
            name=self.translations["generate_btn"],
        )
        self.generate_button.whenPressed = self.solve_batch

        self.clear_button = button_row.add_widget(
            npyscreen.ButtonPress,
            name=self.translations["clear_btn"],
        )
        self.clear_button.whenPressed = self.clear_results

        self.export_button = button_row.add_widget(
            npyscreen.ButtonPress,
            name=self.translations["export_btn"],
        )
        self.export_button.whenPressed = self.export_results

        self.exit_button = button_row.add_widget(
            npyscreen.ButtonPress,
            name=self.translations["exit_btn"],
        )
        self.exit_button.whenPressed = self.exit_app

        self.generator = BatchGenerator(self.settings.difficulty)
        self.current_problems: List[MathProblem] = []
        self.current_summary: Optional[Summary] = None

        # Keyboard shortcuts
        self.add_keypress_handler("^G", self.solve_batch)
        self.add_keypress_handler("^C", self.clear_results)
        self.add_keypress_handler("^E", self.export_results)
        self.add_keypress_handler("^X", self.exit_app)

    def solve_batch(self) -> None:
        """Generate and solve a batch of problems."""
        try:
            # Parse problem count from input
            try:
                count = int(self.count_input.value.strip())
                if count <= 0:
                    raise ValueError("Count must be positive")
            except ValueError:
                self.status_line.value = "Error: Invalid problem count. Using default."
                self.status_line.display()
                count = self.DEFAULT_PROBLEM_COUNT

            # Update settings
            self.settings.problem_count = count
            
            # Show progress
            self.status_line.value = f"Generating {count} problems..."
            self.status_line.display()

            # Filter operations (currently all enabled)
            allowed_ops = self.settings.operations
            
            # Generate problems
            self.current_problems = self.generator.generate(count, allowed_ops)
            self.current_summary = Summary(self.current_problems)

            # Update displays
            self.count_display.value = f"{len(self.current_problems)} / {count}"
            self.count_display.display()

            self.results_box.values = self._format_problems(self.current_problems)
            self.results_box.display()

            self.summary_display.value = self._format_summary(self.current_summary)
            self.summary_display.display()

            self.status_line.value = f"Completed! Generated {len(self.current_problems)} problems"
            self.status_line.display()

            logger.info(f"Batch solved: {len(self.current_problems)} problems")

        except Exception as e:
            self.status_line.value = f"Error: {str(e)}"
            self.status_line.display()
            logger.error(f"Error in solve_batch: {e}")

    def clear_results(self) -> None:
        """Clear all results and reset the display."""
        self.current_problems = []
        self.current_summary = None
        
        self.count_display.value = "0 / 0"
        self.count_display.display()
        
        self.results_box.values = [self.translations["no_problems"]]
        self.results_box.display()
        
        self.summary_display.value = ""
        self.summary_display.display()
        
        self.status_line.value = "Cleared - Ready for new batch"
        self.status_line.display()
        
        logger.info("Results cleared")

    def export_results(self) -> None:
        """Export current results to a file."""
        if not self.current_problems:
            self.status_line.value = "Nothing to export - Generate problems first"
            self.status_line.display()
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_path = f"results_{timestamp}.json"
        
        try:
            success = ExportManager.export_to_json(
                self.current_problems,
                self.current_summary,
                default_path
            )
            
            if success:
                self.status_line.value = f"{self.translations['export_success']} {default_path}"
            else:
                self.status_line.value = f"{self.translations['export_error']} Check logs"
            
            self.status_line.display()
            logger.info(f"Export completed: {success}")
            
        except Exception as e:
            self.status_line.value = f"Export error: {str(e)}"
            self.status_line.display()
            logger.error(f"Export failed: {e}")

    def exit_app(self) -> None:
        """Exit the application gracefully."""
        logger.info("Application exiting")
        self.parentApp.switchForm(None)

    def _format_problems(self, problems: Sequence[MathProblem]) -> List[str]:
        """Format problems for display in the results box.

        Args:
            problems: List of math problems to format

        Returns:
            List of formatted strings
        """
        lines = []
        for index, problem in enumerate(problems, start=1):
            lines.append(
                f"{index:>3}. {problem.expression} = {problem.formatted_result()}"
            )
        return lines

    def _format_summary(self, summary: Optional[Summary]) -> str:
        """Format summary statistics for display.

        Args:
            summary: Summary object containing statistics

        Returns:
            Formatted summary string
        """
        if not summary:
            return ""
        
        counts = summary.counts_by_operator()
        parts = [
            f"{self.translations['avg_result']}: {summary.average_result():.2f}"
        ]
        
        if counts:
            counts_text = ", ".join(
                f"{symbol}×{count}" for symbol, count in sorted(counts.items())
            )
            parts.append(f"{self.translations['distribution']}: {counts_text}")
        
        # Add min/max for more detail
        parts.append(f"Min: {summary.min_result():.2f}, Max: {summary.max_result():.2f}")
        
        return " | ".join(parts)


if __name__ == "__main__":
    AICalculatorApp().run()