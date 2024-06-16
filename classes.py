# classes.py
import datetime
import numpy as np
import random
from sklearn.linear_model import LinearRegression
from transformers import pipeline

classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)


class Character:
    BMI_CATEGORY = ["Underweight", "Healthy", "Overweight", "Chubby", "Obese", "Super Obese", "Hyper Obese"]
    FULLNESS = ["Starving", "Hungry", "Content", "Satiated", "Stuffed", "Overfed"]
    EYE_COLORS = [
        "Amber", "Blue", "Brown", "Gray", "Green", "Hazel", "Turquoise", "Emerald", "Sapphire", "Chocolate"
    ]

    FACIAL_FEATURES = [
        {
            "type": "Nose",
            "features": ["Upturned Nose", "Straight Nose", "Pointed Nose", "Broad Nose"]
        },
        {
            "type": "Eyes",
            "features": ["Almond-Shaped Eyes", "Large Eyes", "Long Eyelashes", "Arched Eyebrows",
                         "Feline Eyes", "Doe Eyes", "Bedroom Eyes", "Sparkling Eyes", "Expressive Eyes"]
        },
        {
            "type": "Lips",
            "features": ["Pouty Lips", "Full Lips", "Cupid's Bow Lips", "Pillowy Lips"]
        },
        {
            "type": "Cheeks",
            "features": ["Dimples", "High Cheekbones", "Freckles", "Beauty Mark", "Rosy Cheeks",
                         "Sculpted Cheekbones", "Plump Cheeks"]
        },
        {
            "type": "Face",
            "features": ["Symmetrical Face", "Delicate Features", "Angelic Features", "Striking Features",
                         "Alluring Features", "Exotic Features"]
        },
        {
            "type": "Smile",
            "features": ["Radiant Smile", "Bright Smile", "Enchanting Smile", "Captivating Smile"]
        }
    ]

    HAIR_COLORS = [
        "Blonde", "Brown", "Black", "Red", "Auburn", "Strawberry Blonde", "Ginger",
        "Chestnut", "Burgundy", "Violet", "Pink", "Blue", "Green", "Platinum", "Lavender", "Turquoise"
    ]

    SKIN_TONES = [
        "Fair", "Porcelain", "Ivory", "Peach", "Olive", "Tan", "Honey", "Beige",
        "Golden", "Bronze", "Chestnut", "Mahogany", "Ebony", "Espresso", "Chocolate"
    ]

    # Extended dataset to cover sizes from X-Small to 15XL
    data = {
        'Size': ["X-Small", "Small", "Medium", "Large", "X-Large", "2XL", "3XL", "4XL", "5XL", "6XL", "7XL", "8XL",
                 "9XL", "10XL", "11XL", "12XL", "13XL", "14XL", "15XL"],
        'Chest': [29, 33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105],
        'Waist': [23.5, 25.75, 29, 33, 37, 41, 44.5, 46.5, 49.5, 52.5, 55.5, 58.5, 61.5, 64.5, 67.5, 70.5, 73.5, 76.5,
                  79.5, 82.5],
        'Hips': [33.5, 35.5, 39, 43, 47, 52.5, 54.5, 56.5, 58.5, 60.5, 62.5, 64.5, 66.5, 68.5, 70.5, 72.5, 74.5, 76.5,
                 78.5, 80.5]
    }
    # Example weights corresponding to the sizes
    weights = np.linspace(90, 300, 20).reshape(-1, 1)  # Assuming weights for sizes from X-Small to 15XL
    # Initialize a dictionary to store the models
    models = {}
    # Perform linear regression for each body measurement
    for feature in ['Chest', 'Waist', 'Hips']:
        y = np.array(data[feature])
        model = LinearRegression()
        model.fit(weights, y)
        models[feature] = model

    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.calories = 0
        self.max_calories = self.calculate_bmr()
        self.weight_diff = 0
        self.bmi = self.calculate_bmi()
        dimensions = self.predict_body_dimensions()
        self.chest = dimensions['Chest']
        self.waist = dimensions['Waist']
        self.hips = dimensions['Hips']
        self.clothing = self.get_clothing_size()
        self.eye_color = self.random_eye_color()
        self.nose = self.random_nose()
        self.eye_shape = self.random_eye_shape()
        self.lips = self.random_lips()
        self.cheeks = self.random_cheeks()
        self.face = self.random_face()
        self.smile = self.random_smile()
        self.hair = self.random_hair_color()
        self.skin = self.random_skin_color()

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_weight(self):
        return self.weight

    def get_height(self):
        return self.height

    def get_calories(self):
        return self.calories

    def get_weight_diff(self):
        return self.weight_diff

    def get_chest(self):
        return self.chest

    def get_waist(self):
        return self.waist

    def get_hips(self):
        return self.hips

    def random_nose(self):
        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Nose" for feature in d["features"]])

    def random_eye_shape(self):
        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Eyes" for feature in d["features"]])

    def random_lips(self):
        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Lips" for feature in d["features"]])

    def random_cheeks(self):
        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Cheeks" for feature in d["features"]])

    def random_face(self):
        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Face" for feature in d["features"]])

    def random_smile(self):
        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Smile" for feature in d["features"]])

    def random_eye_color(self):
        return random.choice(Character.EYE_COLORS)

    def random_hair_color(self):
        return random.choice(Character.HAIR_COLORS)

    def random_skin_color(self):
        return random.choice(Character.SKIN_TONES)

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def set_weight(self, weight):
        self.weight = weight

    def set_height(self, height):
        self.height = height

    def add_calories(self, calories):
        self.current_calories += calories

    def set_eye_color(self, eye_color):
        self.eye_color = eye_color

    def set_nose(self, nose):
        self.nose = nose

    def set_lips(self, lips):
        self.lips = lips

    def set_cheeks(self, cheeks):
        self.cheeks = cheeks

    def set_face(self, face):
        self.face = face

    def set_smile(self, smile):
        self.smile = smile

    def set_hair(self, hair):
        self.hair = hair

    def set_skin(self, skin):
        self.skin = skin

    def calculate_bmi(self):
        try:
            weight = float(self.weight)
            height = float(self.height)
            bmi_value = (weight / (height ** 2)) * 703
            return round(bmi_value, 1)
        except (ValueError, TypeError):
            print("Invalid weight or height value.")
            return None

    def calculate_bmi_class(self):
        bmi_value = self.calculate_bmi()
        thresholds = [15, 20, 25, 30, 35, 40, 50]
        for i, threshold in enumerate(thresholds):
            if bmi_value < threshold:
                return f"{Character.BMI_CATEGORY[i - 1]}"
        return f"{Character.BMI_CATEGORY[-1]}"

    def calculate_bmr(self):
        return 655 + (4.35 * self.weight) + (4.7 * self.height) - (4.7 * self.age)

    def calculate_fullness(self):
        fullness_percentage = (self.current_calories / self.max_calories) * 100
        thresholds = [20, 40, 60, 80, 100]
        for i, threshold in enumerate(thresholds):
            if fullness_percentage < threshold:
                return f"{Character.FULLNESS[i - 1]}"
        return f"{Character.FULLNESS[-1]}"

    def calculate_height_cm(self):
        return self.height * 2.54

    def calculate_height_feet(self):
        feet = self.height / 12
        inches = self.height % 12
        return feet, inches

    def predict_body_dimensions(self):
        bmi = self.calculate_bmi()

        # Define base dimensions for a woman with BMI 25 (overweight)
        base_bust = 40
        base_waist = 32
        base_hips = 42

        # Define the growth rate per 5 BMI points
        growth_rate = 4

        # Calculate the number of 5 BMI point intervals from the base BMI
        bmi_intervals = (bmi - 25) // 5

        # Calculate the estimated dimensions based on linear growth
        estimated_bust = base_bust + (bmi_intervals * growth_rate)
        estimated_waist = base_waist + (bmi_intervals * growth_rate)
        estimated_hips = base_hips + (bmi_intervals * growth_rate)

        # Generate random offsets for each dimension within the specified tolerance
        bust_offset = np.random.uniform(-1.5, 1.5)
        waist_offset = np.random.uniform(-1.5, 1.5)
        hips_offset = np.random.uniform(-1.5, 1.5)

        # Apply the random offsets to the estimated dimensions
        final_bust = estimated_bust + bust_offset
        final_waist = estimated_waist + waist_offset
        final_hips = estimated_hips + hips_offset

        # Round the final dimensions to the nearest inch
        final_bust = round(final_bust)
        final_waist = round(final_waist)
        final_hips = round(final_hips)

        # Ensure the dimensions are within realistic ranges
        final_bust = max(30, min(final_bust, 60))
        final_waist = max(24, min(final_waist, 50))
        final_hips = max(32, min(final_hips, 65))

        # Determine the clothing size based on the estimated dimensions
        sizes = ["X-Small", "Small", "Medium", "Large", "X-Large", "2XL", "3XL", "4XL", "5XL"]
        size_thresholds = [0, 35, 37, 39, 41, 43, 45, 47, 49]

        clothing_size = sizes[-1]
        for i in range(len(size_thresholds) - 1):
            if final_bust < size_thresholds[i + 1]:
                clothing_size = sizes[i]
                break

        # Return the predicted body dimensions and clothing size
        return {
            'Chest': final_bust,
            'Waist': final_waist,
            'Hips': final_hips,
            'Clothing Size': clothing_size
        }


    def get_clothing_size(self):
        # Calculate the absolute differences between character's dimensions and dataset dimensions
        chest_diff = np.abs(np.array(self.data['Chest']) - self.chest)
        waist_diff = np.abs(np.array(self.data['Waist']) - self.waist)
        hips_diff = np.abs(np.array(self.data['Hips']) - self.hips)

        # Sum the differences for each size to find the closest match
        total_diff = chest_diff + waist_diff + hips_diff

        # Find the index of the minimum difference
        closest_index = np.argmin(total_diff)

        # If the closest index is out of range, clamp it to the closest valid index
        closest_index = max(0, min(closest_index, len(self.data['Size']) - 1))

        # Return the corresponding clothing size
        return self.data['Size'][closest_index]

