from __future__ import annotations

import ast
import operator
from typing import Any

from plugins.base_plugin import Plugin
from plugins.plugin_manifest import PluginManifest


class CalculatorPlugin(BasePlugin):
    """
    Built-in calculator plugin.

    Supports safe arithmetic evaluation using Python's AST.

    Examples
    --------
    2 + 2
    10 * (5 + 3)
    25 / 5
    2 ** 8
    10 % 3
    """

    def __init__(
       self,
    ) -> None:

        super().__init__()

        self.manifest = PluginManifest(
            name="calculator",
            version="1.0.0",
            author="Cipher",
            description="Built-in calculator plugin.",
        )

        self._operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def on_load(self) -> None:
        pass

    def on_unload(self) -> None:
        pass

    # --------------------------------------------------
    # Commands
    # --------------------------------------------------

    def can_handle(
        self,
        command: str,
    ) -> bool:

        command = command.strip().lower()

        return (
            command.startswith("calculate ")
            or command.startswith("calc ")
            or command.startswith("math ")
        )

    def handle(
        self,
        command: str,
    ) -> str:

        expression = (
            command.replace("calculate", "", 1)
            .replace("calc", "", 1)
            .replace("math", "", 1)
            .strip()
        )

        if not expression:
            return "Please provide an expression."

        try:

            result = self.evaluate(expression)

            return str(result)

        except Exception as e:

            return f"Calculation error: {e}"

    # --------------------------------------------------
    # Calculator
    # --------------------------------------------------

    def evaluate(
        self,
        expression: str,
    ) -> Any:

        tree = ast.parse(
            expression,
            mode="eval",
        )

        return self._eval(tree.body)

    def _eval(
        self,
        node: ast.AST,
    ) -> Any:

        if isinstance(node, ast.Constant):

            if isinstance(node.value, (int, float)):
                return node.value

            raise TypeError("Unsupported constant.")

        if isinstance(node, ast.Num):
            return node.n

        if isinstance(node, ast.BinOp):

            left = self._eval(node.left)
            right = self._eval(node.right)

            op = self._operators.get(type(node.op))

            if op is None:
                raise TypeError("Unsupported operator.")

            return op(left, right)

        if isinstance(node, ast.UnaryOp):

            operand = self._eval(node.operand)

            op = self._operators.get(type(node.op))

            if op is None:
                raise TypeError("Unsupported operator.")

            return op(operand)

        raise TypeError("Unsupported expression.")