# Python Minimalist Programming Conventions

> Keep it small. Keep it simple. Keep it Pythonic. Embrace **KISS**: “Keep It Simple, Stupid.”

## 1. Python Version & Environment
- Target Python **3.12+** for modern features and performance.
- Avoid legacy Python releases to reduce fragmentation.

## 2. Tooling & Dependencies
- Use [**uv**](https://github.com/…) for:
  - Project initialization: `uv init <project>`
  - Adding dependencies: `uv add <dependency>` (or `--script` for script-level deps)
  - Running scripts: `uv run <script>`
- Centralize all configuration in `pyproject.toml`.
- Favor **Ruff** for linting and formatting (PEP 8 style).
- Keep dependencies minimal. Avoid bloat in environment.

## 3. Type Hints & Validation
- Annotate all functions, methods, and variables (`def func(x: int) -> str:`).
- Run static checks with **mypy** or similar.
- Use **Pydantic** for:
  - Data parsing, validation (e.g., `BaseModel`, `conint`).
  - Configuration - use pydantic‑settings (`class Settings(BaseSettings)`).
  - Command-line args - use pydantic‑settings (`class Settings(BaseSettings, cli_parse_args=True)`).

## 4. Data Modeling & Immutability
- Prefer immutable data structures (`@dataclass(frozen=True)` or `pydantic` models).
- Keep data and operations separate where possible.
  - **Design Pattern**: Use the **Strategy** pattern for different data processing strategies without deep inheritance.
- Avoid complex class hierarchies (favor composition over inheritance).

## 5. Simple Code & Maintainability
- Embrace **KISS**: make logic plain and direct.
- Follow **DRY**: "Don’t Repeat Yourself." Factor out common code. Factor out common configuration.
- Write code that is explicit and easy to follow.
- Keep functions small and focused (Single Responsibility).
- Favor clear variable names and straightforward loops/comprehensions.
- Document core logic inline. Rely on docstrings for function-level detail.
- **Code Smell**: **God Object** – avoid huge classes with too many responsibilities.

## 6. Building & Running
- Ensure builds are fast (seconds, not minutes).
- Use **uv** for packaging and distribution to unify your workflow.
- Keep code modular. Avoid monolithic scripts that do everything.

## 7. Testing & Refactoring
- Use **pytest** or built-in `unittest` for thorough unit tests.
- Maintain high code coverage with both unit and integration tests.
- Refactor frequently, removing unnecessary complexity.
- **Code Smell**: **Over-Engineering** – watch for unnecessary abstractions.

## 8. Web APIs (If Needed)
- Prefer **FastAPI** for asynchronous, performant APIs.
- Keep routes and logic minimal; avoid massive controllers.
- Separate data validation from business logic with Pydantic models.
- **Design Pattern**: **Facade** to simplify external API calls.

## 9. Common Design Patterns for Minimalist Python
| Pattern                | Usage                                                      | Notes                                                                            |
|------------------------|------------------------------------------------------------|----------------------------------------------------------------------------------|
| **Strategy**           | Different algorithms under one interface                  | Avoid if a single function or small switch-case suffices                         |
| **Command**            | Encapsulate operations as objects                         | Useful for CLI tools or job scheduling                                           |
| **Facade**             | Simplify complex subsystems behind a simple API           | Ideal for external API integrations or complex library calls                     |
| **Adapter**            | Adapt external/legacy interfaces to a new API             | Use only when absolutely necessary                                               |
| **Dependency Injection** | Separate creation of dependencies from their usage       | Reduces coupling, eases testing, encourages clear interfaces (example below)     |

### Example: Basic Dependency Injection in Python
```python
class Service:
    def do_work(self) -> None:
        print("Real work done.")

class Consumer:
    def __init__(self, service: Service) -> None:
        self.service = service

    def run(self) -> None:
        self.service.do_work()

# Inject the dependency at creation
service = Service()
consumer = Consumer(service=service)
consumer.run()
```

## 10. Common Code Smells to Avoid
| Smell                | Description                                                               | Mitigation                                                |
|----------------------|---------------------------------------------------------------------------|-----------------------------------------------------------|
| **God Object**       | Class too large, too many responsibilities                               | Split into smaller classes or functions                   |
| **Shotgun Surgery**  | Changing one aspect forces changes in many parts of the code             | Centralize related logic; reduce coupling                 |
| **Over-Engineering** | Adding layers/abstractions with no immediate need                        | Implement only minimal features first; YAGNI principle    |
| **Spaghetti Code**   | Code flow is tangled and hard to follow                                  | Use clear function structure; keep logic compartmentalized|

## 11. Inline Script Metadata
- Embed metadata (author, version, script name) in Python scripts using the official inline‑script‑metadata spec.
- Run scripts via `uv run script.py`.
