# Character Simulation Framework

A comprehensive Python framework for creating and managing dynamic character simulations with realistic personality traits, physical characteristics, time progression, relationships, and psychological modeling.

## Features

### 🎭 **Dynamic Character System**
- **Physical Attributes**: Height, weight, BMI calculations, body measurements
- **Appearance Customization**: Eye color, hair, skin tone, facial features
- **Clothing Size Prediction**: Automatic sizing based on body measurements
- **Health Metrics**: BMR calculation, fullness tracking, weight progression

### 🧠 **Advanced Psychology Engine**
- **Personality Traits**: Positive and negative psychological attributes
- **Mood System**: Dynamic mood changes and tracking
- **Preferences**: Randomized loves and hates for realistic character depth
- **Behavioral Patterns**: Context-aware description generation

### ⏰ **Time Management System**
- **Calendar Integration**: Full date tracking with birthdays and aging
- **Daily Progression**: Realistic day-to-day changes and calorie processing
- **Weight Simulation**: Automatic weight changes based on caloric intake
- **Body Updates**: Dynamic measurement adjustments over time

### 💖 **Relationship Dynamics**
- **Sentiment Analysis**: AI-powered emotion detection from text interactions
- **Dynamic Scoring**: Relationship progression from hatred to devotion
- **Interactive Feedback**: Real-time relationship status updates
- **Emotional Intelligence**: Context-aware relationship adjustments

### 🖥️ **User Interface**
- **Gradio Web Interface**: Easy-to-use web-based character management
- **Real-time Updates**: Live character attribute modification
- **Tabbed Organization**: Organized interface for different character aspects
- **Parameter Control**: Adjustable AI generation settings

## Quick Start

### Installation

```bash
# Install required dependencies
pip install numpy scikit-learn transformers gradio torch
```

### Basic Usage

```python
from classes import Character, Time, Mind, Relationship, Description

# Create a character
character = Character("Emma", 25, 140, 65)

# Set up time management
time_manager = Time(character, birth_day=15, birth_month=8, 
                   current_year=2024, current_month=6, current_day=20)

# Create psychological profile
mind = Mind()

# Initialize relationship tracking
relationship = Relationship()

# Generate contextual descriptions
descriptions = Description(character)

# Display character information
print(f"Character: {character.get_name()}")
print(f"Age: {character.get_age()}")
print(f"BMI: {character.calculate_bmi()} ({character.calculate_bmi_class()})")
print(f"Current mood: {mind.get_mood()}")
print(f"Relationship status: {relationship.get_relationship_status()}")
```

### Interactive Simulation

```python
# Daily progression example
character.add_calories(600)  # Breakfast
character.add_calories(800)  # Lunch
character.add_calories(900)  # Dinner

print(f"Daily calories: {character.get_calories()}")
print(f"Fullness: {character.calculate_fullness()}")

# End the day and process changes
time_manager.end_day()

print(f"New date: {time_manager.get_formatted_current_date()}")
print(f"Weight change: {character.get_weight_diff()} lbs")
print(f"New mood: {mind.get_mood()}")
```

### Relationship Management

```python
# Process interactions with sentiment analysis
relationship.calculate_sentiment_score("You look absolutely beautiful today!")
print(f"Relationship: {relationship.get_relationship_status()}")

# Manual relationship adjustments
relationship.adjust_relationship_score(1.5)
print(f"Updated status: {relationship.get_relationship_status()}")
print(f"Score: {relationship.get_relationship_score():.2f}")
```

## Advanced Features

### Special Commands

The framework supports special commands for dynamic interaction:

#### Food Tracking
```python
# Format: {food_item:calories}
user_input = "I brought you some {pizza:800} for lunch!"
# Automatically adds 800 calories and updates fullness
```

#### Day Progression
```python
user_input = "Time to sleep! ==END_DAY=="
# Advances to next day, processes weight changes, updates mood
```

#### Character Updates
```python
# Direct character modifications
user_input = "weight==150 age==26 height==66"
# Updates character attributes dynamically
```

### Web Interface

Launch the interactive web interface:

