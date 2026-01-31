from openai import OpenAI
import json
from typing import List, Dict, Optional
from config import settings
from rich.console import Console

console = Console()

class Brain:
    """The reasoning engine powered by LLM."""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            console.print("[yellow]Warning: OPENAI_API_KEY not set. Brain will not function.[/yellow]")
        
        # Check if it's an OpenRouter key
        base_url = None
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.startswith("sk-or-"):
            base_url = "https://openrouter.ai/api/v1"
            console.print("[dim]OpenRouter provider detected.[/dim]")
            
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=base_url)
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = self._build_system_prompt()
        
    def _build_system_prompt(self) -> str:
        """Define Jarvis's personality and capabilities."""
        return """You are Jarvis, a highly intelligent personal AI assistant.
You are helpful, concise, and proactive. You have access to real-time information via Google and other search engines.
You can remember facts about the user, control their computer, answer questions, and assist with tasks using your skills.
When a user asks for real-time data or something that requires current facts, use your 'google_search' tool immediately.
Always be respectful and efficient. Keep responses conversational and natural."""

    def _get_tools_definition(self) -> List[Dict]:
        """Define the tools available to Jarvis."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the internet for real-time information and facts.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "The search query."}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "google_search",
                    "description": "Perform an advanced Google search for precise real-time information and specific URLs.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "The search query."}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "visual_scan",
                    "description": "Activate the device's optical sensors (camera) to perform a visual scan of the environment.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "request_location",
                    "description": "Request the user's current GPS coordinates for navigation or local intelligence.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        ]

    def think(self, user_input: str, skills: Dict = None) -> str:
        """Process user input and generate a response, potentially using tools."""
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Initial tools definition
        tools = self._get_tools_definition()
        
        for _ in range(5): # Allow up to 5 tool iterations
            messages = [{"role": "system", "content": self.system_prompt}] + self.conversation_history[-15:]
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                    temperature=0.7
                )
                
                msg = response.choices[0].message
                
                if msg.tool_calls:
                    self.conversation_history.append(msg)
                    
                    for tool_call in msg.tool_calls:
                        function_name = tool_call.function.name
                        args = json.loads(tool_call.function.arguments)
                        
                        console.print(f"[dim]Executing tool: {function_name}({args})[/dim]")
                        
                        if skills and function_name in skills:
                            result = skills[function_name].execute(**args)
                        else:
                            result = f"Error: Tool {function_name} not found."
                            
                        self.conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": str(result)
                        })
                    continue # Call API again with tool results
                
                assistant_message = msg.content
                self.conversation_history.append({"role": "assistant", "content": assistant_message})
                return assistant_message
                
            except Exception as e:
                console.print(f"[red]Brain error: {e}[/red]")
                return "Sir, I'm experiencing cognitive interference. Please check my tool connectivity."
        
        return "I've reached my thinking limit for this request, Sir."
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        console.print("[dim]Memory cleared.[/dim]")
