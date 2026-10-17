"""Scholarship eligibility screening and result management."""

import ast
import json
import operator

results = {}
MERIT_FORMULA = "gpa * 10 + credits * 2"
INCOME_LIMIT = 800000
CUTOFF = 85

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate_merit_score(gpa, credit_count):
    """Calculate a merit score using a safe mathematical formula."""
    formula_tree = ast.parse(MERIT_FORMULA, mode="eval")

    def calculate(node):
        if isinstance(node, ast.Expression):
            return calculate(node.body)

        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Only numeric constants are allowed.")
            return node.value

        if isinstance(node, ast.Name):
            variables = {"gpa": gpa, "credits": credit_count}
            if node.id not in variables:
                raise ValueError("Formula contains an unknown variable.")
            return variables[node.id]

        if isinstance(node, ast.BinOp):
            operation = OPERATORS.get(type(node.op))
            if operation not in (
                operator.add,
                operator.sub,
                operator.mul,
                operator.truediv,
                operator.floordiv,
                operator.mod,
                operator.pow,
            ):
                raise ValueError("Unsupported mathematical operation.")

            left = calculate(node.left)
            right = calculate(node.right)

            if isinstance(node.op, ast.Pow):
                if abs(right) > 10 or abs(left) > 1000000:
                    raise ValueError("Formula exponent is too large.")

            result = operation(left, right)

            if isinstance(result, complex) or not isinstance(
                result, (int, float)
            ):
                raise ValueError("Formula must produce a real number.")

            if abs(result) > 1e100:
                raise ValueError("Formula result is too large.")

            return result

        if isinstance(node, ast.UnaryOp):
            operation = OPERATORS.get(type(node.op))
            if operation not in (operator.pos, operator.neg):
                raise ValueError("Unsupported unary operation.")
            return operation(calculate(node.operand))

        raise ValueError("Formula contains an unsupported operation.")

    return calculate(formula_tree)


def evaluate_applicant(student_id, test_scores, logs=None):
    """Calculate an applicant's score and determine eligibility."""
    if logs is None:
        logs = []

    gpa = test_scores["gpa"]
    credit_count = test_scores.get("credits", 0)
    income = test_scores.get("income", 0)

    if not isinstance(gpa, (int, float)) or isinstance(gpa, bool):
        raise ValueError("GPA must be a number.")
    if not 0 <= gpa <= 10:
        raise ValueError("GPA must be between 0 and 10.")

    if not isinstance(credit_count, int) or isinstance(
        credit_count, bool
    ):
        raise ValueError("Credits must be an integer.")
    if credit_count < 0:
        raise ValueError("Credits cannot be negative.")

    if not isinstance(income, (int, float)) or isinstance(income, bool):
        raise ValueError("Income must be a number.")
    if income < 0:
        raise ValueError("Income cannot be negative.")

    score = calculate_merit_score(gpa, credit_count)
    eligible = score >= CUTOFF and income < INCOME_LIMIT

    results[student_id] = {
        "score": score,
        "eligible": eligible,
    }

    logs.append(f"{student_id} scored {score}")
    return eligible


def change_formula(new_formula):
    """Validate and update the merit formula."""
    global MERIT_FORMULA

    if not isinstance(new_formula, str) or not new_formula.strip():
        raise ValueError("Formula cannot be empty.")

    old_formula = MERIT_FORMULA
    MERIT_FORMULA = new_formula

    try:
        calculate_merit_score(1, 1)
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as error:
        MERIT_FORMULA = old_formula
        raise ValueError(f"Invalid merit formula: {error}") from error


def persist_results(file="scholarships.json"):
    """Save scholarship results to a JSON file."""
    with open(file, "w", encoding="utf-8") as result_file:
        json.dump(results, result_file, indent=4)


def load_results(file="scholarships.json"):
    """Load scholarship results from a JSON file."""
    global results

    try:
        with open(file, "r", encoding="utf-8") as result_file:
            loaded_results = json.load(result_file)

        if not isinstance(loaded_results, dict):
            raise ValueError("Results file must contain a JSON object.")

        results = loaded_results

    except FileNotFoundError:
        results = {}

    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Could not load results: {error}")


def print_shortlist():
    """Print all eligible applicants and their scores."""
    print("Shortlisted applicants:")

    for student_id, applicant in results.items():
        if applicant["eligible"]:
            print(f"  {student_id} score = {applicant['score']}")


def main():
    """Run the scholarship screening workflow."""
    applicants = [
        ("U001", {"gpa": 9.1, "credits": 4, "income": 450000}),
        ("U002", {"gpa": 7.2, "credits": 1, "income": 300000}),
        ("U003", {"gpa": 12.5, "credits": -3, "income": -1}),
        ("U004", {"gpa": 6.5}),
    ]

    for student_id, test_scores in applicants:
        try:
            evaluate_applicant(student_id, test_scores)
        except ValueError as error:
            print(f"Skipping {student_id}: {error}")

    formula = input("Merit formula (Enter to keep default): ")

    if formula.strip():
        try:
            change_formula(formula)
        except ValueError as error:
            print(f"Invalid formula; keeping the previous formula: {error}")

    try:
        evaluate_applicant(
            "U005",
            {"gpa": 8.4, "credits": 3, "income": 600000},
        )
    except ValueError as error:
        print(f"Skipping U005: {error}")

    persist_results()
    load_results()
    print_shortlist()


if __name__ == "__main__":
    main()