class Time:

    def __init__(self, character, birth_day, birth_month):
        today = datetime.date.today()
        self.current_date = datetime.datetime(today.year, today.month, today.day)
        self.day = 0
        self.character = character
        self.birth_date = datetime.datetime((self.current_date.year - character.age), birth_month, birth_day)
        self.mind = Mind()

    def get_current_date(self):
        return self.current_date

    def get_birth_date(self):
        return self.birth_date

    def get_day(self):
        return self.day

    def get_formatted_current_date(self):
        return self.current_date.strftime("%B %d, %Y")

    def get_formatted_birth_date(self):
        return self.birth_date.strftime("%B %d, %Y")

    def set_current_date(self, new_day, new_month, new_year):
        self.current_date = datetime.datetime(new_day, new_month, new_year)

    def set_birth_date(self, new_day, new_month):
        self.birth_date = datetime.datetime(new_day, new_month, (self.get_current_date.year - character.age))

    def set_day(self, num):
        self.day += num

    def end_day(self):
        self.current_date += datetime.timedelta(days=1)
        self.day += 1
        excess_calories = character.current_calories - character.calculate_bmr()
        if excess_calories > 500:
            character.weight += int(excess_calories / 500)
            character.weight_diff += int(excess_calories / 500) # Add 1 lb for every excess of 500 calories
        if self.current_date.month == self.birthday.month and self.current_date.day == self.birthday.day:
            character.age += 1
        character.calories = 0
        dimensions = character.predict_body_dimensions(character.weight)
        character.chest = dimensions['Chest']
        character.waist = dimensions['Waist']
        character.hips = dimensions['Hips']
        character.clothing = character.get_clothing_size()
        character.max_calories = character.calculate_bmr()
        self.mind.change_mood()


