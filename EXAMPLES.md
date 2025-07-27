# Practical Examples

This document provides comprehensive examples demonstrating various use cases and advanced features of the Character Simulation Framework.

## Table of Contents

1. [Basic Character Creation](#basic-character-creation)
2. [Advanced Character Simulation](#advanced-character-simulation)
3. [Relationship Dynamics](#relationship-dynamics)
4. [Time Progression and Aging](#time-progression-and-aging)
5. [AI Integration Examples](#ai-integration-examples)
6. [Custom Extensions](#custom-extensions)
7. [Batch Processing](#batch-processing)
8. [Interactive Scenarios](#interactive-scenarios)

---

## Basic Character Creation

### Creating Your First Character

```python
from classes import Character, Time, Mind, Relationship, Description

def create_character_example():
    # Create a character with basic attributes
    character = Character("Luna", 23, 135, 66)
    
    # Display basic information
    print(f"Character Created: {character.get_name()}")
    print(f"Age: {character.get_age()} years old")
    print(f"Height: {character.get_height()} inches")
    print(f"Weight: {character.get_weight()} lbs")
    print(f"BMI: {character.calculate_bmi()} ({character.calculate_bmi_class()})")
    
    # Get body measurements
    feet, inches = character.calculate_height_feet()
    print(f"Height: {int(feet)}'{inches}\"")
    print(f"Measurements: {character.get_chest()}-{character.get_waist()}-{character.get_hips()}")
    print(f"Clothing Size: {character.clothing}")
    
    return character

# Run the example
character = create_character_example()
```

### Customizing Appearance

```python
def customize_appearance(character):
    # Set specific appearance traits
    character.set_eye_color("Green")
    character.set_hair("Auburn")
    character.set_skin("Olive")
    
    # Set facial features
    character.set_nose("Upturned Nose")
    character.set_eyes("Almond-Shaped Eyes")
    character.set_lips("Full Lips")
    character.set_cheeks("High Cheekbones")
    character.set_face("Striking Features")
    character.set_smile("Radiant Smile")
    
    print("Appearance Updated:")
    print(f"Eyes: {character.eye_color}")
    print(f"Hair: {character.hair}")
    print(f"Skin: {character.skin}")
    print(f"Features: {character.nose}, {character.eye_shape}, {character.lips}")

customize_appearance(character)
```

---

## Advanced Character Simulation

### Complete Character Setup

```python
def advanced_character_setup():
    # Create character with full setup
    character = Character("Aria", 28, 160, 64)
    
    # Set up time management
    time_manager = Time(character, 
                       birth_day=12, birth_month=4, 
                       current_year=2024, current_month=6, current_day=15)
    
    # Create psychological profile
    mind = Mind()
    
    # Initialize relationship tracking
    relationship = Relationship()
    
    # Generate descriptions
    descriptions = Description(character)
    
    # Display comprehensive character info
    print("=== COMPLETE CHARACTER PROFILE ===")
    print(f"Name: {character.get_name()}")
    print(f"Age: {character.get_age()} (Born: {time_manager.get_formatted_birth_date()})")
    print(f"Physical: {character.get_weight()} lbs, {character.calculate_height_cm()} cm")
    print(f"BMI: {character.calculate_bmi()} ({character.calculate_bmi_class()})")
    print(f"Current Date: {time_manager.get_formatted_current_date()}")
    print(f"Current Mood: {mind.get_mood()}")
    print(f"Relationship Status: {relationship.get_relationship_status()}")
    print(f"Daily Calories: {character.get_calories()}/{character.calculate_bmr():.0f}")
    print(f"Fullness: {character.calculate_fullness()}")
    
    return character, time_manager, mind, relationship, descriptions

# Create the advanced character
char, time_mgr, mind, rel, desc = advanced_character_setup()
```

### Daily Life Simulation

```python
def simulate_daily_life(character, time_manager, mind, relationship):
    print("\n=== DAILY LIFE SIMULATION ===")
    
    # Morning routine
    print("Morning:")
    character.add_calories(450)  # Breakfast
    print(f"  Breakfast consumed (450 cal) - Fullness: {character.calculate_fullness()}")
    
    # Midday interaction
    print("\nMidday:")
    relationship.calculate_sentiment_score("Good morning! You look lovely today.")
    print(f"  Positive interaction - Relationship: {relationship.get_relationship_status()}")
    
    # Lunch
    character.add_calories(650)  # Lunch
    print(f"  Lunch consumed (650 cal) - Fullness: {character.calculate_fullness()}")
    
    # Afternoon
    print("\nAfternoon:")
    mood_before = mind.get_mood()
    mind.change_mood()
    print(f"  Mood changed from {mood_before} to {mind.get_mood()}")
    
    # Dinner
    character.add_calories(800)  # Dinner
    print(f"  Dinner consumed (800 cal) - Fullness: {character.calculate_fullness()}")
    
    # Evening interaction
    relationship.calculate_sentiment_score("Thank you for such a wonderful day together!")
    print(f"  Evening gratitude - Relationship: {relationship.get_relationship_status()}")
    
    # End of day summary
    print(f"\nDay Summary:")
    print(f"  Total calories: {character.get_calories()}")
    print(f"  BMR: {character.calculate_bmr():.0f}")
    print(f"  Excess calories: {character.get_calories() - character.calculate_bmr():.0f}")
    
    # End the day
    weight_before = character.get_weight()
    time_manager.end_day()
    weight_after = character.get_weight()
    
    print(f"\n=== NEXT DAY ===")
    print(f"Date: {time_manager.get_formatted_current_date()}")
    print(f"Weight change: {weight_after - weight_before:.1f} lbs")
    print(f"New mood: {mind.get_mood()}")
    print(f"Relationship: {relationship.get_relationship_status()}")

# Run daily simulation
simulate_daily_life(char, time_mgr, mind, rel)
```

---

## Relationship Dynamics

### Relationship Progression Example

```python
def relationship_progression_demo():
    relationship = Relationship()
    
    print("=== RELATIONSHIP PROGRESSION DEMO ===")
    print(f"Starting relationship: {relationship.get_relationship_status()}")
    print(f"Starting score: {relationship.get_relationship_score()}")
    
    # Series of interactions
    interactions = [
        ("Hello there!", "Neutral greeting"),
        ("You have such beautiful eyes!", "Compliment"),
        ("I really enjoy spending time with you.", "Positive affirmation"),
        ("You're amazing and I care about you so much!", "Strong positive"),
        ("I love everything about you!", "Love expression"),
        ("You're incredible and perfect!", "Adoration"),
    ]
    
    for interaction, description in interactions:
        print(f"\nInteraction: '{interaction}' ({description})")
        old_status = relationship.get_relationship_status()
        old_score = relationship.get_relationship_score()
        
        relationship.calculate_sentiment_score(interaction)
        
        new_status = relationship.get_relationship_status()
        new_score = relationship.get_relationship_score()
        
        print(f"  Status: {old_status} → {new_status}")
        print(f"  Score: {old_score:.3f} → {new_score:.3f}")
        print(f"  Change: {new_score - old_score:+.3f}")

relationship_progression_demo()
```

### Negative Relationship Example

```python
def negative_relationship_demo():
    relationship = Relationship()
    
    print("\n=== NEGATIVE RELATIONSHIP DEMO ===")
    
    # Negative interactions
    negative_interactions = [
        "I'm really angry with you right now.",
        "You're being completely unreasonable!",
        "I hate when you act like this.",
        "You're so frustrating and annoying!",
        "I can't stand this behavior anymore!"
    ]
    
    for interaction in negative_interactions:
        old_status = relationship.get_relationship_status()
        relationship.calculate_sentiment_score(interaction)
        new_status = relationship.get_relationship_status()
        
        print(f"'{interaction}'")
        print(f"  {old_status} → {new_status}")
        print(f"  Score: {relationship.get_relationship_score():.3f}\n")

negative_relationship_demo()
```

---

## Time Progression and Aging

### Long-term Character Development

```python
def long_term_development():
    # Create a young character
    character = Character("Zoe", 18, 120, 63)
    time_manager = Time(character, 15, 9, 2024, 6, 15)  # Birthday Sept 15
    
    print("=== LONG-TERM CHARACTER DEVELOPMENT ===")
    print(f"Starting: {character.get_name()}, Age {character.get_age()}")
    print(f"Weight: {character.get_weight()} lbs, BMI: {character.calculate_bmi()}")
    
    # Simulate several years of gradual weight gain
    for year in range(5):  # 5 years
        print(f"\n--- Year {year + 1} ---")
        
        for day in range(365):  # Each day of the year
            # Simulate slightly excessive eating
            daily_excess = random.randint(100, 300)  # 100-300 excess calories
            character.add_calories(character.calculate_bmr() + daily_excess)
            
            # End each day
            time_manager.end_day()
            
            # Check for birthday
            if time_manager.current_date.month == 9 and time_manager.current_date.day == 15:
                print(f"  🎂 Birthday! Now age {character.get_age()}")
        
        # Yearly summary
        dimensions = character.predict_body_dimensions()
        character.chest = dimensions['Chest']
        character.waist = dimensions['Waist'] 
        character.hips = dimensions['Hips']
        character.clothing = character.get_clothing_size()
        
        print(f"  Age: {character.get_age()}")
        print(f"  Weight: {character.get_weight()} lbs (BMI: {character.calculate_bmi()})")
        print(f"  Measurements: {character.get_chest()}-{character.get_waist()}-{character.get_hips()}")
        print(f"  Clothing size: {character.clothing}")
        print(f"  Category: {character.calculate_bmi_class()}")

import random
long_term_development()
```

### Special Events and Birthdays

```python
def birthday_celebration():
    character = Character("Maya", 24, 140, 65)
    # Set birthday to tomorrow
    time_manager = Time(character, 20, 6, 2024, 6, 19)  # Birthday June 20, today is June 19
    
    print("=== BIRTHDAY CELEBRATION ===")
    print(f"Today: {time_manager.get_formatted_current_date()}")
    print(f"Birthday: {time_manager.get_formatted_birth_date()}")
    print(f"Current age: {character.get_age()}")
    
    # Birthday feast
    print("\n🎂 Birthday celebration with lots of food!")
    character.add_calories(800)   # Birthday breakfast
    character.add_calories(1200)  # Birthday lunch
    character.add_calories(1500)  # Birthday dinner + cake
    
    print(f"Total birthday calories: {character.get_calories()}")
    print(f"Fullness level: {character.calculate_fullness()}")
    
    # End the day (birthday!)
    time_manager.end_day()
    
    print(f"\n🎉 Happy Birthday! {character.get_name()} is now {character.get_age()} years old!")
    print(f"New date: {time_manager.get_formatted_current_date()}")
    print(f"Weight change from celebration: +{character.get_weight_diff()} lbs")

birthday_celebration()
```

---

## AI Integration Examples

### Character Context Generation

```python
def ai_context_example():
    # Create detailed character
    character = Character("Sophia", 26, 155, 67)
    character.set_eye_color("Hazel")
    character.set_hair("Chestnut")
    character.set_skin("Golden")
    character.set_username("Alex")
    
    time_manager = Time(character, 8, 3, 2024, 6, 20)
    mind = Mind()
    relationship = Relationship()
    
    # Build relationship
    relationship.adjust_relationship_score(3.5)  # Good relationship
    
    from script import generate_context_prompt
    
    print("=== AI CONTEXT GENERATION ===")
    context = generate_context_prompt("Sophia", "Alex")
    print(context)
    
    return context

ai_context = ai_context_example()
```

### Dynamic Prompt Updates

```python
def dynamic_prompt_demo():
    character = Character("Isabella", 22, 130, 64)
    time_manager = Time(character, 14, 7, 2024, 6, 20)
    relationship = Relationship()
    
    # Simulate conversation with dynamic updates
    conversations = [
        ("Good morning, beautiful!", "Starting positively"),
        ("Would you like some breakfast?", "Offering food"),
        ("You look amazing in that dress!", "Appearance compliment"),
        ("I love spending time with you", "Emotional connection")
    ]
    
    print("=== DYNAMIC PROMPT DEMO ===")
    
    for i, (message, context) in enumerate(conversations):
        print(f"\nConversation {i+1}: {context}")
        print(f"User: '{message}'")
        
        # Process sentiment
        relationship.calculate_sentiment_score(message)
        
        # Generate updated context
        from script import generate_context_prompt
        prompt = generate_context_prompt("Isabella", "User")
        
        # Show relevant parts of the prompt
        lines = prompt.split('\n')
        for line in lines:
            if 'Relationship' in line:
                print(f"  {line}")
                break

dynamic_prompt_demo()
```

---

## Custom Extensions

### Adding New Personality Traits

```python
def extend_personality_system():
    # Create character and mind
    character = Character("Nova", 25, 145, 66)
    mind = Mind()
    
    print("=== EXTENDING PERSONALITY SYSTEM ===")
    print("Original traits:", mind.formatted_personality_traits())
    
    # Add custom traits
    custom_traits = [
        "Mystical", "Tech-savvy", "Bookworm", "Night owl", 
        "Coffee addict", "Minimalist", "Ambitious", "Dreamer"
    ]
    
    mind.traits.extend(custom_traits)
    
    # Regenerate with new options
    mind.personality_traits = mind.random_personality_traits()
    
    print("Extended traits:", mind.formatted_personality_traits())
    
    # Add custom moods
    custom_moods = [
        "Contemplative", "Inspired", "Focused", "Whimsical", 
        "Determined", "Mellow", "Energized", "Zen"
    ]
    
    mind.moods.extend(custom_moods)
    mind.change_mood()
    
    print(f"New mood from extended list: {mind.get_mood()}")

extend_personality_system()
```

### Custom Description Categories

```python
def custom_descriptions():
    character = Character("Raven", 24, 140, 65)
    descriptions = Description(character)
    
    print("=== CUSTOM DESCRIPTION CATEGORIES ===")
    
    # Add hobby descriptions
    descriptions.descriptions["hobbies"] = [
        f"{character.name} loves painting watercolor landscapes.",
        f"{character.name} enjoys playing acoustic guitar.",
        f"{character.name} is passionate about photography.",
        f"{character.name} loves reading science fiction novels.",
        f"{character.name} enjoys hiking in nature.",
        f"{character.name} practices meditation daily.",
        f"{character.name} loves cooking international cuisine.",
        f"{character.name} enjoys learning new languages."
    ]
    
    # Add career descriptions  
    descriptions.descriptions["career"] = [
        f"{character.name} is dedicated to her work as a designer.",
        f"{character.name} loves the creative challenges in her job.",
        f"{character.name} is ambitious about her career goals.",
        f"{character.name} enjoys collaborating with her team.",
        f"{character.name} finds fulfillment in her professional growth."
    ]
    
    # Create getters for new categories
    def get_hobby():
        return random.choice(descriptions.descriptions["hobbies"])
    
    def get_career():
        return random.choice(descriptions.descriptions["career"])
    
    # Demonstrate new descriptions
    print("Hobby description:", get_hobby())
    print("Career description:", get_career())
    
    return descriptions

import random
custom_descriptions()
```

---

## Batch Processing

### Multiple Character Creation

```python
def create_character_batch():
    import random
    
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
    characters = []
    
    print("=== BATCH CHARACTER CREATION ===")
    
    for name in names:
        # Random attributes
        age = random.randint(18, 35)
        weight = random.randint(110, 200)
        height = random.randint(60, 72)
        
        character = Character(name, age, weight, height)
        
        # Random appearance
        character.set_eye_color(random.choice(Character.EYE_COLORS))
        character.set_hair(random.choice(Character.HAIR_COLORS))
        character.set_skin(random.choice(Character.SKIN_TONES))
        
        characters.append(character)
        
        print(f"{name}: {age}yo, {weight}lbs, {height}in, BMI:{character.calculate_bmi()}")
    
    return characters

batch_characters = create_character_batch()
```

### Group Relationship Network

```python
def group_relationship_network():
    # Create multiple characters
    characters = create_character_batch()
    
    # Create relationship matrix
    relationships = {}
    
    print("\n=== GROUP RELATIONSHIP NETWORK ===")
    
    for i, char1 in enumerate(characters):
        relationships[char1.name] = {}
        
        for j, char2 in enumerate(characters):
            if i != j:  # Don't create self-relationships
                rel = Relationship()
                # Random relationship starting point
                rel.adjust_relationship_score(random.uniform(-2, 2))
                relationships[char1.name][char2.name] = rel
    
    # Display relationship matrix
    print("\nRelationship Matrix:")
    print("From → To: Status (Score)")
    
    for char1_name in relationships:
        print(f"\n{char1_name}:")
        for char2_name in relationships[char1_name]:
            rel = relationships[char1_name][char2_name]
            print(f"  → {char2_name}: {rel.get_relationship_status()} ({rel.get_relationship_score():.2f})")

group_relationship_network()
```

---

## Interactive Scenarios

### Dating Simulation

```python
def dating_simulation():
    # Create two characters
    player_char = Character("You", 25, 160, 68)
    date_char = Character("Alex", 24, 140, 65)
    
    # Set up time and relationship
    time_manager = Time(date_char, 10, 5, 2024, 6, 20)
    relationship = Relationship()
    mind = Mind()
    
    print("=== DATING SIMULATION ===")
    print(f"You're on a date with {date_char.name}")
    print(f"Current relationship: {relationship.get_relationship_status()}")
    
    # Date scenarios
    scenarios = [
        {
            "situation": "You arrive at the restaurant",
            "choices": [
                ("You look absolutely stunning tonight!", 0.2),
                ("Thanks for meeting me here.", 0.05),
                ("Hope I'm not late!", 0.0)
            ]
        },
        {
            "situation": "Ordering food together",
            "choices": [
                ("Order whatever you'd like, it's my treat!", 0.15),
                ("Want to share an appetizer?", 0.1),
                ("I'll just have a salad.", -0.05)
            ]
        },
        {
            "situation": "Deep conversation during dinner", 
            "choices": [
                ("I really enjoy talking with you.", 0.2),
                ("You're so interesting and thoughtful.", 0.25),
                ("This food is pretty good.", 0.0)
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios):
        print(f"\n--- Scenario {i+1}: {scenario['situation']} ---")
        
        for j, (choice, impact) in enumerate(scenario['choices']):
            print(f"{j+1}. {choice}")
        
        # Simulate choice (random for demo)
        choice_idx = random.randint(0, len(scenario['choices'])-1)
        choice_text, impact = scenario['choices'][choice_idx]
        
        print(f"\nYou chose: {choice_text}")
        
        # Process choice
        relationship.adjust_relationship_score(impact)
        relationship.calculate_sentiment_score(choice_text)
        
        print(f"Relationship status: {relationship.get_relationship_status()}")
        print(f"Score: {relationship.get_relationship_score():.3f}")
    
    # End of date
    print(f"\n=== END OF DATE ===")
    final_status = relationship.get_relationship_status()
    final_score = relationship.get_relationship_score()
    
    if final_score > 2:
        print("🌟 Amazing date! They seem really interested in seeing you again!")
    elif final_score > 1:
        print("😊 Good date! There's definitely potential here.")
    elif final_score > 0:
        print("🙂 Pleasant evening, but nothing too exciting.")
    elif final_score > -1:
        print("😐 Okay date, but probably won't lead to a second one.")
    else:
        print("😞 Not a great match. Better luck next time!")

dating_simulation()
```

### Weight Management Game

```python
def weight_management_game():
    character = Character("Sam", 28, 180, 66)
    time_manager = Time(character, 15, 8, 2024, 6, 1)  # Start June 1
    
    target_weight = 160  # Goal: lose 20 lbs
    days_simulated = 0
    max_days = 90  # 3 months
    
    print("=== WEIGHT MANAGEMENT GAME ===")
    print(f"Character: {character.name}")
    print(f"Starting weight: {character.weight} lbs")
    print(f"Target weight: {target_weight} lbs")
    print(f"BMI: {character.calculate_bmi()} ({character.calculate_bmi_class()})")
    print(f"Daily BMR: {character.calculate_bmr():.0f} calories")
    print(f"Goal: Reach {target_weight} lbs in {max_days} days!")
    
    while days_simulated < max_days and character.weight > target_weight:
        days_simulated += 1
        
        # Simulate daily choices (random for demo)
        daily_calories = random.choice([
            character.calculate_bmr() - 500,  # Aggressive deficit
            character.calculate_bmr() - 300,  # Moderate deficit  
            character.calculate_bmr() - 100,  # Small deficit
            character.calculate_bmr(),        # Maintenance
            character.calculate_bmr() + 200   # Slight surplus
        ])
        
        character.calories = max(0, daily_calories)  # Can't be negative
        time_manager.end_day()
        
        # Weekly progress reports
        if days_simulated % 7 == 0:
            print(f"\nWeek {days_simulated // 7}:")
            print(f"  Weight: {character.weight} lbs (Change: {character.weight_diff:+} lbs)")
            print(f"  BMI: {character.calculate_bmi()} ({character.calculate_bmi_class()})")
            print(f"  Date: {time_manager.get_formatted_current_date()}")
    
    # Final results
    print(f"\n=== FINAL RESULTS ===")
    print(f"Days elapsed: {days_simulated}")
    print(f"Final weight: {character.weight} lbs")
    print(f"Total weight change: {character.weight_diff:+} lbs")
    print(f"BMI: {character.calculate_bmi()} ({character.calculate_bmi_class()})")
    
    if character.weight <= target_weight:
        print("🎉 Congratulations! Goal achieved!")
    else:
        print(f"😔 Goal not reached. Still need to lose {character.weight - target_weight} lbs")

weight_management_game()
```

These examples demonstrate the full range of capabilities in the Character Simulation Framework, from basic character creation to complex interactive scenarios. Each example builds upon the core functionality while showing different aspects of the system's flexibility and power.