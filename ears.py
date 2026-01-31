import speech_recognition as sr
from rich.console import Console
from typing import Optional

console = Console()

class Ears:
    """Handles speech-to-text conversion."""
    
    def __init__(self, device_index: Optional[int] = None):
        try:
            self.recognizer = sr.Recognizer()
            self.microphone_index = device_index
            
            # Check if PyAudio is installed
            import pyaudio
            self.available = True
        except ImportError:
            console.print("[yellow]Warning: PyAudio not installed. Microphone input will be disabled.[/yellow]")
            self.available = False
        except Exception as e:
            console.print(f"[yellow]Warning: Speech recognition initialization error: {e}[/yellow]")
            self.available = False
            
    def calibrate(self):
        """Calibrate the microphone for ambient noise."""
        if not self.available:
            return
        try:
            with sr.Microphone(device_index=self.microphone_index) as source:
                console.print("[dim]Calibrating microphone... Please stay quiet.[/dim]")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                # Set energy threshold slightly higher to reduce false positives
                self.recognizer.dynamic_energy_threshold = True
                console.print("[dim]Calibration complete.[/dim]")
        except Exception as e:
            console.print(f"[yellow]Calibration failed: {e}[/yellow]")
        
    def listen(self, timeout: int = 5, calibrate: bool = False) -> Optional[str]:
        """Listen to microphone and convert speech to text."""
        if not self.available:
            console.print("[yellow]Speech recognition not available.[/yellow]")
            return None
            
        try:
            with sr.Microphone(device_index=self.microphone_index) as source:
                if calibrate:
                    console.print("[dim]Calibrating for background noise...[/dim]")
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                console.print("[cyan]Listening...[/cyan]")
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                console.print("[dim]Processing speech...[/dim]")
                
                # Convert speech to text using Google Speech Recognition
                try:
                    text = self.recognizer.recognize_google(audio)
                    if text:
                        console.print(f"[dim]Heard: {text}[/dim]")
                    return text
                except sr.UnknownValueError:
                    # Log the energy level to help debugging
                    energy = self.recognizer.energy_threshold
                    console.print(f"[dim]Recognition failed. Current energy threshold: {energy:.1f}[/dim]")
                    return None
                
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
    
    def listen_for_wake_word(self, wake_word: str = "jarvis") -> Optional[str]:
        """
        Listen for the wake word. 
        Returns the full text if detected, so follow-up commands in the same breath aren't lost.
        """
        if not self.available:
            return None
            
        # Shorter timeout for wake word listening to keep it responsive
        text = self.listen(timeout=2, calibrate=False)
        
        if text and wake_word.lower() in text.lower():
            console.print(f"[green]Wake word '{wake_word}' detected![/green]")
            
            # If there's more text after the wake word, extract it
            # Example: "Jarvis what time is it" -> "what time is it"
            parts = text.lower().split(wake_word.lower(), 1)
            command = parts[1].strip() if len(parts) > 1 else ""
            
            return command if command else "WAKE_WORD_ONLY"
            
        return None
