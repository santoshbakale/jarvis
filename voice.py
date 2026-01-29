import pyttsx3
from rich.console import Console
from typing import Optional

console = Console()

class Voice:
    """Handles text-to-speech conversion."""
    
    def __init__(self, voice_id: Optional[str] = None):
        try:
            self.engine = pyttsx3.init()
            
            # Configure voice properties
            self.engine.setProperty('rate', 175)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
            
            # Set voice if specified
            if voice_id:
                voices = self.engine.getProperty('voices')
                try:
                    voice_index = int(voice_id)
                    if 0 <= voice_index < len(voices):
                        self.engine.setProperty('voice', voices[voice_index].id)
                except (ValueError, IndexError):
                    # Try to find voice by ID string
                    for voice in voices:
                        if voice_id in voice.id:
                            self.engine.setProperty('voice', voice.id)
                            break
            
            self.available = True
                            
        except Exception as e:
            console.print(f"[yellow]Voice initialization warning: {e}[/yellow]")
            console.print("[yellow]Text-to-speech not available. Running in text-only mode.[/yellow]")
            self.engine = None
            self.available = False
    
    def speak(self, text: str):
        """Convert text to speech and play it."""
        if not self.engine or not self.available:
            console.print(f"[bold cyan]Jarvis:[/bold cyan] {text}")
            return
            
        try:
            console.print(f"[bold cyan]Jarvis:[/bold cyan] {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            console.print(f"[yellow]Speech error: {e}[/yellow]")
            console.print(f"[bold cyan]Jarvis:[/bold cyan] {text}")
    
    def list_voices(self):
        """List all available voices."""
        if not self.engine or not self.available:
            console.print("[yellow]Voice engine not available.[/yellow]")
            return
            
        voices = self.engine.getProperty('voices')
        console.print("\n[bold]Available voices:[/bold]")
        for idx, voice in enumerate(voices):
            console.print(f"{idx}: {voice.name} ({voice.id})")
