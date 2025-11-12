"""
Pizza Ordering MCP Server

Demonstrates the "Tool-as-Guide" pattern where the MCP tool actively
orchestrates the conversation workflow rather than passively returning data.

The AI host (e.g., Cursor) acts as a messenger, relaying instructions
from the guide tool to the user and vice versa.
"""

from fastmcp import FastMCP
from pizza_guide import PizzaOrderGuide

# Initialize FastMCP server
mcp = FastMCP("Pizza Ordering Guide")

# Initialize the guide (state machine)
guide = PizzaOrderGuide()


@mcp.tool()
def start_pizza_order() -> dict:
    """
    Start a new pizza order.
    
    This begins the guided ordering workflow. The tool will return instructions
    for what the AI should ask the user next.
    
    Returns:
        Dictionary with session_id, prompt, and instructions for the AI
    """
    result = guide.start_order()
    return result


@mcp.tool()
def continue_pizza_order(session_id: str, user_response: str) -> dict:
    """
    Continue an existing pizza order with the user's response.
    
    The tool processes the response, updates the order state, and returns
    instructions for the next step. The AI host should follow these instructions
    exactly - the workflow logic lives in the tool, not the AI.
    
    Args:
        session_id: The order session ID from start_pizza_order()
        user_response: The user's response to the last question
    
    Returns:
        Dictionary with next prompt, state, and instructions for the AI
    """
    result = guide.continue_order(session_id, user_response)
    return result


@mcp.tool()
def get_order_status(session_id: str) -> dict:
    """
    Get the current status of a pizza order.
    
    Args:
        session_id: The order session ID
    
    Returns:
        Dictionary with current order details or error if not found
    """
    order = guide.get_order(session_id)
    if order:
        return {
            "status": "found",
            "order": order
        }
    return {
        "status": "error",
        "message": f"Order {session_id} not found"
    }


@mcp.tool()
def cancel_pizza_order(session_id: str) -> dict:
    """
    Cancel a pizza order.
    
    Args:
        session_id: The order session ID to cancel
    
    Returns:
        Dictionary with cancellation status
    """
    result = guide.cancel_order(session_id)
    return result


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()

