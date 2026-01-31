#!/usr/bin/env python3
"""
Jarvis - Personal AI Assistant
Main entry point for the application
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from typing import Optional
import webbrowser
import pygetwindow as gw

from config import settings
from brain import Brain
from memory import Memory
from skills import TimeSkill, CalculatorSkill, WebSearchSkill, GoogleSearchSkill

# Try to import voice modules, but allow running without them
try:
    from ears import Ears
    from voice import Voice
    VOICE_AVAILABLE = True
except ImportError as e:
    VOICE_AVAILABLE = False
    console = Console()
    console.print(f"[yellow]Voice modules not available: {e}[/yellow]")
    console.print("[yellow]Running in text-only mode. Install requirements-optional.txt for voice support.[/yellow]")
    Ears = None
    Voice = None

app = typer.Typer()
console = Console()

class Jarvis:
    """Main Jarvis assistant class."""
    
    def __init__(self, voice_mode: bool = False):
        if voice_mode and not VOICE_AVAILABLE:
            console.print("[yellow]Voice mode requested but voice modules not available.[/yellow]")
            console.print("[yellow]Install requirements-optional.txt for voice support.[/yellow]")
            console.print("[yellow]Falling back to text mode.[/yellow]")
            voice_mode = False
            
        self.voice_mode = voice_mode
        self.brain = Brain()
        self.memory = Memory()
        self.voice = Voice(settings.VOICE_ID) if VOICE_AVAILABLE and voice_mode else None
        self.ears = Ears(device_index=settings.MIC_INDEX) if VOICE_AVAILABLE and voice_mode else None
        
        # Load skills
        self.skills = {
            "time": TimeSkill(),
            "calculator": CalculatorSkill(),
            "web_search": WebSearchSkill(),
            "google_search": GoogleSearchSkill()
        }
        
    def respond(self, text: str):
        """Generate and deliver a response."""
        response = self.brain.think(text, skills=self.skills)
        
        if self.voice_mode:
            self.voice.speak(response)
        else:
            console.print(f"\n[bold cyan]Jarvis:[/bold cyan] {response}\n")
    
    def process_command(self, user_input: str) -> bool:
        """Process special commands. Returns True if command was handled."""
        command = user_input.lower().strip()
        
        if command in ["exit", "quit", "goodbye", "bye"]:
            farewell = "Goodbye! Have a great day."
            if self.voice_mode and self.voice:
                self.voice.speak(farewell)
            else:
                console.print(f"[bold cyan]Jarvis:[/bold cyan] {farewell}")
            return True
            
        elif command == "clear":
            self.brain.clear_history()
            return False
            
        elif command == "memory":
            facts = self.memory.get_all_facts()
            prefs = self.memory.get_all_preferences()
            console.print("\n[bold]Stored Facts:[/bold]")
            for key, value in facts.items():
                console.print(f"  {key}: {value}")
            console.print("\n[bold]Preferences:[/bold]")
            for key, value in prefs.items():
                console.print(f"  {key}: {value}")
            console.print()
            return False
            
        elif command == "voices":
            if VOICE_AVAILABLE and self.voice:
                self.voice.list_voices()
            else:
                console.print("[yellow]Voice module not available.[/yellow]")
                console.print("[yellow]Install requirements-optional.txt for voice support.[/yellow]")
            return False
            
        elif command.startswith("remember "):
            # Format: remember <key>=<value>
            try:
                _, rest = command.split("remember ", 1)
                key, value = rest.split("=", 1)
                self.memory.remember_fact(key.strip(), value.strip())
            except ValueError:
                console.print("[yellow]Format: remember <key>=<value>[/yellow]")
            return False
            
        return False
    
    def run_text_mode(self):
        """Run in text-only mode."""
        console.print(Panel.fit(
            "[bold cyan]Jarvis AI Assistant[/bold cyan]\n"
            "Text Mode - Type your messages below\n"
            "Commands: exit, clear, memory, voices, remember <key>=<value>",
            border_style="cyan"
        ))
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold green]You[/bold green]")
                
                if not user_input.strip():
                    continue
                
                # Check for special commands
                if self.process_command(user_input):
                    break
                
                # Get response from Jarvis
                self.respond(user_input)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
    
    def run_voice_mode(self):
        """Run in voice interaction mode."""
        if not self.ears or not self.ears.available:
            console.print("[yellow]Voice input (microphone) is not available.[/yellow]")
            console.print("[yellow]Falling back to Text Input + Voice Output mode.[/yellow]")
            self.run_hybrid_mode()
            return

        console.print(Panel.fit(
            "[bold cyan]Jarvis AI Assistant[/bold cyan]\n"
            f"Voice Mode - Say '{settings.WAKE_WORD}' to activate\n"
            "Press Ctrl+C to exit",
            border_style="cyan"
        ))
        
        self.ears.calibrate()
        
        while True:
            try:
                # Listen for wake word
                wake_result = self.ears.listen_for_wake_word(settings.WAKE_WORD)
                
                if wake_result:
                    # Summon Protocol: Force HUD to front
                    try:
                        hud_windows = [w for w in gw.getWindowsWithTitle('JARVIS') if 'Virtual Assistant' in w.title or 'localhost' in w.title]
                        if hud_windows:
                            # If minimized, restore it
                            if hud_windows[0].isMinimized:
                                hud_windows[0].restore()
                            hud_windows[0].activate()
                        else:
                            webbrowser.open("http://localhost:8000")
                    except Exception as e:
                        # Fallback to simple open if anything fails
                        webbrowser.open("http://localhost:8000")
                    
                    user_input = None
                    
                    if wake_result == "WAKE_WORD_ONLY":
                        # Only wake word was heard, prompt for command
                        if self.voice_mode:
                            self.voice.speak("How can I help?")
                        user_input = self.ears.listen(timeout=10)
                    else:
                        # Command was already in the same breath
                        user_input = wake_result
                    
                    if user_input:
                        console.print(f"[bold green]You:[/bold green] {user_input}")
                        
                        # Check for exit commands
                        if self.process_command(user_input):
                            break
                        
                        # Get response
                        self.respond(user_input)
                        
            except KeyboardInterrupt:
                console.print("\n[yellow]Shutting down...[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

    def run_hybrid_mode(self):
        """Run with text input and voice output."""
        console.print(Panel.fit(
            "[bold cyan]Jarvis AI Assistant[/bold cyan]\n"
            "Hybrid Mode - Type your messages below\n"
            "Jarvis will respond with voice",
            border_style="cyan"
        ))
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold green]You[/bold green]")
                
                if not user_input.strip():
                    continue
                
                # Check for special commands
                if self.process_command(user_input):
                    break
                
                # Get response from Jarvis (will use voice output)
                self.respond(user_input)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

@app.command()
def main(
    voice: bool = typer.Option(False, "--voice", "-v", help="Enable voice mode"),
    list_voices: bool = typer.Option(False, "--list-voices", help="List available voices and exit")
):
    """
    Start Jarvis AI Assistant.
    
    By default, runs in text mode. Use --voice for voice interaction.
    """
    if list_voices:
        if not VOICE_AVAILABLE:
            console.print("[yellow]Voice modules not available.[/yellow]")
            console.print("[yellow]Install requirements-optional.txt for voice support.[/yellow]")
            return
        v = Voice()
        v.list_voices()
        return
    
    jarvis = Jarvis(voice_mode=voice)
    
    if voice and VOICE_AVAILABLE:
        jarvis.run_voice_mode()
    else:
        jarvis.run_text_mode()

if __name__ == "__main__":
    app()
