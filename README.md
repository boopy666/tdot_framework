diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -0,0 +1,175 @@
+# Dating Simulator with Weight Gain Mechanics
+
+A CLI-based dating simulator powered by LM Studio API featuring character progression, weight gain mechanics, and relationship dynamics.
+
+## Features
+
+🌹 **Interactive Dating Simulation**
+- Real-time conversations with AI-powered character responses
+- Dynamic relationship system that responds to player actions
+- Character personality and mood changes over time
+
+🍽️ **Weight Gain Mechanics**
+- Calorie tracking and feeding system
+- Body measurements and clothing size changes
+- BMI calculation and health status monitoring
+
+📊 **Character Progression**
+- Multiple personality traits and moods
+- Relationship status tracking
+- Save/load game functionality
+
+🎮 **CLI Interface**
+- Simple text-based commands
+- Special game commands for day progression
+- Statistics and help system
+
+## Requirements
+
+- Python 3.7+
+- LM Studio running locally
+- `requests` library (install via requirements.txt)
+
+## Setup Instructions
+
+### 1. Install Python Dependencies
+
+```bash
+pip install -r requirements.txt
+```
+
+### 2. Set Up LM Studio
+
+1. Download and install [LM Studio](https://lmstudio.ai/)
+2. Load a language model (recommended: any 7B+ parameter model for better conversations)
+3. Start the local server in LM Studio:
+   - Go to the "Local Server" tab
+   - Click "Start Server"
+   - Default URL will be `http://localhost:1234`
+
+### 3. Run the Game
+
+```bash
+python dating_simulator.py
+```
+
+## How to Play
+
+### Basic Interaction
+Simply type your messages to chat with the character naturally. The AI will respond in character.
+
+### Food System
+Offer food using the special syntax:
+```
+Want some pizza? {pizza:800}
+```
+This offers pizza with 800 calories. The character's weight and body measurements will change based on caloric intake.
+
+### Special Commands
+
+- `==END_DAY==` - Advance to the next day (processes weight gain)
+- `==STATS==` - Show detailed character statistics
+- `==HELP==` - Display help information
+- `==SAVE==` - Save your current game progress
+- `==LOAD==` - Load previously saved game
+- `==QUIT==` - Exit the game
+
+### Game Mechanics
+
+**Relationship System:**
+- Your words and actions affect the relationship score
+- Positive interactions improve the relationship
+- Negative sentiment decreases relationship status
+
+**Weight Gain System:**
+- Characters have a daily caloric requirement
+- Excess calories (500+) result in weight gain
+- Body measurements update automatically
+- Clothing sizes change as the character grows
+
+**Time Progression:**
+- Use `==END_DAY==` to advance time
+- Character mood changes daily
+- Birthday events trigger age progression
+
+## Character Information
+
+**Default Character: Maddy**
+- 19 years old gaming enthusiast
+- Introverted but yearning for connection
+- Passionate about video games and pop culture
+- Struggles with self-esteem and body image
+- Loves food and intimate moments
+
+## Customization
+
+You can modify `classes.py` to:
+- Change character starting stats
+- Add new personality traits
+- Modify food preferences
+- Adjust weight gain rates
+- Add new moods and emotions
+
+## Troubleshooting
+
+**LM Studio Connection Issues:**
+- Ensure LM Studio is running and the server is started
+- Check that the URL is `http://localhost:1234`
+- Try loading a different model if responses are poor
+
+**Game Performance:**
+- Larger language models provide better conversations
+- If responses are slow, try a smaller model
+- Adjust temperature settings in LM Studio for varied responses
+
+**Save/Load Issues:**
+- Game saves to `savegame.json` in the same directory
+- Make sure the directory is writable
+- Backup save files if switching between versions
+
+## File Structure
+
+```
+dating-simulator/
+├── dating_simulator.py    # Main game engine
+├── classes.py            # Character, time, and game mechanics
+├── requirements.txt      # Python dependencies
+├── README.md            # This file
+└── savegame.json        # Game save file (created when saving)
+```
+
+## Advanced Usage
+
+### Custom LM Studio Configuration
+
+If your LM Studio runs on a different port or server:
+
+```python
+game = DatingSimulator("http://localhost:8080")
+```
+
+### Modifying Character Traits
+
+Edit `classes.py` to customize:
+- Starting weight and measurements
+- Personality traits lists
+- Food preferences
+- Relationship progression rates
+
+## Tips for Better Gameplay
+
+1. **Be Consistent**: Stay in character for better immersion
+2. **Experiment with Food**: Different foods affect mood and weight differently  
+3. **Pay Attention to Stats**: Check `==STATS==` regularly to track progress
+4. **Save Often**: Use `==SAVE==` before major decisions
+5. **Character Development**: Watch how personality evolves over time
+
+## Contributing
+
+Feel free to fork this project and add features like:
+- Multiple characters
+- More complex relationship mechanics
+- Additional stats and progression systems
+- Different storylines and scenarios
+
+Enjoy your dating simulation adventure! 💕
