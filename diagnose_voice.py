import pyttsx3
import speech_recognition as sr
import time

def test_speakers():
    print("\n--- Testing Speakers ---")
    try:
        engine = pyttsx3.init()
        print("Initialized TTS engine.")
        print("Saying: 'Testing speakers, one two three.'")
        engine.say("Testing speakers, one two three. If you can hear this, your speakers are working.")
        engine.runAndWait()
        print("Playback finished.")
    except Exception as e:
        print(f"Speaker Test Failed: {e}")

def test_microphone():
    print("\n--- Testing Microphone ---")
    recognizer = sr.Recognizer()
    try:
        import pyaudio
        print("PyAudio is installed.")
        
        mics = sr.Microphone.list_microphone_names()
        print("Available Microphones:")
        for i, name in enumerate(mics):
            print(f"  {i}: {name}")
            
        with sr.Microphone() as source:
            print("\nAdjusting for ambient noise... (1 second)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening for 5 seconds... Say something clearly!")
            try:
                audio = recognizer.listen(source, timeout=5)
                print("Processing audio...")
                text = recognizer.recognize_google(audio)
                print(f"Google understood: '{text}'")
            except sr.WaitTimeoutError:
                print("Error: No speech detected (Timeout).")
            except sr.UnknownValueError:
                print("Error: Could not understand audio.")
            except sr.RequestError as e:
                print(f"Error: Google API Request Error: {e}")
                
    except ImportError:
        print("Error: PyAudio is NOT installed.")
    except Exception as e:
        print(f"Microphone Test Failed: {e}")

if __name__ == "__main__":
    print("Jarvis Voice Diagnostic Tool")
    test_speakers()
    time.sleep(1)
    test_microphone()
    print("\nDiagnostic finished.")
