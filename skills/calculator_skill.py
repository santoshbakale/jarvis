from skills.base import BaseSkill
import re

class CalculatorSkill(BaseSkill):
    """Performs basic mathematical calculations."""
    
    @property
    def name(self) -> str:
        return "calculator"
    
    @property
    def description(self) -> str:
        return "Perform mathematical calculations (add, subtract, multiply, divide)"
    
    def execute(self, expression: str) -> str:
        """
        Execute a mathematical calculation.
        
        Args:
            expression: Mathematical expression to evaluate
        
        Returns:
            Result of the calculation
        """
        try:
            # Clean the expression - only allow numbers, operators, parentheses, and spaces
            cleaned = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            
            # Evaluate the expression safely
            result = eval(cleaned, {"__builtins__": {}}, {})
            
            return f"{expression} = {result}"
            
        except ZeroDivisionError:
            return "Error: Cannot divide by zero"
        except Exception as e:
            return f"Error: Invalid mathematical expression - {str(e)}"
