# Quick Start Guide

Get up and running with the Character Simulation Framework in just a few minutes!

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install numpy scikit-learn transformers gradio torch
```

### Step 2: Verify Installation
```python
# test_installation.py
try:
    from classes import Character, Time, Mind, Relationship, Description
    print("✅ All modules imported successfully!")
    
    # Quick test
    character = Character("Test", 25, 140, 65)
    print(f"✅ Character created: {character.get_name()}")
    print("🎉 Installation successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please check your installation.")
```

## 🎯 Your First Character

### Basic Character Creation
```python
from classes import Character, Time, Mind, Relationship, Description

# Create a character
character = Character("Emma", 25, 140, 65)

# Display basic info
print(f"Name: {character.get_name()}")
print(f"Age: {character.get_age()}")
print(f"BMI: {character.calculate_bmi()}")
print(f"Clothing Size: {character.clothing}")
```

### Add Psychology and Time
```python
# Set up time management
time_manager = Time(character, 
                   birth_day=15, birth_month=8,
                   current_year=2024, current_month=6, current_day=20)

# Create psychological profile  
mind = Mind()

# Initialize relationship tracking
relationship = Relationship()

# Generate behavioral descriptions
descriptions = Description(character)

print(f"Mood: {mind.get_mood()}")
print(f"Birthday: {time_manager.get_formatted_birth_date()}")
print(f"Relationship: {relationship.get_relationship_status()}")
```

## 🎮 Interactive Features

### Food Tracking
```python
# Add meals throughout the day
character.add_calories(450)  # Breakfast
print(f"After breakfast: {character.calculate_fullness()}")

character.add_calories(650)  # Lunch
print(f"After lunch: {character.calculate_fullness()}")

character.add_calories(800)  # Dinner
print(f"After dinner: {character.calculate_fullness()}")
print(f"Total calories: {character.get_calories()}")
```

### Relationship Interactions
```python
# Process positive interactions
relationship.calculate_sentiment_score("You look beautiful today!")
print(f"Relationship status: {relationship.get_relationship_status()}")

# Manual relationship adjustments
relationship.adjust_relationship_score(1.5)
print(f"Updated relationship: {relationship.get_relationship_status()}")
```

### Day Progression
```python
# End the day and see changes
print(f"Weight before: {character.get_weight()} lbs")
time_manager.end_day()
print(f"Weight after: {character.get_weight()} lbs")
print(f"New date: {time_manager.get_formatted_current_date()}")
print(f"New mood: {mind.get_mood()}")
```

## 🖥️ Web Interface

### Launch the GUI
```python
from script import ui

# Start the web interface
interface = ui()
interface.launch()
```

This opens a web interface at `http://localhost:7860` with tabs for:
- **Character**: Physical attributes and appearance
- **Mind**: Personality traits and moods  
- **Time**: Date management and progression
- **Parameters**: AI generation settings

## 🤖 AI Integration

### Generate Character Context
```python
from script import generate_context_prompt

# Create AI-ready character prompt
context = generate_context_prompt("Emma", "John")
print(context)
```

### Special Commands in Chat
When using with AI systems, these commands work automatically:

```python
# Food tracking: {food:calories}
user_input = "I brought you some {pizza:800} for dinner!"

# Day progression
user_input = "Time to sleep! ==END_DAY=="

# Character updates
user_input = "weight==150 age==26"
```

## 📊 Common Use Cases

### 1. Daily Life Simulation
```python
def daily_routine():
    # Morning
    character.add_calories(400)  # Breakfast
    relationship.calculate_sentiment_score("Good morning, beautiful!")
    
    # Afternoon  
    character.add_calories(600)  # Lunch
    mind.change_mood()
    
    # Evening
    character.add_calories(800)  # Dinner
    relationship.calculate_sentiment_score("I love spending time with you!")
    
    # End day
    time_manager.end_day()
    
    print("Daily routine complete!")

daily_routine()
```

### 2. Character Development Over Time
```python
def simulate_month():
    for day in range(30):
        # Random daily calories
        import random
        calories = random.randint(1800, 2500)
        character.add_calories(calories)
        
        # Random interactions
        if random.random() > 0.5:
            relationship.calculate_sentiment_score("You're wonderful!")
        
        time_manager.end_day()
    
    print(f"After 30 days:")
    print(f"Weight: {character.get_weight()} lbs")
    print(f"Relationship: {relationship.get_relationship_status()}")

simulate_month()
```

### 3. Custom Appearance
```python
def customize_character():
    character.set_eye_color("Green")
    character.set_hair("Auburn") 
    character.set_skin("Olive")
    character.set_nose("Upturned Nose")
    character.set_lips("Full Lips")
    
    print("Character customized!")
    print(f"Eyes: {character.eye_color}")
    print(f"Hair: {character.hair}")

customize_character()
```

## 🔧 Troubleshooting

### Common Issues

**ImportError: No module named 'transformers'**
```bash
pip install transformers torch
```

**Gradio interface won't start**
```bash
pip install --upgrade gradio
```

**Memory issues with AI models**
```python
# Use CPU-only mode
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
```

### Performance Tips

1. **Batch Operations**: When simulating many days, use loops efficiently
2. **Memory Management**: Create new character instances for separate simulations
3. **AI Processing**: The sentiment analysis model loads once and stays in memory

## 📚 Next Steps

1. **Read the full documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
2. **Try the examples**: [EXAMPLES.md](EXAMPLES.md)
3. **Explore the codebase**: Start with `classes.py` for core functionality
4. **Customize the framework**: Add new traits, descriptions, or features

## 🎯 Quick Examples to Try

### Relationship Progression
```python
# Watch a relationship develop
for message in ["Hi there!", "You look nice!", "I really like you!", "I love you!"]:
    relationship.calculate_sentiment_score(message)
    print(f"'{message}' → {relationship.get_relationship_status()}")
```

### Weight Change Simulation  
```python
# Simulate weight gain over time
for week in range(4):  # 4 weeks
    for day in range(7):  # 7 days per week
        character.add_calories(character.calculate_bmr() + 300)  # Excess calories
        time_manager.end_day()
    print(f"Week {week+1}: {character.get_weight()} lbs")
```

### Birthday Countdown
```python
# Count down to birthday
while time_manager.current_date.month != time_manager.birth_month or \
      time_manager.current_date.day != time_manager.birth_day:
    time_manager.end_day()
    if time_manager.current_date.month == time_manager.birth_month and \
       time_manager.current_date.day == time_manager.birth_day:
        print(f"🎂 Happy Birthday! {character.get_name()} is now {character.get_age()}!")
        break
```

---

**Ready to start building? Create your first character and explore the possibilities!** 🚀