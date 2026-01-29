# Jarvis - Personal AI Assistant

A modular, extensible personal AI assistant with voice and text interaction capabilities.

## Features

- 🗣️ **Voice Interaction**: Speech-to-text and text-to-speech capabilities
- 🧠 **AI Brain**: Powered by OpenAI GPT for intelligent conversations
- 💾 **Memory System**: Remembers facts and user preferences
- 🔧 **Extensible Skills**: Plugin-based architecture for adding new capabilities
- 🎨 **Beautiful CLI**: Rich terminal interface with colors and formatting

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note for Windows users**: PyAudio installation may require additional steps:
```bash
pip install pipwin
pipwin install pyaudio
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
WAKE_WORD=jarvis
```

### 3. Run Jarvis

**Text Mode** (default):
```bash
python main.py
```

**Voice Mode**:
```bash
python main.py --voice
```

**List Available Voices**:
```bash
python main.py --list-voices
```

## Usage

### Text Mode Commands

- Type naturally to chat with Jarvis
- `exit` or `quit` - Exit the application
- `clear` - Clear conversation history
- `memory` - View stored facts and preferences
- `voices` - List available voice options
- `remember <key>=<value>` - Store a fact in memory

### Voice Mode

1. Say the wake word (default: "jarvis")
2. Wait for the listening prompt
3. Speak your command or question
4. Jarvis will respond with voice

## Project Structure

```
jarvis/
├── main.py              # Entry point and main loop
├── config.py            # Configuration management
├── brain.py             # LLM integration and reasoning
├── ears.py              # Speech-to-text (voice input)
├── voice.py             # Text-to-speech (voice output)
├── memory.py            # Long-term memory and preferences
├── skills/              # Extensible skill plugins
│   ├── base.py          # Base skill interface
│   ├── time_skill.py    # Time and date information
│   └── calculator_skill.py  # Mathematical calculations
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (create this)
```

## Adding New Skills

Create a new skill by extending `BaseSkill`:

```python
from skills.base import BaseSkill

class MySkill(BaseSkill):
    @property
    def name(self) -> str:
        return "my_skill"
    
    @property
    def description(self) -> str:
        return "What this skill does"
    
    def execute(self, *args, **kwargs):
        # Your skill logic here
        return "Result"
```

Then register it in `main.py`:

```python
self.skills["my_skill"] = MySkill()
```

## Requirements

- Python 3.10+
- OpenAI API key
- Microphone (for voice mode)
- Speakers/headphones (for voice output)

## Troubleshooting

### PyAudio Installation Issues

**Windows**: Use `pipwin install pyaudio` or download the wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

**macOS**: `brew install portaudio && pip install pyaudio`

**Linux**: `sudo apt-get install portaudio19-dev python3-pyaudio`

### Microphone Not Working

- Check system permissions for microphone access
- Verify microphone is set as default input device
- Test with: `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`

### Voice Not Speaking

- Run `python main.py --list-voices` to see available voices
- Set `VOICE_ID` in `.env` to select a specific voice

## Future Enhancements

- [ ] Integration with calendar and email
- [ ] Smart home device control
- [ ] Web search capabilities
- [ ] File system operations
- [ ] Task scheduling and reminders
- [ ] Vector database for semantic memory
- [ ] Multi-language support

## License

MIT License - Feel free to modify and extend!
