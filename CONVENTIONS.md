# Conventions

## minimalist python principles

When writing Python code, you MUST follow these principles:

- **Environment & Tooling**
  - Use Python **3.12+**; avoid legacy versions.
  - Centralize configuration in `pyproject.toml`.
  - Use **uv** for project initialization, dependency management, and running scripts.
  - Favor **Ruff** for linting and PEP 8 compliance.

- **Code Simplicity & Readability**
  - Keep it small, simple, and Pythonic (KISS).
  - Code must be easy to read and understand.
  - Use meaningful names that reveal intent.
  - Write small functions that do one thing well.
  - Keep functions focused; aim for no more than 2–3 arguments.

- **Comments & Documentation**
  - Use comments only when necessary; code should be self-explanatory.
  - When used, comments must add value beyond the obvious.
  - Document core logic with clear docstrings.

- **Type Hints & Data Modeling**
  - Annotate all functions, methods, and variables.
  - Run static checks with **mypy** (or similar).
  - Use **Pydantic** for data parsing, validation, and CLI argument handling.
  - Prefer immutable data structures (e.g., `@dataclass(frozen=True)` or Pydantic models).
  - Separate data from operations; use patterns like **Strategy** when needed.

- **Error Handling & Security**
  - Handle errors robustly; use exceptions (not error codes).
  - Implement security best practices to protect against vulnerabilities.

- **Functional Programming Principles**
  - Embrace pure functions, immutability, function composition, and declarative code.
  - Limit side effects in your design.

- **Object Orientation & Design**
  - Minimize object-oriented programming; avoid complex class hierarchies.
  - Favor functional style and composition over inheritance.

- **Building, Testing & Refactoring**
  - Ensure builds are fast; use **uv** for packaging and distribution.
  - Write modular code; avoid monolithic scripts.
  - Test thoroughly with **pytest** or `unittest` and maintain high coverage.
  - Refactor frequently; steer clear of over-engineering and God objects.
  - Watch for code smells: Shotgun Surgery, Over-Engineering, and Spaghetti Code.

- **Web APIs (If Needed)**
  - Prefer **FastAPI** for asynchronous, performant APIs.
  - Keep routes minimal and separate data validation using Pydantic models.
  - Use patterns like **Facade** to simplify complex subsystems.

- **Inline Script Metadata**
  - Embed metadata (author, version, script name) in scripts per the inline‑script‑metadata spec.
  - Execute scripts via `uv run`.


## Examples

examples illustrate the conventions:
- Use clear, simple functions.
- Validate inputs with type hints and pydantic.
- Keep configurations centralized.
- Leverage **uv** for a unified development workflow.
- Emphasize minimalism and readability throughout your project.

### Design Patterns & Type Validation

Below is a single Python code block showing multiple design patterns.
It merges type hints and runtime argument validation with **pydantic.validate_call**.

```python
from pydantic import BaseModel, validate_call

# Strategy Pattern: processing data with a pure function.
@validate_call
def strategy_process(data: int) -> int:
    return data * 2

# Command Pattern: encapsulate an operation.
class Command:
    @validate_call
    def __call__(self, message: str) -> None:
        print(f"Command executed: {message}")

# Facade Pattern: simplify complex operations.
@validate_call
def facade_operation(x: float, y: float) -> float:
    return (x + y) / 2

# Adapter Pattern: wrap legacy functionality.
class LegacyService:
    def old_method(self, value: str) -> str:
        return value.upper()

class Adapter:
    @validate_call
    def new_method(self, value: str) -> str:
        legacy = LegacyService()
        return legacy.old_method(value)

# Dependency Injection: pass dependencies explicitly.
class Service(BaseModel):
    name: str

@validate_call
def consumer(service: Service, times: int) -> None:
    for _ in range(times):
        print(f"Service {service.name} is used.")

if __name__ == '__main__':
    print(strategy_process(5))
    Command()("Execute command")
    print(facade_operation(10.0, 20.0))
    print(Adapter().new_method("adapter"))
    consumer(Service(name="MyService"), times=3)
```

---

### `pyproject.toml` Example

Below is a sample `pyproject.toml` configured for a project with source code in the `src` folder.
It uses **uv** for project management, includes example dependencies, and configures **ruff** and **pytest**.

```toml
[build-system]
requires = ["uv>=1.0"]
build-backend = "uv.build"

[project]
name = "minimalist_python_project"
version = "0.1.0"
description = "A sample project following minimalist‑Python conventions."
authors = ["Your Name <you@example.com>"]
requires-python = ">=3.12"
dependencies = [
    "pydantic>=1.10",
    "fastapi>=0.78",
    "uv>=1.0"
]

[tool.uv]
# uv commands for scripts.
scripts = {
    "start": "uv run src/main.py",
    "test": "pytest"
}
# Additional project dependency groups.
[tool.uv.deps]
dev = ["pytest>=7", "mypy>=0.961"]

[tool.uv.project]
src = "src"

[tool.ruff]
line-length = 88
select = ["E", "F", "W"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

---

### Project Development Workflow with **uv**

- **Initialize Project:**
  Run `uv init --project` to set up your project.

- **Add Dependencies:**
  Use `uv add <dependency>` (e.g., `uv add requests`) to include a package.

- **Run Tests:**
  Execute `uv run` (or the test script defined in `pyproject.toml`) to run your tests.

- **Lock Dependencies:**
  Use `uv lock --project` to lock dependency versions.

- **Export Lockfile:**
  Run `uv export --project` to output a reproducible dependency list.

---

### Inline Script Metadata Example

- **Metadata Block:**
  Starts with `# /// script` and ends with `# ///`.

- **Content:**
  Must be valid TOML with each line as a comment.
  Fields include `requires-python` and `dependencies`.

- **Purpose:**
  Enables tools to automatically manage script dependencies and Python version requirements.

- **Usage:**
  Use `uv init --script` to create a script with embedded metadata, and `uv add --script` to update it.

Example inline metadata block:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///
import requests
print(requests.__version__)
```

*(See specification details in citepython-inline-script-metadata.md)*

---

### Python Script Development Workflow with **uv**

- **Script Initialization:**
  Create a new script with `uv init --script example.py --python 3.12`.

- **Declare Dependencies:**
  Add required packages using:
  `uv add --script example.py 'requests<3' 'rich'`.

- **Run the Script:**
  Execute with `uv run example.py`.
  Use `--no-project` if not relying on project dependencies.

- **Lock Dependencies:**
  Lock the script with `uv lock --script example.py` for reproducibility.

- **Update as Needed:**
  Modify metadata with `uv add --script` and re-run as required.
