# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "openai",
#     "pydantic",
#     "pydantic-ai-slim[openai]",
#     "pydantic-settings",
# ]
# ///
from __future__ import annotations

from typing import Protocol, runtime_checkable

from openai import OpenAI, pydantic_function_tool
from pydantic import BaseModel
from pydantic_settings import BaseSettings, CliPositionalArg, SettingsConfigDict


# Protocol for tools
@runtime_checkable
class ToolProtocol(Protocol):
    def run(self) -> any: ...

# tools
class Calculator(BaseModel):
    num1: float
    num2: float
    operator: str

    def run(self) -> float:
        match self.operator:
            case "+":
                return self.num1 + self.num2
            case "-":
                return self.num1 - self.num2
            case "*":
                return self.num1 * self.num2
            case "/":
                return self.num1 / self.num2 if self.num2 != 0 else float("nan")
        msg = f"Invalid operator: {self.operator}"
        raise ValueError(msg)

class Permutator(BaseModel):
    num: int

    def run(self) -> list[list[int]]:
        def permutator(n: int) -> list[list[int]]:
            if n == 0:
                return [[]]
            return [[i, *p] for i in range(1, n+1) for p in permutator(n-1)]

        return permutator(self.num)

TOOLS: dict[str, type[ToolProtocol]] = {
    "Calculator": Calculator,
    "Permutator": Permutator,
}

# env
class CliArgs(BaseSettings, cli_parse_args=True):
    """Ask AI to calculate or permutat numbers"""
    # args
    prompt: CliPositionalArg[str]
    # .env
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        cli_parse_args=True,
    )

def main()->None:
    args = CliArgs()
    client = OpenAI(api_key=args.openai_api_key)

    messages = [
        {"role": "system", "content": "You are a calculator."},
        {"role": "user", "content": args.prompt},
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=[
            pydantic_function_tool(Calculator),
            pydantic_function_tool(Permutator),
        ],
        tool_choice="auto",
    )

    # use tools
    tool_calls = (response.choices[0].message.tool_calls or [])
    for tool_call in tool_calls:
        try:
            tool = TOOLS[tool_call.function.name]
            tool_instance = tool.model_validate_json(tool_call.function.arguments)
            result = tool_instance.run()
        except (KeyError, ValueError) as e:
            result = f"Error: {e}"

        print(f"tool call: {tool_call.function.name} result: {result}")

        messages += [
            {"role": "assistant", "content": None, "tool_calls": [tool_call]},
            {"role": "tool","tool_call_id": tool_call.id, "content": str(result)},
        ]

    # Final API call to generate response
    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    # Print the final response
    print("final response :")
    print(final_response.choices[0].message.content)

if __name__ == "__main__":
    main()
