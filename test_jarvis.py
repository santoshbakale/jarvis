"""
Test script to verify all Jarvis components work correctly
"""

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from config import settings
        print("✓ config module imported")
        
        from brain import Brain
        print("✓ brain module imported")
        
        from memory import Memory
        print("✓ memory module imported")
        
        from skills import TimeSkill, CalculatorSkill
        print("✓ skills module imported")
        
        print("\nAll imports successful!")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_memory():
    """Test memory functionality."""
    print("\nTesting memory...")
    try:
        from memory import Memory
        mem = Memory("test_memory.json")
        
        # Test fact storage
        mem.remember_fact("test_key", "test_value")
        value = mem.recall_fact("test_key")
        assert value == "test_value", "Fact recall failed"
        print("✓ Fact storage and recall works")
        
        # Test preferences
        mem.set_preference("theme", "dark")
        theme = mem.get_preference("theme")
        assert theme == "dark", "Preference storage failed"
        print("✓ Preference storage works")
        
        # Clean up
        import os
        if os.path.exists("test_memory.json"):
            os.remove("test_memory.json")
        
        print("Memory tests passed!")
        return True
    except Exception as e:
        print(f"✗ Memory test failed: {e}")
        return False

def test_skills():
    """Test skill functionality."""
    print("\nTesting skills...")
    try:
        from skills import TimeSkill, CalculatorSkill
        
        # Test time skill
        time_skill = TimeSkill()
        result = time_skill.execute("time")
        print(f"✓ Time skill works: {result}")
        
        # Test calculator skill
        calc_skill = CalculatorSkill()
        result = calc_skill.execute("2 + 2")
        assert "4" in result, "Calculator failed"
        print(f"✓ Calculator skill works: {result}")
        
        print("Skill tests passed!")
        return True
    except Exception as e:
        print(f"✗ Skill test failed: {e}")
        return False

def test_brain():
    """Test brain functionality (without API key)."""
    print("\nTesting brain...")
    try:
        from brain import Brain
        brain = Brain()
        print("✓ Brain initialized (API key warning expected)")
        
        # Test history
        brain.clear_history()
        print("✓ History clearing works")
        
        print("Brain tests passed!")
        return True
    except Exception as e:
        print(f"✗ Brain test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("JARVIS COMPONENT TEST SUITE")
    print("=" * 50)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Memory", test_memory()))
    results.append(("Skills", test_skills()))
    results.append(("Brain", test_brain()))
    
    print("\n" + "=" * 50)
    print("TEST RESULTS")
    print("=" * 50)
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + ("All tests passed! ✓" if all_passed else "Some tests failed! ✗"))
