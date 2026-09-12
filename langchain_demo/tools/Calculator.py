import abc
import ast
import math
import operator
import re
from typing import Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_UNOPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_FUNCS = {
    "sqrt": math.sqrt,
    "log": math.log,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
}
_NAMES = {"pi": math.pi, "e": math.e}


def safe_eval_math(expr: str):
    """Evaluate a numeric expression. Names and calls outside the allow-list raise."""
    tree = ast.parse(expr, mode="eval")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNOPS:
            return _UNOPS[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
            return _BINOPS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.Name) and node.id in _NAMES:
            return _NAMES[node.id]
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id not in _FUNCS or node.keywords:
                raise ValueError("unsupported call")
            return _FUNCS[node.func.id](*(_eval(arg) for arg in node.args))
        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == "math"
        ):
            if node.attr in _FUNCS:
                return _FUNCS[node.attr]
            if node.attr in _NAMES:
                return _NAMES[node.attr]
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "math"
            and node.func.attr in _FUNCS
            and not node.keywords
        ):
            return _FUNCS[node.func.attr](*(_eval(arg) for arg in node.args))
        raise ValueError("unsupported expression")

    return _eval(tree)


class CalculatorInput(BaseModel):
    calculation: str = Field(description="calculation to perform")


class Calculator(BaseTool, abc.ABC):
    name = "Calculator"
    description = "Useful for when you need to calculate math problems"
    args_schema: Type[BaseModel] = CalculatorInput

    def __init__(self):
        super().__init__()

    def parameter_validation(self, para: str):
        """
        You can write your own parameter validation rules here,
        you can refer to the code given here.
        :param para:
        :return:
        """
        symbols = ["math", "sqrt", "log", "sin", "cos", "tan", "pi"]
        for sym in symbols:
            para = para.replace(sym, "")
        patten = re.compile("[+*/\-%\d()=\s.]{3,}")
        if re.findall(patten, para):
            return True

    def _run(self, calculation: str) -> str:
        calculation = calculation.replace("^", "**")
        if "sqrt" in calculation and "math" not in calculation:
            calculation = calculation.replace("sqrt", "math.sqrt")
        if "log" in calculation and "math" not in calculation:
            calculation = calculation.replace("log", "math.log")
        if "sin" in calculation and "math" not in calculation:
            calculation = calculation.replace("sin", "math.sin")
        if "cos" in calculation and "math" not in calculation:
            calculation = calculation.replace("cos", "math.cos")
        if "tan" in calculation and "math" not in calculation:
            calculation = calculation.replace("tan", "math.tan")
        if "pi" in calculation and "math" not in calculation:
            calculation = calculation.replace("pi", "math.pi")
        if "pI" in calculation and "math" not in calculation:
            calculation = calculation.replace("pI", "math.pi")
        if "PI" in calculation and "math" not in calculation:
            calculation = calculation.replace("PI", "math.pi")
        if "Pi" in calculation and "math" not in calculation:
            calculation = calculation.replace("Pi", "math.pi")
        return safe_eval_math(calculation)
