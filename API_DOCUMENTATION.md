# Character Simulation Framework - API Documentation

## Overview

This Character Simulation Framework provides a comprehensive system for creating and managing dynamic character simulations with personality traits, physical characteristics, time progression, relationships, and psychological modeling. The framework consists of several interconnected classes that work together to create rich, interactive character experiences.

## Table of Contents

1. [Character Class](#character-class)
2. [Description Class](#description-class)
3. [Time Class](#time-class)
4. [Mind Class](#mind-class)
5. [Relationship Class](#relationship-class)
6. [Script Functions](#script-functions)
7. [Usage Examples](#usage-examples)

---

## Character Class

The `Character` class is the core component that manages all physical and basic attributes of a character.

### Constructor

```python
Character(name, age, weight, height)
```

**Parameters:**
- `name` (str): Character's name
- `age` (int): Character's age in years
- `weight` (float): Character's weight in pounds
- `height` (float): Character's height in inches

**Example:**
```python
character = Character("Emma", 25, 140, 65)
```

### Properties

- `name` (str): Character's name
- `age` (int): Character's age
- `weight` (float): Character's weight in pounds
- `height` (float): Character's height in inches
- `calories` (int): Current calorie intake for the day
- `max_calories` (float): Maximum recommended calories based on BMR
- `weight_diff` (int): Weight change tracking
- `bmi` (float): Body Mass Index
- `chest`, `waist`, `hips` (int): Body measurements in inches
- `clothing` (str): Clothing size based on measurements
- `eye_color`, `hair`, `skin` (str): Appearance attributes
- `nose`, `eye_shape`, `lips`, `cheeks`, `face`, `smile` (str): Facial features

### Core Methods

#### Physical Calculations

##### `calculate_bmi()`
Calculates and returns the character's Body Mass Index.

**Returns:** `float` - BMI value rounded to 1 decimal place

**Example:**
```python
bmi = character.calculate_bmi()
print(f"BMI: {bmi}")  # Output: BMI: 23.3
```

##### `calculate_bmi_class()`
Returns the BMI category based on the calculated BMI.

**Returns:** `str` - BMI category from BMI_CATEGORY list

**Example:**
```python
category = character.calculate_bmi_class()
print(f"BMI Category: {category}")  # Output: BMI Category: Healthy
```

##### `calculate_bmr()`
Calculates Basal Metabolic Rate using the Mifflin-St Jeor equation.

**Returns:** `float` - Daily calorie requirement

**Example:**
```python
bmr = character.calculate_bmr()
print(f"Daily calories needed: {bmr}")
```

##### `calculate_fullness()`
Determines fullness level based on calorie intake vs. BMR.

**Returns:** `str` - Fullness status from FULLNESS list

**Example:**
```python
fullness = character.calculate_fullness()
print(f"Fullness level: {fullness}")  # Output: Fullness level: Content
```

##### `calculate_height_cm()`
Converts height from inches to centimeters.

**Returns:** `float` - Height in centimeters

##### `calculate_height_feet()`
Converts height to feet and inches format.

**Returns:** `tuple` - (feet, inches)

**Example:**
```python
feet, inches = character.calculate_height_feet()
print(f"Height: {int(feet)}'{inches}\"")  # Output: Height: 5'5"
```

#### Body Measurements

##### `predict_body_dimensions()`
Predicts body measurements based on BMI using linear regression.

**Returns:** `dict` - Dictionary containing chest, waist, hips measurements and clothing size

**Example:**
```python
dimensions = character.predict_body_dimensions()
print(f"Measurements: {dimensions}")
# Output: {'Chest': 36, 'Waist': 28, 'Hips': 38, 'Clothing Size': 'Medium'}
```

##### `get_clothing_size()`
Determines clothing size based on body measurements.

**Returns:** `str` - Clothing size from X-Small to 15XL

### Setter Methods

#### Basic Attributes
- `set_name(name)`: Set character name
- `set_age(age)`: Set character age
- `set_weight(weight)`: Set character weight
- `set_height(height)`: Set character height
- `add_calories(calories)`: Add calories to daily intake
- `set_username(name)`: Set username for interactions

#### Appearance
- `set_eye_color(eye_color)`: Set eye color
- `set_nose(nose)`: Set nose type
- `set_eyes(eyes)`: Set eye shape
- `set_lips(lips)`: Set lip type
- `set_cheeks(cheeks)`: Set cheek features
- `set_face(face)`: Set face type
- `set_smile(smile)`: Set smile type
- `set_hair(hair)`: Set hair color
- `set_skin(skin)`: Set skin tone

### Getter Methods

All attributes have corresponding getter methods:
- `get_name()`, `get_age()`, `get_weight()`, `get_height()`
- `get_calories()`, `get_weight_diff()`
- `get_chest()`, `get_waist()`, `get_hips()`
- `get_username()`

### Class Constants

- `BMI_CATEGORY`: List of BMI classifications
- `FULLNESS`: List of fullness levels
- `EYE_COLORS`: Available eye colors
- `FACIAL_FEATURES`: Structured facial feature options
- `HAIR_COLORS`: Available hair colors
- `SKIN_TONES`: Available skin tones

---

## Description Class

The `Description` class generates contextual descriptions for various character behaviors and preferences.

### Constructor

```python
Description(char)
```

**Parameters:**
- `char` (Character): Character instance to generate descriptions for

### Methods

#### Random Description Generators

- `random_fetish()`: Returns random fetish-related description
- `random_feeding()`: Returns random feeding-related description
- `random_gain()`: Returns random weight gain description
- `random_sex()`: Returns random intimacy description
- `random_eating()`: Returns random eating description
- `random_eroticism()`: Returns random erotic description
- `random_partying()`: Returns random party description
- `random_binging()`: Returns random binge description
- `random_romance()`: Returns random romance description
- `random_teasing()`: Returns random teasing description
- `random_clothing_choices()`: Returns random clothing preference

#### Getter Methods

Each category has a corresponding getter:
- `get_fetish()`, `get_forced_feeding()`, `get_weight_gain()`
- `get_sex()`, `get_eating()`, `get_eroticism()`
- `get_partying()`, `get_binging()`, `get_romance()`
- `get_teasing()`, `get_clothing()`

#### Formatted Output Methods

- `formatted_fetish()`: Returns formatted fetish descriptions
- `formatted_feeding()`: Returns formatted feeding descriptions
- `formatted_weight_gain()`: Returns formatted weight gain descriptions
- `formatted_sex()`: Returns formatted intimacy descriptions
- `formatted_eating()`: Returns formatted eating descriptions
- `formatted_eroticism()`: Returns formatted erotic descriptions
- `formatted_partying()`: Returns formatted party descriptions
- `formatted_binging()`: Returns formatted binge descriptions
- `formatted_romance()`: Returns formatted romance descriptions
- `formatted_teasing()`: Returns formatted teasing descriptions
- `formatted_clothing_choices()`: Returns formatted clothing descriptions
- `formatted_all()`: Returns all descriptions formatted together

**Example:**
```python
desc = Description(character)
eating_desc = desc.get_eating()
print(eating_desc)  # Output: "Emma loves indulging in her favorite foods."

all_formatted = desc.formatted_all()
print(all_formatted)  # Output: Combined formatted descriptions
```

---

## Time Class

The `Time` class manages temporal aspects including dates, aging, and day progression.

### Constructor

```python
Time(character, birth_day, birth_month, current_year, current_month, current_day)
```

**Parameters:**
- `character` (Character): Character instance
- `birth_day` (int): Day of birth (1-31)
- `birth_month` (int): Month of birth (1-12)
- `current_year` (int): Current year
- `current_month` (int): Current month (1-12)
- `current_day` (int): Current day (1-31)

### Properties

- `current_date` (datetime): Current date object
- `birth_date` (datetime): Birth date object
- `day` (int): Game day counter
- `mind` (Mind): Associated mind instance

### Methods

#### Date Management

##### `get_current_date()`
Returns the current date as a datetime object.

##### `get_birth_date()`
Returns the birth date as a datetime object.

##### `get_formatted_current_date()`
Returns current date in human-readable format.

**Returns:** `str` - Formatted date (e.g., "June 20, 2024")

##### `get_formatted_birth_date()`
Returns birth date in human-readable format.

##### `set_current_date(new_year, new_month, new_day)`
Updates the current date.

**Parameters:**
- `new_year` (int): New year
- `new_month` (int): New month
- `new_day` (int): New day

##### `set_birth_date(new_month, new_day)`
Updates the birth date.

**Parameters:**
- `new_month` (int): New birth month
- `new_day` (int): New birth day

#### Time Progression

##### `end_day()`
Advances to the next day and processes daily changes:
- Increments current date
- Processes weight changes based on excess calories
- Handles birthday aging
- Resets daily calories
- Updates body measurements
- Changes mood

**Example:**
```python
time_manager = Time(character, 15, 8, 2024, 6, 20)
time_manager.end_day()  # Advance to next day
print(time_manager.get_formatted_current_date())  # Output: "June 21, 2024"
```

##### `get_birth_year()`
Calculates birth year based on current date and character age.

**Returns:** `int` - Calculated birth year

##### `set_day(num)`
Increments the game day counter.

**Parameters:**
- `num` (int): Number of days to add

---

## Mind Class

The `Mind` class handles psychological aspects including personality traits, moods, and preferences.

### Constructor

```python
Mind()
```

Automatically generates random traits and mood upon initialization.

### Properties

- `moods` (list): Available mood states
- `positive_mind_traits` (list): Positive psychological traits
- `negative_mind_traits` (list): Negative psychological traits
- `traits` (list): General personality traits
- `loves` (list): Things the character loves
- `hates` (list): Things the character hates
- `mind_traits` (list): Selected mind traits (6 positive + 6 negative)
- `personality_traits` (list): Selected personality traits (5 traits)
- `current_mood` (str): Current mood state

### Methods

#### Trait Generation

##### `random_mind_traits()`
Generates a combination of positive and negative mind traits.

**Returns:** `list` - Combined list of 6 positive and 6 negative traits

##### `random_personality_traits()`
Selects 5 random personality traits.

**Returns:** `list` - List of 5 personality traits

##### `random_loves()`
Selects 5 random things the character loves.

**Returns:** `list` - List of 5 loved items

##### `random_hates()`
Selects 5 random things the character hates.

**Returns:** `list` - List of 5 hated items

#### Mood Management

##### `change_mood()`
Randomly changes the current mood.

##### `get_mood()`
Returns the current mood.

**Returns:** `str` - Current mood state

#### Formatting Methods

##### `formatted_mind_traits()`
Returns mind traits formatted for prompt generation.

**Returns:** `str` - Formatted traits string

##### `formatted_personality_traits()`
Returns personality traits formatted for prompt generation.

##### `formatted_loves()`
Returns loves formatted for prompt generation.

##### `formatted_hates()`
Returns hates formatted for prompt generation.

**Example:**
```python
mind = Mind()
current_mood = mind.get_mood()
print(f"Current mood: {current_mood}")

mind.change_mood()
new_mood = mind.get_mood()
print(f"New mood: {new_mood}")

traits = mind.formatted_personality_traits()
print(f"Personality: {traits}")
```

---

## Relationship Class

The `Relationship` class manages relationship dynamics and sentiment analysis.

### Constructor

```python
Relationship()
```

Initializes with neutral relationship status and zero score.

### Properties

- `relationship_status` (str): Current relationship status
- `relationship_score` (float): Numerical relationship score (-10.0 to 10.0)

### Class Constants

- `RELATIONSHIP_STATUS`: List of relationship states from "Hatred" to "Devotion"

### Methods

#### Relationship Management

##### `get_relationship_status()`
Returns the current relationship status.

**Returns:** `str` - Current relationship status

##### `get_relationship_score()`
Returns the current relationship score.

**Returns:** `float` - Relationship score (-10.0 to 10.0)

##### `set_relationship_status(relationship_status)`
Manually sets the relationship status.

**Parameters:**
- `relationship_status` (str): New relationship status

##### `adjust_relationship_score(relationship_adjustment)`
Adjusts the relationship score and updates status accordingly.

**Parameters:**
- `relationship_adjustment` (float): Score adjustment (-10.0 to 10.0)

##### `update_relationship_status()`
Updates relationship status based on current score.

##### `calculate_relationship()`
Calculates and returns the current relationship status.

**Returns:** `str` - Current relationship status

#### Sentiment Analysis

##### `calculate_sentiment_score(string)`
Analyzes text sentiment using AI and adjusts relationship score.

**Parameters:**
- `string` (str): Text to analyze

**Score Adjustments:**
- Love: +0.1
- Joy: +0.067
- Surprise: +0.033
- Sadness: -0.033
- Fear: -0.067
- Anger: -0.1

**Example:**
```python
relationship = Relationship()
relationship.calculate_sentiment_score("I love spending time with you!")
print(relationship.get_relationship_status())  # Improved status

relationship.adjust_relationship_score(2.0)
print(f"Score: {relationship.get_relationship_score()}")
```

---

## Script Functions

The main script provides integration functions and UI components.

### State Management

#### `generate_context_prompt(name, user)`
Generates a comprehensive character context prompt for AI interactions.

**Parameters:**
- `name` (str): Character name
- `user` (str): User name

**Returns:** `str` - Formatted context prompt

#### `state_modifier(state)`
Modifies conversation state and processes special commands.

**Parameters:**
- `state` (dict): Conversation state object

**Returns:** `dict` - Modified state

#### `chat_input_modifier(text, visible_text, state)`
Processes user input for special commands and food tracking.

**Parameters:**
- `text` (str): Internal text representation
- `visible_text` (str): Visible text to user
- `state` (dict): Conversation state

**Returns:** `tuple` - (modified_text, modified_visible_text)

#### `output_modifier(string, state, is_chat=True)`
Processes AI output for sentiment analysis.

**Parameters:**
- `string` (str): AI output text
- `state` (dict): Conversation state
- `is_chat` (bool): Whether in chat mode

**Returns:** `str` - Processed output

### Special Commands

The framework supports several special commands in user input:

#### Food Tracking
```
{food_item:calories}
```
**Example:** `{pizza:800}` - Adds 800 calories of pizza to character's daily intake

#### Day Progression
```
==END_DAY==
```
Advances to the next day and processes daily changes

#### Character Updates
```
weight==150
age==26
height==66
date==2024-06-21
birth==05-15
```

### UI Functions

#### `ui()`
Creates and returns the Gradio interface for character management.

**Returns:** `gr.Blocks` - Gradio interface object

The UI includes tabs for:
- Character physical attributes
- Facial features and appearance
- Mind and personality traits
- Time and date management
- Generation parameters

---

## Usage Examples

### Basic Character Creation

```python
from classes import Character, Time, Mind, Relationship, Description

# Create a character
character = Character("Alice", 22, 125, 64)

# Set up time management
time_manager = Time(character, 10, 3, 2024, 6, 20)

# Create psychological profile
mind = Mind()

# Initialize relationship tracking
relationship = Relationship()

# Generate descriptions
descriptions = Description(character)

print(f"Character: {character.get_name()}")
print(f"BMI: {character.calculate_bmi()} ({character.calculate_bmi_class()})")
print(f"Current mood: {mind.get_mood()}")
print(f"Birth date: {time_manager.get_formatted_birth_date()}")
```

### Daily Progression Simulation

```python
# Add food intake
character.add_calories(500)  # Breakfast
character.add_calories(600)  # Lunch
character.add_calories(800)  # Dinner

print(f"Daily calories: {character.get_calories()}")
print(f"Fullness: {character.calculate_fullness()}")

# End the day
time_manager.end_day()

print(f"New date: {time_manager.get_formatted_current_date()}")
print(f"Weight change: {character.get_weight_diff()} lbs")
print(f"New mood: {mind.get_mood()}")
```

### Relationship Management

```python
# Process positive interaction
relationship.calculate_sentiment_score("You look amazing today!")
print(f"Relationship: {relationship.get_relationship_status()}")

# Manual adjustment
relationship.adjust_relationship_score(1.5)
print(f"Updated relationship: {relationship.get_relationship_status()}")
print(f"Score: {relationship.get_relationship_score()}")
```

### Dynamic Character Updates

```python
# Update physical attributes
character.set_weight(130)
character.set_age(23)

# Update appearance
character.set_hair("Blonde")
character.set_eye_color("Blue")

# Recalculate measurements
new_dimensions = character.predict_body_dimensions()
character.chest = new_dimensions['Chest']
character.waist = new_dimensions['Waist']
character.hips = new_dimensions['Hips']
character.clothing = character.get_clothing_size()

print(f"New measurements: {character.get_chest()}-{character.get_waist()}-{character.get_hips()}")
print(f"Clothing size: {character.clothing}")
```

### Context Generation for AI

```python
from script import generate_context_prompt

# Generate AI context
context = generate_context_prompt("Alice", "John")
print(context)
```

This will output a formatted character prompt suitable for AI language models, including all character attributes, relationships, and current state.

---

## Installation and Dependencies

```python
# Required packages
import datetime
import numpy as np
import random
import gradio as gr
from sklearn.linear_model import LinearRegression
from transformers import pipeline
```

### Setup

1. Install required packages:
```bash
pip install numpy scikit-learn transformers gradio torch
```

2. Import and initialize:
```python
from classes import Character, Time, Mind, Relationship, Description
```

3. Create character instances and begin simulation:
```python
character = Character("Name", age, weight, height)
time_manager = Time(character, birth_day, birth_month, current_year, current_month, current_day)
```

The framework is designed to be modular and extensible, allowing for easy integration into larger applications or standalone use for character simulation and management.