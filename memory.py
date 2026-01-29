import json
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from datetime import datetime

console = Console()

class Memory:
    """Manages long-term memory and user preferences."""
    
    def __init__(self, memory_file: str = "memory.json"):
        self.memory_file = Path(memory_file)
        self.data: Dict[str, Any] = self._load()
        
    def _load(self) -> Dict[str, Any]:
        """Load memory from file."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                console.print(f"[yellow]Could not load memory: {e}[/yellow]")
                return {"facts": {}, "preferences": {}, "history": []}
        return {"facts": {}, "preferences": {}, "history": []}
    
    def _save(self):
        """Save memory to file."""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            console.print(f"[red]Could not save memory: {e}[/red]")
    
    def remember_fact(self, key: str, value: Any):
        """Store a fact in long-term memory."""
        self.data["facts"][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._save()
        console.print(f"[green]Remembered: {key} = {value}[/green]")
    
    def recall_fact(self, key: str) -> Optional[Any]:
        """Retrieve a fact from memory."""
        fact = self.data["facts"].get(key)
        if fact:
            return fact["value"]
        return None
    
    def set_preference(self, key: str, value: Any):
        """Set a user preference."""
        self.data["preferences"][key] = value
        self._save()
        console.print(f"[green]Preference set: {key} = {value}[/green]")
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference."""
        return self.data["preferences"].get(key, default)
    
    def add_to_history(self, entry: str):
        """Add an entry to interaction history."""
        self.data["history"].append({
            "entry": entry,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 100 entries
        if len(self.data["history"]) > 100:
            self.data["history"] = self.data["history"][-100:]
        self._save()
    
    def get_all_facts(self) -> Dict[str, Any]:
        """Get all stored facts."""
        return {k: v["value"] for k, v in self.data["facts"].items()}
    
    def get_all_preferences(self) -> Dict[str, Any]:
        """Get all preferences."""
        return self.data["preferences"]
    
    def clear_all(self):
        """Clear all memory."""
        self.data = {"facts": {}, "preferences": {}, "history": []}
        self._save()
        console.print("[yellow]All memory cleared.[/yellow]")
