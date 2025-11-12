"""
Pizza Ordering State Machine - Core Logic

This demonstrates the "Tool-as-Guide" pattern where the tool (not the AI)
controls the workflow through a state machine.
"""

import uuid
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PizzaOrder:
    """Represents a pizza order in progress"""
    session_id: str
    state: str = "START"
    crust: Optional[str] = None
    category: Optional[str] = None  # "vegetarian" or "meat"
    toppings: List[str] = field(default_factory=list)
    size: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert order to dictionary"""
        return {
            "session_id": self.session_id,
            "state": self.state,
            "crust": self.crust,
            "category": self.category,
            "toppings": self.toppings,
            "size": self.size,
            "created_at": self.created_at.isoformat()
        }


class PizzaOrderGuide:
    """
    State machine that guides AI through pizza ordering workflow.
    
    This is the "Guide" in the Tool-as-Guide pattern. It controls the
    conversation flow, not the AI host.
    """
    
    # Menu options
    CRUSTS = ["Thin", "Regular", "Thick", "Gluten-free"]
    SIZES = ["Small (10\")", "Medium (12\")", "Large (14\")", "Extra Large (16\")"]
    
    VEGETARIAN_TOPPINGS = [
        "Mushrooms", "Olives", "Bell Peppers", "Onions", 
        "Tomatoes", "Spinach", "Artichokes", "Pineapple"
    ]
    
    MEAT_TOPPINGS = [
        "Pepperoni", "Sausage", "Ham", "Bacon",
        "Chicken", "Ground Beef", "Salami"
    ]
    
    def __init__(self):
        self.sessions: Dict[str, PizzaOrder] = {}
    
    def start_order(self) -> dict:
        """
        Start a new pizza order.
        
        Returns instructions for the AI host on what to do next.
        """
        session_id = str(uuid.uuid4())[:8]
        order = PizzaOrder(session_id=session_id, state="CHOOSE_CRUST")
        self.sessions[session_id] = order
        
        return {
            "status": "in_progress",
            "session_id": session_id,
            "action": "ask_user",
            "prompt": f"Great! Let's build your perfect pizza. What kind of crust would you like?\n\nOptions: {', '.join(self.CRUSTS)}",
            "next_state": "CHOOSE_CRUST",
            "instructions_for_ai": "Ask the user this exact question and wait for their response."
        }
    
    def continue_order(self, session_id: str, user_response: str) -> dict:
        """
        Process user response and advance to next step.
        
        This is where the state machine logic lives. The AI doesn't decide
        what to ask next - the guide does.
        """
        if session_id not in self.sessions:
            return {
                "status": "error",
                "message": f"Session {session_id} not found. Please start a new order."
            }
        
        order = self.sessions[session_id]
        user_response = user_response.strip()
        
        # State machine logic
        if order.state == "CHOOSE_CRUST":
            return self._handle_crust_choice(order, user_response)
        
        elif order.state == "CHOOSE_CATEGORY":
            return self._handle_category_choice(order, user_response)
        
        elif order.state == "CHOOSE_TOPPINGS":
            return self._handle_toppings_choice(order, user_response)
        
        elif order.state == "CHOOSE_SIZE":
            return self._handle_size_choice(order, user_response)
        
        elif order.state == "CONFIRM":
            return self._handle_confirmation(order, user_response)
        
        else:
            return {
                "status": "error",
                "message": f"Unknown state: {order.state}"
            }
    
    def _handle_crust_choice(self, order: PizzaOrder, response: str) -> dict:
        """Handle crust selection and move to category"""
        # Simple matching - in production you'd use better NLP
        crust = self._match_option(response, self.CRUSTS)
        
        if not crust:
            return {
                "status": "in_progress",
                "session_id": order.session_id,
                "action": "ask_user",
                "prompt": f"I didn't catch that. Please choose from: {', '.join(self.CRUSTS)}",
                "stay_in_state": True,
                "instructions_for_ai": "The user's response was unclear. Ask them to choose from the listed options."
            }
        
        order.crust = crust
        order.state = "CHOOSE_CATEGORY"
        
        return {
            "status": "in_progress",
            "session_id": order.session_id,
            "action": "ask_user",
            "prompt": f"Perfect! {crust} crust it is. Would you like a vegetarian pizza or one with meat?",
            "next_state": "CHOOSE_CATEGORY",
            "instructions_for_ai": "Acknowledge their choice and ask this next question."
        }
    
    def _handle_category_choice(self, order: PizzaOrder, response: str) -> dict:
        """Handle vegetarian/meat choice and show relevant toppings"""
        response_lower = response.lower()
        
        if "veg" in response_lower:
            order.category = "vegetarian"
            toppings = self.VEGETARIAN_TOPPINGS
        elif "meat" in response_lower:
            order.category = "meat"
            toppings = self.MEAT_TOPPINGS
        else:
            return {
                "status": "in_progress",
                "session_id": order.session_id,
                "action": "ask_user",
                "prompt": "Please say 'vegetarian' or 'meat'.",
                "stay_in_state": True
            }
        
        order.state = "CHOOSE_TOPPINGS"
        
        return {
            "status": "in_progress",
            "session_id": order.session_id,
            "action": "ask_user",
            "prompt": f"Great choice! Here are your {order.category} topping options:\n\n{', '.join(toppings)}\n\nPlease list the toppings you'd like (e.g., 'Mushrooms, Olives, Bell Peppers')",
            "next_state": "CHOOSE_TOPPINGS",
            "available_toppings": toppings,
            "instructions_for_ai": "Show the user the topping options and wait for their selection."
        }
    
    def _handle_toppings_choice(self, order: PizzaOrder, response: str) -> dict:
        """Handle topping selection and move to size"""
        # Get available toppings based on category
        available = self.VEGETARIAN_TOPPINGS if order.category == "vegetarian" else self.MEAT_TOPPINGS
        
        # Simple parsing - split by comma or "and"
        parts = response.replace(" and ", ",").split(",")
        selected_toppings = []
        
        for part in parts:
            topping = self._match_option(part.strip(), available)
            if topping:
                selected_toppings.append(topping)
        
        if not selected_toppings:
            return {
                "status": "in_progress",
                "session_id": order.session_id,
                "action": "ask_user",
                "prompt": f"I didn't recognize any of those toppings. Please choose from: {', '.join(available)}",
                "stay_in_state": True
            }
        
        order.toppings = selected_toppings
        order.state = "CHOOSE_SIZE"
        
        toppings_str = ", ".join(selected_toppings)
        return {
            "status": "in_progress",
            "session_id": order.session_id,
            "action": "ask_user",
            "prompt": f"Excellent! Your pizza will have: {toppings_str}\n\nWhat size would you like?\n\nOptions: {', '.join(self.SIZES)}",
            "next_state": "CHOOSE_SIZE",
            "instructions_for_ai": "Confirm their toppings and ask about size."
        }
    
    def _handle_size_choice(self, order: PizzaOrder, response: str) -> dict:
        """Handle size selection and move to confirmation"""
        size = self._match_option(response, self.SIZES)
        
        if not size:
            return {
                "status": "in_progress",
                "session_id": order.session_id,
                "action": "ask_user",
                "prompt": f"Please choose from: {', '.join(self.SIZES)}",
                "stay_in_state": True
            }
        
        order.size = size
        order.state = "CONFIRM"
        
        # Generate order summary
        summary = self._generate_summary(order)
        
        return {
            "status": "in_progress",
            "session_id": order.session_id,
            "action": "ask_user",
            "prompt": f"Here's your order:\n\n{summary}\n\nLooks good? (yes/no)",
            "next_state": "CONFIRM",
            "order_summary": summary,
            "instructions_for_ai": "Show the order summary and ask for confirmation."
        }
    
    def _handle_confirmation(self, order: PizzaOrder, response: str) -> dict:
        """Handle final confirmation"""
        response_lower = response.lower()
        
        if "yes" in response_lower or "confirm" in response_lower or "looks good" in response_lower:
            order.state = "COMPLETE"
            summary = self._generate_summary(order)
            
            # In a real app, this would place the order
            return {
                "status": "complete",
                "session_id": order.session_id,
                "action": "respond",
                "message": f"🎉 Order confirmed!\n\n{summary}\n\nYour pizza will be ready in 20-30 minutes. Thank you!",
                "order": order.to_dict(),
                "instructions_for_ai": "Tell the user their order is confirmed and provide the summary."
            }
        else:
            # Cancel order
            del self.sessions[order.session_id]
            return {
                "status": "cancelled",
                "session_id": order.session_id,
                "action": "respond",
                "message": "No problem! Your order has been cancelled. Feel free to start a new order anytime.",
                "instructions_for_ai": "Tell the user the order was cancelled."
            }
    
    def _generate_summary(self, order: PizzaOrder) -> str:
        """Generate order summary string"""
        toppings = ", ".join(order.toppings)
        return f"""
• Size: {order.size}
• Crust: {order.crust}
• Category: {order.category.title()}
• Toppings: {toppings}
        """.strip()
    
    def _match_option(self, user_input: str, options: List[str]) -> Optional[str]:
        """Simple fuzzy matching for menu options"""
        user_input = user_input.lower().strip()
        
        for option in options:
            if option.lower() in user_input or user_input in option.lower():
                return option
        
        return None
    
    def get_order(self, session_id: str) -> Optional[dict]:
        """Get current order state"""
        if session_id in self.sessions:
            return self.sessions[session_id].to_dict()
        return None
    
    def cancel_order(self, session_id: str) -> dict:
        """Cancel an order"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return {
                "status": "cancelled",
                "message": "Order cancelled successfully."
            }
        return {
            "status": "error",
            "message": f"Session {session_id} not found."
        }

