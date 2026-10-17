# Static Code Analysis — Issue Documentation

| Issue | Tool | Description | Fix |
|---|---|---|---|
| Unsafe formula evaluation | Bandit B307, Pylint W0123 | The original program used eval() directly on the formula. | Replaced eval() with a restricted AST-based mathematical evaluator. |
| Mutable default argument | Pylint W0102 | The logs=[] default shared a list between function calls. | Changed the default to None and initialized a new list inside the function. |
| Bare exception | Bandit B110, Flake8 E722 | A bare except silently ignored every exception. | Handled specific expected exceptions. |
| Missing file encoding | Pylint W1514 | Files were opened without an explicit encoding. | Specified UTF-8 when opening JSON files. |
| Unclosed file handles | Pylint R1732 | Files were manually opened and closed. | Used with statements for file handling. |
| Unused imports | Pylint W0611, Flake8 F401 | math and sys were imported but unused. | Removed unused imports. |
| Missing docstrings | Pylint C0114, C0116 | The module and functions lacked documentation. | Added module and function docstrings. |
| Naming convention | Pylint C0103 | printShortlist did not follow snake_case. | Renamed it to print_shortlist. |
| Boolean comparison | Pylint C0121, Flake8 E712 | The program compared a value directly with True. | Used a truthiness check. |
| Missing file encoding and formatting | Flake8 E302, E305, W292 | Blank lines and final newline did not follow style requirements. | Corrected formatting and added a final newline. |
| Invalid applicant data | Additional validation | Invalid GPA, credits, and income could produce misleading results. | Added validation and skipped invalid applicants. |

# Reflection

## 1. What is static code analysis?
Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, and style violations.

## 2. What did Pylint identify?
Pylint identified missing docstrings, unused imports, unsafe evaluation, mutable default arguments, broad exception handling, naming issues, and other code-quality concerns.

## 3. What did Bandit identify?
Bandit identified unsafe use of eval() and a bare exception that silently ignored errors. The final Bandit scan reported no issues.

## 4. What did Flake8 identify?
Flake8 identified unused imports, missing blank lines, a bare exception, a Boolean comparison, and a missing final newline.

## 5. How did the fixes improve the program?
The fixes improved code readability, reduced unsafe evaluation, strengthened input validation, improved file handling, and made exception handling more specific.

## 6. What did you learn?
I learned that static analysis tools complement one another: Pylint checks code quality, Bandit checks common security issues, and Flake8 checks style and formatting. Running the tools before and after changes helps verify improvements.
