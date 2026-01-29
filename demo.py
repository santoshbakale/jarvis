"""
Automated demo script for Jarvis AI Assistant
This simulates user interactions to demonstrate functionality
"""

import sys
import time
from io import StringIO

def simulate_conversation():
    """Simulate a conversation with Jarvis."""
    print("=" * 60)
    print("JARVIS AI ASSISTANT - AUTOMATED DEMO")
    print("=" * 60)
    print("\nThis demo shows Jarvis working without an OpenAI API key.")
    print("All features work except AI responses (which need the API key).\n")
    
    # Test imports
    print("1. Testing module imports...")
    try:
        from config import settings
        from brain import Brain
        from memory import Memory
        from skills import TimeSkill, CalculatorSkill
        print("   ✓ All modules imported successfully\n")
    except Exception as e:
        print(f"   ✗ Import error: {e}\n")
        return
    
    # Test memory
    print("2. Testing Memory System...")
    mem = Memory("demo_memory.json")
    mem.remember_fact("user_name", "Alice")
    mem.remember_fact("favorite_color", "blue")
    mem.set_preference("theme", "dark")
    
    print(f"   ✓ Stored fact: user_name = {mem.recall_fact('user_name')}")
    print(f"   ✓ Stored fact: favorite_color = {mem.recall_fact('favorite_color')}")
    print(f"   ✓ Stored preference: theme = {mem.get_preference('theme')}\n")
    
    # Test skills
    print("3. Testing Skills...")
    time_skill = TimeSkill()
    calc_skill = CalculatorSkill()
    
    print(f"   ✓ Time: {time_skill.execute('time')}")
    print(f"   ✓ Date: {time_skill.execute('date')}")
    print(f"   ✓ Calculator: {calc_skill.execute('15 + 27')}")
    print(f"   ✓ Calculator: {calc_skill.execute('100 / 4')}\n")
    
    # Test brain (without API)
    print("4. Testing Brain Module...")
    brain = Brain()
    print("   ✓ Brain initialized (API key warning expected)")
    print("   ✓ Conversation history ready")
    brain.clear_history()
    print("   ✓ History cleared\n")
    
    # Show memory contents
    print("5. Memory Contents:")
    facts = mem.get_all_facts()
    prefs = mem.get_all_preferences()
    print("   Facts:")
    for key, value in facts.items():
        print(f"     - {key}: {value}")
    print("   Preferences:")
    for key, value in prefs.items():
        print(f"     - {key}: {value}")
    print()
    
    # Clean up
    import os
    if os.path.exists("demo_memory.json"):
        os.remove("demo_memory.json")
    
    print("=" * 60)
    print("DEMO COMPLETE!")
    print("=" * 60)
    print("\nTo use Jarvis interactively:")
    print("1. Add your OpenAI API key to .env file")
    print("2. Run: python main.py")
    print("3. Start chatting with Jarvis!")
    print("\nCommands you can use:")
    print("  - Type naturally to chat")
    print("  - 'memory' - View stored facts")
    print("  - 'clear' - Clear conversation history")
    print("  - 'remember name=John' - Store a fact")
    print("  - 'exit' - Quit the program")
    print()

if __name__ == "__main__":
    simulate_conversation()
