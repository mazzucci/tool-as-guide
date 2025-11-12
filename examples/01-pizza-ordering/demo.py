#!/usr/bin/env python3
"""
Simple CLI demo of the pizza ordering state machine.

Run this to test the guide logic without needing MCP or Cursor.
"""

from pizza_guide import PizzaOrderGuide


def main():
    """Run interactive pizza ordering demo"""
    guide = PizzaOrderGuide()
    
    print("=" * 60)
    print("🍕 PIZZA ORDERING DEMO - Tool-as-Guide Pattern")
    print("=" * 60)
    print()
    print("This demonstrates how the state machine guides the conversation.")
    print("The guide decides what to ask next, not the AI.")
    print()
    print("-" * 60)
    print()
    
    # Start order
    result = guide.start_order()
    session_id = result["session_id"]
    
    print(f"[Guide] Starting order (session: {session_id})")
    print()
    
    # Main conversation loop
    while True:
        if result["status"] == "complete":
            print(f"\n✅ {result['message']}")
            break
        
        if result["status"] == "cancelled":
            print(f"\n❌ {result['message']}")
            break
        
        if result["status"] == "error":
            print(f"\n⚠️  Error: {result['message']}")
            break
        
        # Display prompt from guide
        print(f"[Guide → AI → You] {result['prompt']}")
        print()
        
        # Get user input
        user_response = input("Your response: ").strip()
        print()
        
        if not user_response:
            print("Please provide a response.")
            continue
        
        # Send response back to guide
        print(f"[You → AI → Guide] Processing: '{user_response}'")
        print()
        
        result = guide.continue_order(session_id, user_response)
        
        # Show next state (for demonstration)
        if "next_state" in result:
            print(f"[Guide State Machine] Moving to: {result['next_state']}")
            print()
    
    print()
    print("=" * 60)
    print("Demo complete! Notice how the guide controlled the entire workflow.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Order cancelled. Goodbye!")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")