class Mind:
    MOODS = [
        "Happy", "Sad", "Angry", "Excited", "Anxious", "Calm", "Confused",
        "Bored", "Nervous", "Relaxed", "Content", "Frustrated", "Euphoric",
        "Melancholic", "Indifferent", "Optimistic", "Pessimistic", "Hopeful",
        "Disappointed", "Energetic", "Tired", "Irritated", "Grateful",
        "Lonely", "Motivated", "Overwhelmed", "Peaceful", "Restless",
        "Satisfied", "Surprised", "Worried", "Jealous", "Curious", "Determined",
        "Fearful", "Guilty", "Insecure", "Joyful", "Lazy", "Mischievous",
        "Proud", "Regretful", "Resentful", "Scared", "Shy", "Skeptical",
        "Sympathetic", "Thankful", "Uncomfortable", "Vulnerable", "Weary",
        "Zealous", "Horny", "Ravenous"
    ]

    POSITIVE_MIND_TRAITS = [
        "Creative", "Curious", "Determined", "Empathetic", "Enthusiastic", "Grateful",
        "Insightful", "Optimistic", "Patient", "Resilient", "Adaptable", "Adventurous",
        "Charming", "Compassionate", "Confident", "Considerate", "Courageous", "Decisive",
        "Diligent", "Encouraging", "Faithful", "Forgiving", "Generous", "Genuine",
        "Humble", "Imaginative", "Independent", "Kind", "Loyal", "Motivated",
        "Observant", "Open-Minded", "Passionate", "Reliable", "Sincere", "Supportive"
    ]

    NEGATIVE_MIND_TRAITS = [
        "Anxious", "Cynical", "Impulsive", "Insecure", "Irritable", "Jealous",
        "Moody", "Pessimistic", "Selfish", "Stubborn", "Apathetic", "Arrogant",
        "Bossy", "Cold", "Critical", "Deceitful", "Disorganized", "Distrustful",
        "Egocentric", "Envious", "Gossipy", "Greedy", "Grumpy", "Harsh",
        "Impatient", "Judgmental", "Lazy", "Manipulative", "Narrow-Minded",
        "Narcissistic", "Obsessive", "Paranoid", "Rebellious", "Rude", "Sarcastic",
        "Self-Centered", "Suspicious", "Unreliable", "Vindictive", "Playful", "Impulsive"
    ]

    TRAITS = [
        "Adventurous", "Ambitious", "Caring", "Confident", "Dependable", "Friendly",
        "Generous", "Hardworking", "Honest", "Loyal", "Modest", "Polite",
        "Responsible", "Sociable", "Thoughtful", "Understanding", "Warm", "Witty",
        "Affectionate", "Amiable", "Brave", "Calm", "Charismatic", "Cheerful",
        "Clever", "Conscientious", "Considerate", "Cooperative", "Courteous",
        "Disciplined", "Empathetic", "Encouraging", "Fair", "Forgiving",
        "Frank", "Fun-Loving", "Generous", "Gentle", "Genuine", "Gracious",
        "Helpful", "Honorable", "Humble", "Humorous", "Imaginative", "Intelligent",
        "Kind", "Knowledgeable", "Lively", "Mature", "Neat", "Optimistic",
        "Organized", "Patient", "Perceptive", "Persistent", "Practical",
        "Respectful", "Self-Confident", "Sensible", "Sensitive", "Sincere",
        "Tactful", "Trustworthy", "Understanding", "Vigilant", "Wise"
    ]

    LOVES = [
        "Feeding", "Being fed", "Big meals", "Weight gain", "Romantic dinners",
        "Lazy days", "Party nights", "Late-night snacks", "Comfort food", "Intimacy",
        "Sweet treats", "Cuddling", "Fast food", "Takeout", "Movie marathons",
        "Indulgence", "Breakfast in bed", "Pillow talk", "Morning cuddles",
        "Pizza nights", "Desserts", "Cheese platters", "Fucking", "Binge eating",
        "Wine and dine", "Cooking together", "Binge-watching", "Food delivery",
        "Brunch dates", "Bubble baths", "Pancake breakfasts", "Ice cream",
        "Chocolate", "Fried food", "Bar nights", "Dancing", "Cozy nights in",
        "Sleepovers", "Bakery visits", "Shared meals", "Lazy Sundays",
        "Breakfast buffets", "Surprise treats", "Gourmet food", "Sweet kisses",
        "Home-cooked meals", "Food festivals", "Date nights", "Picnics",
        "Midnight feasts", "Warm hugs", "Junk food", "Guilty pleasures",
        "Sensual touch", "Passionate kisses", "Intimate moments", "Erotic whispers",
        "Slow dancing", "Romantic gestures", "Candlelit dinners", "Bubble baths",
        "Massage", "Role-playing", "Dirty talk", "Lingerie", "Flirting", "Foreplay",
        "Spontaneous sex", "Public displays", "Body worship", "Holding hands",
        "Eye contact", "Playful teasing", "Soft music", "Bedtime stories", "Erotic novels",
        "Sexy photos", "Morning sex", "Shower sex", "Handcuffs", "Blindfolds",
        "Feather tickling", "Silk sheets", "Warm embraces", "Tantric sex",
        "Erotic games", "Adventurous locations", "Love letters", "Cuddling",
        "Pillow talk", "Scented candles", "Intimate conversations", "Long kisses",
        "Body oil", "Sexy surprises", "Whispers in the ear", "Erotic massages",
        "Private jokes", "Sensual dancing", "Body painting", "Touching under the table",
        "Skin contact", "Shared fantasies"
    ]

    HATES = [
        "Dieting", "Calorie counting", "Exercise", "Healthy food", "Early mornings",
        "Being judged", "Small portions", "Skipping meals", "Feeling guilty",
        "Food waste", "Hangovers", "Long work hours", "Stressful jobs",
        "Strict schedules", "Uncomfortable clothes", "Bland meals", "Crowded gyms",
        "Body shaming", "Fast-paced life", "Routine", "Plain salads",
        "Cold weather", "Loneliness", "Strict diets", "Being rushed",
        "Meal prepping", "Work deadlines", "Cooking alone", "Noise",
        "Boring people", "Bad food", "Overtime", "Being ignored",
        "Unappetizing food", "Waking up early", "Unkind people", "Rude comments",
        "Arguments", "Discomfort", "Rigid plans", "Crowds", "Unpleasant smells",
        "Insecurity", "Judgmental attitudes", "Lack of communication", "Coldness",
        "Disrespect", "Neglect", "Rejection", "Boredom", "Routine", "Lack of effort",
        "Criticism", "Dishonesty", "Cheating", "Disinterest", "Jealousy",
        "Overthinking", "Misunderstandings", "Awkward silence", "Lack of intimacy",
        "Unresolved conflicts", "Selfishness", "Insensitivity", "Lack of trust",
        "Emotional distance", "Negativity", "Impatience", "Aggressiveness",
        "Disorganization", "Unreliability", "Disharmony", "Stress", "Pressure",
        "Unkind remarks", "Unfulfilled promises", "Unappreciated", "Apathy",
        "Lack of passion", "Monotony", "Clinginess", "Over-possessiveness",
        "Unwillingness to compromise", "Criticizing appearance", "Ignoring boundaries",
        "Taking things for granted"
    ]

    def __init__(self):
        self.mind_traits = self.random_mind_traits()
        self.personality_traits = self.random_personality_traits()
        self.current_mood = random.choice(self.MOODS)
        self.loves = self.random_loves()
        self.hates = self.random_hates()

    def random_mind_traits(self):
        combined_traits = random.sample(Mind.POSITIVE_MIND_TRAITS, 6) + random.sample(Mind.NEGATIVE_MIND_TRAITS, 6)
        return random.sample(combined_traits, 5)

    def random_personality_traits(self):
        return random.sample(Mind.TRAITS, 5)

    def random_loves(self):
        return random.sample(Mind.LOVES, 5)

    def random_hates(self):
        return random.sample(Mind.HATES, 5)

    def change_mood(self):
        self.current_mood = random.choice(Mind.MOODS)

    def get_mood(self):
        return self.current_mood

    def __str__(self):
        return f"Mind Traits: {self.formatted_mind_traits()}, Personality Traits: {self.formatted_personality_traits()}, Current Mood: {self.current_mood}"

    def formatted_mind_traits(self):
        formatted_traits = [f'"{trait}"' for trait in self.mind_traits]
        return " + ".join(formatted_traits)

    def formatted_personality_traits(self):
        formatted_traits = [f'"{trait}"' for trait in self.personality_traits]
        return " + ".join(formatted_traits)

    def formatted_loves(self):
        formatted_traits = [f'"{trait}"' for trait in self.loves]
        return " + ".join(formatted_traits)

    def formatted_hates(self):
        formatted_traits = [f'"{trait}"' for trait in self.hates]
        return " + ".join(formatted_traits)


