"""Terminal-based AI calculator for solving batches of math problems.

The application uses the ``npyscreen`` library to create a minimal text UI
that can generate and solve one hundred arithmetic expressions at the press of
a button.  The interface displays the solved problems in a scrollable list,
along with lightweight statistics describing the generated batch.
"""

from __future__ import annotations

import operator
import random
from dataclasses import dataclass
from typing import Callable, Iterable, List, Sequence

import npyscreen


@dataclass(frozen=True)
class MathProblem:
    """Representation of a single arithmetic problem and its solution."""

    expression: str
    result: float
    operator_symbol: str

    def formatted_result(self) -> str:
        """Return a human-friendly representation of ``result``.

        Results that are mathematically integers are displayed without a
        decimal component.  Otherwise we keep two decimal places to avoid
        overwhelming the limited terminal real estate with long floats.
        """

        if self.result.is_integer():
            return f"{int(self.result)}"
        return f"{self.result:.2f}"


class BatchGenerator:
    """Create batches of arithmetic problems ready for display."""

    def __init__(self) -> None:
        self.operations: Sequence[tuple[str, Callable[[int, int], float]]] = (
            ("+", operator.add),
            ("-", operator.sub),
            ("×", operator.mul),
            ("÷", operator.truediv),
        )

    def generate(self, count: int = 100) -> List[MathProblem]:
        """Generate ``count`` arithmetic problems with calculated answers."""

        problems: List[MathProblem] = []
        for _ in range(count):
            symbol, func = random.choice(self.operations)
            left, right = self._generate_operands(symbol)
            result = func(left, right)
            problems.append(
                MathProblem(
                    expression=f"{left} {symbol} {right}",
                    result=result,
                    operator_symbol=symbol,
                )
            )
        return problems

    def _generate_operands(self, symbol: str) -> tuple[int, int]:
        """Produce operands tailored to ``symbol`` for tidy results."""

        if symbol == "÷":
            divisor = random.randint(2, 12)
            quotient = random.randint(2, 12)
            dividend = divisor * quotient
            return dividend, divisor
        if symbol == "×":
            return random.randint(2, 20), random.randint(2, 12)
        if symbol == "-":
            left = random.randint(20, 199)
            right = random.randint(1, 99)
            if right > left:
                left, right = right, left
            return left, right
        return random.randint(10, 199), random.randint(1, 99)


class Summary:
    """Compute quick stats over generated problems."""

    def __init__(self, problems: Iterable[MathProblem]):
        self.problems = list(problems)

    def counts_by_operator(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for problem in self.problems:
            counts[problem.operator_symbol] = counts.get(problem.operator_symbol, 0) + 1
        return counts

    def average_result(self) -> float:
        if not self.problems:
            return 0.0
        return sum(problem.result for problem in self.problems) / len(self.problems)


class AICalculatorApp(npyscreen.NPSAppManaged):
    """Application entry-point that registers the main form."""

    def onStart(self) -> None:  # noqa: N802 (npyscreen naming convention)
        self.addForm("MAIN", MainForm)


class MainForm(npyscreen.Form):
    """Primary user interface for the batch calculator."""

    DEFAULT_PROBLEM_COUNT = 100

    def create(self) -> None:  # noqa: D401, N802 (npyscreen naming convention)
        self.name = "AI Calculator - Batch Solver"
        self.add(
            npyscreen.FixedText,
            value="Solve 100 randomly generated math problems at once.",
            editable=False,
        )

        self.counter_display = self.add(
            npyscreen.TitleText,
            name="Problems solved:",
            value="0 / 0",
            editable=False,
        )

        self.results_box = self.add(
            npyscreen.BoxTitle,
            name="Solved Problems",
            values=["Press the button below to generate a batch."],
            max_height=18,
        )

        self.summary_display = self.add(
            npyscreen.FixedText,
            value="",
            editable=False,
        )

        self.generate_button = self.add(
            npyscreen.ButtonPress,
            name="Generate and Solve 100 Problems",
        )
        self.generate_button.whenPressed = self.solve_batch

        self.generator = BatchGenerator()

    def solve_batch(self) -> None:
        problems = self.generator.generate(self.DEFAULT_PROBLEM_COUNT)
        summary = Summary(problems)

        self.counter_display.value = f"{len(problems)} / {self.DEFAULT_PROBLEM_COUNT}"
        self.counter_display.display()

        self.results_box.values = self._format_problems(problems)
        self.results_box.display()

        self.summary_display.value = self._format_summary(summary)
        self.summary_display.display()

    def _format_problems(self, problems: Sequence[MathProblem]) -> List[str]:
        lines = []
        for index, problem in enumerate(problems, start=1):
            lines.append(f"{index:>3}. {problem.expression} = {problem.formatted_result()}")
        return lines

    def _format_summary(self, summary: Summary) -> str:
        counts = summary.counts_by_operator()
        parts = [f"Avg result: {summary.average_result():.2f}"]
        if counts:
            counts_text = ", ".join(
                f"{symbol}×{count}" for symbol, count in sorted(counts.items())
            )
            parts.append(f"Distribution: {counts_text}")
        return " | ".join(parts)


if __name__ == "__main__":
    AICalculatorApp().run()