```python
from script import ui

# Start the Gradio interface
interface = ui()
interface.launch()
```

The web interface provides:
- **Character Tab**: Physical attributes, appearance, and features
- **Mind Tab**: Personality traits, moods, and preferences
- **Time Tab**: Date management and progression tracking
- **Parameters Tab**: AI generation settings

### AI Integration

Generate comprehensive character prompts for language models:

```python
from script import generate_context_prompt

# Create detailed character context
context = generate_context_prompt("Emma", "John")
print(context)
```

Output example:
```
[character("Emma")
{
Species("Human")
Age("25 years old")
Weight("140 lbs")
BMI("23.3, Class: Healthy")
Features("Brown hair, Blue eyes, Fair skin tone, Straight Nose, Almond-Shaped Eyes, Full Lips")
Height("165 cm, 5 feet 5 inches tall")
Mind("Creative" + "Curious" + "Empathetic" + "Anxious" + "Moody")
Personality("Caring" + "Confident" + "Friendly" + "Thoughtful" + "Witty")
Mood("Happy")
Relationship("Relationship status with John is: Neutral")
...
}]
```

## Architecture

### Core Classes

1. **Character**: Manages physical attributes, health metrics, and appearance
2. **Mind**: Handles psychological traits, moods, and preferences
3. **Time**: Controls temporal progression and aging simulation
4. **Relationship**: Tracks relationship dynamics and sentiment analysis
5. **Description**: Generates contextual behavioral descriptions

### Data Flow

```
User Input → Character Updates → Time Progression → Relationship Changes → AI Context Generation
     ↓              ↓                ↓                     ↓                      ↓
Special Commands → Physical Changes → Daily Processing → Sentiment Analysis → Formatted Output
```

## Customization

### Adding New Traits

```python
# Extend personality traits
mind.traits.extend(["Adventurous", "Mysterious", "Charismatic"])

# Add custom moods
mind.moods.extend(["Euphoric", "Contemplative", "Mischievous"])

# Custom appearance options
Character.EYE_COLORS.extend(["Violet", "Gold", "Silver"])
```

### Custom Descriptions

```python
# Add new description categories
descriptions.descriptions["hobby"] = [
    f"{character.name} loves painting landscapes.",
    f"{character.name} enjoys reading mystery novels.",
    f"{character.name} practices yoga every morning."
]
```

## Use Cases

### Interactive Fiction
- Dynamic character development in narrative games
- Realistic character progression over time
- Relationship tracking between characters and players

### AI Training
- Generate diverse character prompts for language models
- Create consistent character personalities across conversations
- Simulate realistic human behavior patterns

### Social Simulation
- Model complex interpersonal relationships
- Track emotional and physical changes over time
- Create believable virtual personas

### Educational Tools
- Demonstrate psychology and human development concepts
- Teach relationship dynamics and emotional intelligence
- Simulate real-world scenarios for training purposes

## Technical Specifications

### Dependencies
- **Python 3.7+**
- **NumPy**: Numerical computations and linear regression
- **scikit-learn**: Machine learning for body measurement predictions
- **Transformers**: AI-powered sentiment analysis
- **Gradio**: Web-based user interface
- **PyTorch**: Deep learning backend for transformers

### Performance
- **Memory Usage**: ~50MB for basic character instance
- **Processing Speed**: Sub-second response times for most operations
- **Scalability**: Supports multiple concurrent character instances

### Compatibility
- **Operating Systems**: Windows, macOS, Linux
- **Python Versions**: 3.7, 3.8, 3.9, 3.10, 3.11
- **Hardware**: CPU-only operation (GPU optional for faster AI processing)

## Contributing

Contributions are welcome! Areas for enhancement:

- Additional personality trait categories
- More sophisticated relationship algorithms
- Enhanced physical simulation accuracy
- Additional AI model integrations
- Performance optimizations
- Extended customization options

## Documentation

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## License

This project is open source and available under the MIT License.

---

**Note**: This framework is designed for creative and educational purposes. Ensure appropriate content filtering and user guidelines when deploying in production environments.