class Relationship:
    RELATIONSHIP_STATUS = [
        "Hatred", "Loathing", "Disgust", "Resentment", "Animosity", "Hostility",
        "Dislike", "Irritation", "Annoyance", "Indifference", "Neutral",
        "Curiosity", "Interest", "Affection", "Fondness", "Respect",
        "Friendship", "Attachment", "Love", "Adoration", "Devotion"
    ]

    def __init__(self):
        self.relationship_status = Relationship.RELATIONSHIP_STATUS[9]
        self.relationship_score = 0.0

    def get_relationship_status(self):
        return self.relationship_status

    def get_relationship_score(self):
        return self.relationship_score

    def set_relationship_status(self, relationship_status):
        self.relationship_status = relationship_status

    def adjust_relationship_score(self, relationship_adjustment):
        self.relationship_score += relationship_adjustment
        self.relationship_score = max(-10.0, min(10.0, self.relationship_score))  # Ensure score remains within bounds
        self.update_relationship_status()

    def update_relationship_status(self):
        thresholds = [-10.0, -9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        for i, threshold in enumerate(thresholds):
            if self.relationship_score < threshold:
                self.relationship_status = Relationship.RELATIONSHIP_STATUS[i]
                return
        self.relationship_status = Relationship.RELATIONSHIP_STATUS[-1]

    def calculate_relationship(self):
        self.update_relationship_status()
        return self.relationship_status

    def calculate_sentiment_score(self, string):
        prediction = classifier(string)
        # Unpack the emotion scores
        emotion_scores = {
            "love": prediction[0][2]["score"],
            "joy": prediction[0][1]["score"],
            "surprise": prediction[0][5]["score"],
            "sadness": prediction[0][0]["score"],
            "fear": prediction[0][4]["score"],
            "anger": prediction[0][3]["score"]
        }

        # Find the emotion with the highest score
        max_emotion = max(emotion_scores, key=emotion_scores.get)

        # Adjust the relationship score based on the max emotion
        if max_emotion == "love":
            self.adjust_relationship_score(0.1)
        elif max_emotion == "joy":
            self.adjust_relationship_score(0.067)
        elif max_emotion == "surprise":
            self.adjust_relationship_score(0.033)
        elif max_emotion == "sadness":
            self.adjust_relationship_score(-0.033)
        elif max_emotion == "fear":
            self.adjust_relationship_score(-0.067)
        elif max_emotion == "anger":
            self.adjust_relationship_score(-0.1)