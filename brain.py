from openai import OpenAI
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
You are helpful, concise, and proactive. You have access to various tools and skills.
You can remember facts about the user, control their computer, answer questions, and assist with tasks.
Always be respectful and efficient. When uncertain, ask clarifying questions.
Keep responses conversational and natural, as if speaking to a friend."""

    def think(self, user_input: str, available_tools: Optional[List] = None) -> str:
        """Process user input and generate a response."""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Build messages for API call
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history[-10:]  # Keep last 10 messages for context
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            console.print(f"[red]Brain error: {e}[/red]")
            return "I'm having trouble thinking right now. Please check my configuration."
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        console.print("[dim]Memory cleared.[/dim]")
