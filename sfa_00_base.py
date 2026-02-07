# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "openai",
#     "pydantic",
#     "pydantic-settings",
# ]
# ///
from __future__ import annotations

from openai import OpenAI, pydantic_function_tool
from pydantic import BaseModel
from pydantic_settings import BaseSettings, CliPositionalArg, SettingsConfigDict

# tools

class Calculator(BaseModel):

    num1: float
    num2: float
    operator: str

    def run(self) -> float:
        match self.operator:
            case "+": return self.num1 + self.num2
            case "-": return self.num1 - self.num2
            case "*": return self.num1 * self.num2
            case "/":
                if self.num2 == 0:
                    raise ValueError("Division by zero is not allowed")
                return self.num1 / self.num2
        raise ValueError(f"Invalid operator: {self.operator}")


class Permutator(BaseModel):

    num: int

    def run(self) -> list[list[int]]:
        import itertools

        # Generate all permutations of numbers from 1 to num
        numbers = list(range(1, self.num + 1))
        return [list(p) for p in itertools.permutations(numbers)]


# env
class CliArgs(BaseSettings, cli_parse_args=True):
    """Ask AI to calculate or permutat numbers"""
    # args
    prompt: CliPositionalArg[str]
    # .env
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", cli_parse_args=True)

    @classmethod
    def show_help(cls):
        """Show help information about using this tool."""
        print("Single File Agent - Calculator and Permutator")
        print("\nExamples:")
        print("  python sfa_00_base.py 'Calculate 25 * 16'")
        print("  python sfa_00_base.py 'Generate all permutations of 3 numbers'")
        print("\nAvailable tools:")
        print("  - Calculator: Perform basic arithmetic operations (+, -, *, /)")
        print("  - Permutator: Generate all possible permutations of numbers 1 to n")



def main()->None:
    import sys

    # Check if no arguments provided, show help
    if len(sys.argv) < 2:
        CliArgs.show_help()
        return

    args = CliArgs()

    if not args.openai_api_key:
        print("Error: OpenAI API key is required. Please set it in .env file or as an environment variable.")
        return
        
    client = OpenAI(api_key=args.openai_api_key)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant that can perform calculations and generate permutations."},
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
            match tool_call.function.name:
                case "Calculator":
                    result = Calculator.model_validate_json(tool_call.function.arguments).run()
                case "Permutator":
                    result = Permutator.model_validate_json(tool_call.function.arguments).run()
                case _:
                    result = "Error: no tool execution function found"
        except Exception as e:
            result = f"Error: {e}"

        formatted_result = result
        if isinstance(result, list) and len(result) > 10:
            # Truncate long lists for display
            formatted_result = result[:10]
            formatted_result.append("... (truncated)")

        print(f"Tool: {tool_call.function.name}")
        print(f"Result: {formatted_result}")

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
    print("\nFinal Response:")
    print("-" * 40)
    print(final_response.choices[0].message.content)
    print("-" * 40)



if __name__ == "__main__":
    main()
