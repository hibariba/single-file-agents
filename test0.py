# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "openai>1.60",
#     "pydantic>=2.0",
# ]
# ///
# from pydantic import validate_call


# @validate_call
# def search_products(
#     query: str,
#     category: str|None = None,
#     max_results: int = 10,
# ) -> list[dict]:
#     """Search for products in the catalog."""
#     # Implementation...
#     return []

# from openai import pydantic_function_tool

# search_products_tool = pydantic_function_tool(search_products)

# print(search_products_tool)



from typing import List, Optional

from pydantic import Field, validate_call


# 1. Create a decorated function with type annotations
@validate_call
def search_products(
    query: str = Field(..., description="Search query string"),
    category: Optional[str] = Field(None, description="Product category filter"),
    max_results: int = Field(10, description="Maximum number of results to return"),
) -> List[dict]:
    """Search for products in the catalog."""
    # Implementation...
    return []

# 2. Extract function signature as a Pydantic model
# Get the validated_function from the decorated function
# validated_function = search_products.__pydantic_core_schema__

# 3. Create tool definition using pydantic_function_tool
from openai import pydantic_function_tool

# Create the tool
search_tool = pydantic_function_tool(search_products)

print(search_tool)

# # 4. Use the tool with OpenAI client
# client = OpenAI()
# response = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[{"role": "user", "content": "Find red shoes under $100"}],
#     tools=[search_tool],
# )
