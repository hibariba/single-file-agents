# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai",
#     "pydantic",
#     "pydantic-settings",
# ]
# ///


from openai import OpenAI, pydantic_function_tool
from pydantic_settings import BaseSettings
from pydantic import Field, BaseModel

class Environment(BaseSettings, cli_parse_args=True):
    openai_api_key: str

class Calculator(BaseModel):



# env = Environment()
# tools = Tools(env)
# system_prompt = "Goals, constraints, and how to act"

# while True:
#     action = llm. run (system_prompt + env. state)
#     env. state = tools. run (action)


def main() -> None:
    print("Hello from 01-atomic-agent.py!")


if __name__ == "__main__":
    main()
