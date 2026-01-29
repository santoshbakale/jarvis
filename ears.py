import speech_recognition as sr
from rich.console import Console
from typing import Optional

console = Console()

class Ears:
    """Handles speech-to-text conversion."""
    
    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = None
            self.available = True
        except Exception as e:
            console.print(f"[yellow]Warning: Speech recognition not available: {e}[/yellow]")
            self.available = False
        
    def listen(self, timeout: int = 5) -> Optional[str]:
        """Listen to microphone and convert speech to text."""
        if not self.available:
            console.print("[yellow]Speech recognition not available.[/yellow]")
            return None
            
        try:
            with sr.Microphone() as source:
                console.print("[cyan]Listening...[/cyan]")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                console.print("[dim]Processing speech...[/dim]")
                
                # Convert speech to text using Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                return text
                
        except sr.WaitTimeoutError:
            console.print("[yellow]No speech detected.[/yellow]")
            return None
        except sr.UnknownValueError:
            console.print("[yellow]Could not understand audio.[/yellow]")
            return None
        except sr.RequestError as e:
            console.print(f"[red]Speech recognition error: {e}[/red]")
            return None
        except Exception as e:
            console.print(f"[red]Microphone error: {e}[/red]")
            console.print("[yellow]Make sure you have a microphone connected and PyAudio installed.[/yellow]")
            return None
    
    def listen_for_wake_word(self, wake_word: str = "jarvis") -> bool:
        """Listen for the wake word to activate Jarvis."""
        if not self.available:
            return False
            
        text = self.listen(timeout=3)
        if text and wake_word.lower() in text.lower():
            console.print(f"[green]Wake word '{wake_word}' detected![/green]")
            return True
        return False
