diff --git a/classes.py b/classes.py
--- a/classes.py
+++ b/classes.py
@@ -1,989 +1,998 @@
-# classes.py
-import datetime
-import numpy as np
-import random
-from sklearn.linear_model import LinearRegression
-from transformers import pipeline
-
-classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)
-
-
-class Description:
-    def __init__(self, char):
-        self.char = char
-        self.descriptions = {
-            "fat_fetishism": [
-                f"{self.char.name} loves the feeling of her expanding body.",
-                f"{self.char.name} finds pleasure in her growing curves.",
-                f"{self.char.name} enjoys the attention her larger size brings.",
-                f"{self.char.name} feels sexier with every pound she gains.",
-                f"{self.char.name} loves to flaunt her fuller figure.",
-                f"{self.char.name} is turned on by the idea of getting even bigger.",
-                f"{self.char.name} admires her body in the mirror, appreciating every new roll and bulge.",
-                f"{self.char.name} loves the jiggle and bounce of her body when she moves.",
-                f"{self.char.name} finds herself more confident with every inch she adds to her waist.",
-                f"{self.char.name} feels a rush of excitement when her clothes feel tighter.",
-                f"{self.char.name} enjoys the sensation of her belly filling her lap when she sits down.",
-                f"{self.char.name} loves the softness of her body.",
-                f"{self.char.name} finds it erotic to feel her body growing.",
-                f"{self.char.name} is fascinated by the changes in her body.",
-                f"{self.char.name} loves to feel the weight of her body.",
-                f"{self.char.name} feels a thrill when she notices new stretch marks.",
-                f"{self.char.name} loves the way her body moves when she walks.",
-                f"{self.char.name} enjoys the way her body feels against her partner.",
-                f"{self.char.name} finds herself more beautiful with every pound she gains.",
-                f"{self.char.name} feels more desirable as she gets bigger."
-            ],
-            "forced_feeding": [
-                f"{self.char.name} loves being fed by {self.char.username}.",
-                f"{self.char.name} enjoys having her partner stuff her with food.",
-                f"{self.char.name} feels a thrill when {self.char.username} insists she eats more.",
-                f"{self.char.name} loves the sensation of her stomach being filled to the brim.",
-                f"{self.char.name} finds it exciting when {self.char.username} encourages her to overeat.",
-                f"{self.char.name} enjoys the feeling of being pampered and fed.",
-                f"{self.char.name} loves the indulgence of being fed by hand.",
-                f"{self.char.name} feels a rush when {self.char.username} pushes her to eat just one more bite.",
-                f"{self.char.name} enjoys the sensation of her belly growing tighter and fuller.",
-                f"{self.char.name} finds it arousing when {self.char.username} feeds her decadent treats.",
-                f"{self.char.name} loves the intimacy of being fed by {self.char.username}.",
-                f"{self.char.name} enjoys the pleasure of overindulging at {self.char.username}'s insistence.",
-                f"{self.char.name} finds herself craving more when {self.char.username} feeds her.",
-                f"{self.char.name} loves the feeling of having her partner take control of her eating.",
-                f"{self.char.name} enjoys the decadence of being spoiled with food.",
-                f"{self.char.name} finds it thrilling when {self.char.username} encourages her to eat more than she should.",
-                f"{self.char.name} loves the sensation of her stomach stretching as she eats.",
-                f"{self.char.name} enjoys the feeling of being overfed.",
-                f"{self.char.name} finds it exciting when {self.char.username} makes sure she finishes every bite.",
-                f"{self.char.name} loves the indulgence of being coaxed into eating more."
-            ],
-            "weight_gain": [
-                f"{self.char.name} enjoys watching the scale go up.",
-                f"{self.char.name} loves the feeling of outgrowing her clothes.",
-                f"{self.char.name} finds pleasure in the idea of gaining more weight.",
-                f"{self.char.name} enjoys the changes in her body as she gains weight.",
-                f"{self.char.name} loves the sensation of her body getting heavier.",
-                f"{self.char.name} finds it exciting to see new rolls and curves appear.",
-                f"{self.char.name} enjoys the process of gaining weight.",
-                f"{self.char.name} loves the way her body feels as it gets bigger.",
-                f"{self.char.name} finds herself more attractive with every pound she adds.",
-                f"{self.char.name} enjoys the fullness of her body as she gains weight.",
-                f"{self.char.name} loves the way her skin stretches to accommodate her growing size.",
-                f"{self.char.name} finds it thrilling to outgrow her favorite clothes.",
-                f"{self.char.name} enjoys the way her body jiggles as she gains weight.",
-                f"{self.char.name} loves the feeling of getting heavier.",
-                f"{self.char.name} finds pleasure in the softness of her growing body.",
-                f"{self.char.name} enjoys the new curves that come with weight gain.",
-                f"{self.char.name} loves the idea of getting even bigger.",
-                f"{self.char.name} finds it exciting to see her body change with each pound she gains.",
-                f"{self.char.name} enjoys the sensation of her body expanding.",
-                f"{self.char.name} loves the way her body feels as she continues to gain weight."
-            ],
-            "fat_sex": [
-                f"{self.char.name} loves the way her body feels during sex.",
-                f"{self.char.name} finds it exhilarating when her partner enjoys her larger size.",
-                f"{self.char.name} loves the way her body moves during intimate moments.",
-                f"{self.char.name} finds pleasure in the softness of her body during sex.",
-                f"{self.char.name} enjoys the way her partner's hands feel on her curves.",
-                f"{self.char.name} loves the sensation of her partner's hands exploring her body.",
-                f"{self.char.name} finds it exciting when her partner appreciates her growing size.",
-                f"{self.char.name} enjoys the intimacy that comes with her larger body.",
-                f"{self.char.name} loves the way her body reacts during sex.",
-                f"{self.char.name} finds pleasure in the way her body feels against her partner.",
-                f"{self.char.name} enjoys the sensation of her body being caressed.",
-                f"{self.char.name} loves the way her body moves and jiggles during intimate moments.",
-                f"{self.char.name} finds it thrilling when her partner expresses desire for her fuller figure.",
-                f"{self.char.name} enjoys the way her body responds during sex.",
-                f"{self.char.name} loves the feeling of her partner's hands on her curves.",
-                f"{self.char.name} finds it exhilarating to feel desired for her larger body.",
-                f"{self.char.name} enjoys the intimacy of being close to her partner.",
-                f"{self.char.name} loves the way her body feels during intimate moments.",
-                f"{self.char.name} finds pleasure in the softness of her body during sex.",
-                f"{self.char.name} enjoys the way her partner's hands feel on her larger body."
-            ],
-            "eating": [
-                f"{self.char.name} loves indulging in her favorite foods.",
-                f"{self.char.name} enjoys the sensation of her stomach filling up.",
-                f"{self.char.name} finds pleasure in savoring each bite.",
-                f"{self.char.name} loves the decadence of rich, creamy desserts.",
-                f"{self.char.name} enjoys the indulgence of a large meal.",
-                f"{self.char.name} finds it satisfying to eat until she is completely full.",
-                f"{self.char.name} loves the flavors and textures of her favorite dishes.",
-                f"{self.char.name} enjoys the ritual of preparing and eating a feast.",
-                f"{self.char.name} finds comfort in eating her favorite comfort foods.",
-                f"{self.char.name} loves the experience of dining out and trying new foods.",
-                f"{self.char.name} enjoys the pleasure of a well-cooked meal.",
-                f"{self.char.name} finds it thrilling to indulge in a forbidden treat.",
-                f"{self.char.name} loves the feeling of eating to her heart's content.",
-                f"{self.char.name} enjoys the sensory experience of eating.",
-                f"{self.char.name} finds satisfaction in a hearty meal.",
-                f"{self.char.name} loves the joy of eating with friends and family.",
-                f"{self.char.name} enjoys the indulgence of a snack in the middle of the night.",
-                f"{self.char.name} finds pleasure in the simple act of eating.",
-                f"{self.char.name} loves the sensation of her stomach stretching as she eats.",
-                f"{self.char.name} enjoys the feeling of fullness after a big meal."
-            ],
-            "eroticism": [
-                f"{self.char.name} loves the sensuality of her body.",
-                f"{self.char.name} finds pleasure in her own touch.",
-                f"{self.char.name} enjoys the erotic nature of her curves.",
-                f"{self.char.name} loves to explore her own body.",
-                f"{self.char.name} finds it thrilling to feel her own skin.",
-                f"{self.char.name} enjoys the sensuality of intimate moments.",
-                f"{self.char.name} loves the way her body feels in the heat of passion.",
-                f"{self.char.name} finds pleasure in the act of seduction.",
-                f"{self.char.name} enjoys the erotic tension between herself and her partner.",
-                f"{self.char.name} loves the feeling of being desired.",
-                f"{self.char.name} finds it exciting to explore her own desires.",
-                f"{self.char.name} enjoys the intimacy of being close to her partner.",
-                f"{self.char.name} loves the way her body responds to touch.",
-                f"{self.char.name} finds satisfaction in the act of lovemaking.",
-                f"{self.char.name} enjoys the pleasure of her partner's touch.",
-                f"{self.char.name} loves the sensuality of her own body.",
-                f"{self.char.name} finds it thrilling to be desired.",
-                f"{self.char.name} enjoys the eroticism of intimate moments.",
-                f"{self.char.name} loves the feeling of being close to her partner.",
-                f"{self.char.name} finds pleasure in the act of seduction."
-            ],
-            "partying": [
-                f"{self.char.name} loves to party and have a good time.",
-                f"{self.char.name} enjoys the excitement of a night out.",
-                f"{self.char.name} finds pleasure in dancing the night away.",
-                f"{self.char.name} loves the energy of a lively party.",
-                f"{self.char.name} enjoys the social aspect of partying.",
-                f"{self.char.name} finds it thrilling to meet new people.",
-                f"{self.char.name} loves the freedom of letting loose.",
-                f"{self.char.name} enjoys the fun of a good party.",
-                f"{self.char.name} finds pleasure in the music and dancing.",
-                f"{self.char.name} loves the atmosphere of a crowded club.",
-                f"{self.char.name} enjoys the excitement of a spontaneous night out.",
-                f"{self.char.name} finds it exhilarating to be the life of the party.",
-                f"{self.char.name} loves the joy of celebrating with friends.",
-                f"{self.char.name} enjoys the thrill of a big event.",
-                f"{self.char.name} finds pleasure in the chaos of a wild party.",
-                f"{self.char.name} loves the feeling of being carefree.",
-                f"{self.char.name} enjoys the social interactions at parties.",
-                f"{self.char.name} finds it exciting to be surrounded by people.",
-                f"{self.char.name} loves the fun of a themed party",
-                f"{self.char.name} finds it exciting to be surrounded by people.",
-                f"{self.char.name} loves the fun of a themed party.",
-                f"{self.char.name} enjoys the thrill of a surprise party."
-            ],
-            "binging": [
-                f"{self.char.name} loves the thrill of a binge session.",
-                f"{self.char.name} enjoys the sensation of eating non-stop.",
-                f"{self.char.name} finds pleasure in consuming large quantities of food.",
-                f"{self.char.name} loves the indulgence of a binge.",
-                f"{self.char.name} enjoys the feeling of fullness after a binge.",
-                f"{self.char.name} finds it satisfying to eat until she can't eat anymore.",
-                f"{self.char.name} loves the decadence of a food binge.",
-                f"{self.char.name} enjoys the ritual of binging on her favorite foods.",
-                f"{self.char.name} finds comfort in binging on comfort foods.",
-                f"{self.char.name} loves the experience of losing control while binging.",
-                f"{self.char.name} enjoys the pleasure of a secret binge session.",
-                f"{self.char.name} finds it thrilling to binge on forbidden foods.",
-                f"{self.char.name} loves the sensation of her stomach stretching during a binge.",
-                f"{self.char.name} enjoys the sensory overload of a binge.",
-                f"{self.char.name} finds satisfaction in a binge session.",
-                f"{self.char.name} loves the joy of eating without limits.",
-                f"{self.char.name} enjoys the indulgence of a late-night binge.",
-                f"{self.char.name} finds pleasure in the act of binging.",
-                f"{self.char.name} loves the feeling of fullness after a big binge.",
-                f"{self.char.name} enjoys the sensation of her body responding to a binge."
-            ],
-            "romance": [
-                f"{self.char.name} loves the feeling of being in love.",
-                f"{self.char.name} enjoys the intimacy of a romantic relationship.",
-                f"{self.char.name} finds pleasure in the small gestures of love.",
-                f"{self.char.name} loves the excitement of a new romance.",
-                f"{self.char.name} enjoys the comfort of a steady relationship.",
-                f"{self.char.name} finds it thrilling to be swept off her feet.",
-                f"{self.char.name} loves the warmth of a loving embrace.",
-                f"{self.char.name} enjoys the joy of spending time with her partner.",
-                f"{self.char.name} finds satisfaction in the stability of a romantic relationship.",
-                f"{self.char.name} loves the feeling of being cherished.",
-                f"{self.char.name} enjoys the pleasure of a romantic date night.",
-                f"{self.char.name} finds it exciting to be in love.",
-                f"{self.char.name} loves the sensation of her heart racing when she sees her partner.",
-                f"{self.char.name} enjoys the intimacy of shared secrets and inside jokes.",
-                f"{self.char.name} finds pleasure in the act of loving and being loved.",
-                f"{self.char.name} loves the feeling of butterflies in her stomach.",
-                f"{self.char.name} enjoys the thrill of a romantic surprise.",
-                f"{self.char.name} finds satisfaction in the connection with her partner.",
-                f"{self.char.name} loves the joy of being with someone special.",
-                f"{self.char.name} enjoys the warmth of a loving relationship."
-            ],
-            "teasing": [
-                f"{self.char.name} loves to tease with her growing curves.",
-                f"{self.char.name} enjoys the playful nature of teasing.",
-                f"{self.char.name} finds pleasure in teasing her partner.",
-                f"{self.char.name} loves the excitement of playful teasing.",
-                f"{self.char.name} enjoys the thrill of being a tease.",
-                f"{self.char.name} finds it satisfying to see her partner's reaction.",
-                f"{self.char.name} loves the fun of a good tease.",
-                f"{self.char.name} enjoys the playful banter and flirtation.",
-                f"{self.char.name} finds pleasure in the art of teasing.",
-                f"{self.char.name} loves the way her partner responds to her teasing.",
-                f"{self.char.name} enjoys the game of cat and mouse.",
-                f"{self.char.name} finds it thrilling to keep her partner on their toes.",
-                f"{self.char.name} loves the sensation of playful teasing.",
-                f"{self.char.name} enjoys the excitement of a teasing game.",
-                f"{self.char.name} finds satisfaction in the playful interaction.",
-                f"{self.char.name} loves the fun of teasing her partner.",
-                f"{self.char.name} enjoys the playful nature of teasing.",
-                f"{self.char.name} finds pleasure in the reaction she gets from teasing.",
-                f"{self.char.name} loves the thrill of being a tease.",
-                f"{self.char.name} enjoys the playful dance of tease and flirtation."
-            ],
-            "clothing_choices": [
-                f"{self.char.name} loves to wear clothes that show off her curves.",
-                f"{self.char.name} enjoys the feeling of tight clothes against her skin.",
-                f"{self.char.name} finds pleasure in dressing up.",
-                f"{self.char.name} loves the way her body looks in form-fitting clothes.",
-                f"{self.char.name} enjoys the confidence boost from wearing sexy outfits.",
-                f"{self.char.name} finds it exciting to try on new clothes.",
-                f"{self.char.name} loves the way her body fills out her clothes.",
-                f"{self.char.name} enjoys the sensation of fabrics against her skin.",
-                f"{self.char.name} finds satisfaction in a well-put-together outfit.",
-                f"{self.char.name} loves the way her clothes accentuate her body.",
-                f"{self.char.name} enjoys the thrill of shopping for new clothes.",
-                f"{self.char.name} finds pleasure in wearing clothes that make her feel sexy.",
-                f"{self.char.name} finds pleasure in wearing clothes that make her feel sexy.",
-                f"{self.char.name} loves the confidence she feels in stylish outfits.",
-                f"{self.char.name} enjoys the process of picking out the perfect outfit.",
-                f"{self.char.name} finds it thrilling to wear clothes that hug her curves.",
-                f"{self.char.name} loves the way her clothes fit as she gains weight.",
-                f"{self.char.name} enjoys the sensation of slipping into something tight and revealing.",
-                f"{self.char.name} finds satisfaction in wearing clothes that show off her figure.",
-                f"{self.char.name} loves the way her body looks in a new dress.",
-                f"{self.char.name} enjoys the excitement of wearing something new.",
-                f"{self.char.name} finds pleasure in clothes that make her feel desired.",
-                f"{self.char.name} loves the way her clothes feel as they hug her body.",
-                f"{self.char.name} enjoys the confidence that comes from wearing a great outfit.",
-                f"{self.char.name} finds it thrilling to wear something daring.",
-                f"{self.char.name} loves the way her body looks in lingerie.",
-                f"{self.char.name} enjoys the process of getting dressed up.",
-                f"{self.char.name} finds satisfaction in wearing clothes that make her feel beautiful.",
-                f"{self.char.name} loves the way her clothes fit her changing body.",
-                f"{self.char.name} enjoys the sensation of wearing something special.",
-                f"{self.char.name} finds pleasure in the way her clothes accentuate her curves.",
-                f"{self.char.name} loves the excitement of trying on different styles."
-            ]
-        }
-        self.fat_fetishism = self.random_fetish()
-        self.forced_feeding = self.random_feeding()
-        self.weight_gain = self.random_gain()
-        self.sex = self.random_sex()
-        self.eating = self.random_eating()
-        self.eroticism = self.random_eroticism()
-        self.partying = self.random_partying()
-        self.binging = self.random_binging()
-        self.romance = self.random_romance()
-        self.teasing = self.random_teasing()
-        self.clothing = self.random_clothing_choices()
-
-    def random_fetish(self):
-        return random.choice(self.descriptions['fat_fetishism'])
-
-    def random_feeding(self):
-        return random.choice(self.descriptions['forced_feeding'])
-
-    def random_gain(self):
-        return random.choice(self.descriptions['weight_gain'])
-
-    def random_sex(self):
-        return random.choice(self.descriptions['fat_sex'])
-
-    def random_eating(self):
-        return random.choice(self.descriptions['eating'])
-
-    def random_eroticism(self):
-        return random.choice(self.descriptions['eroticism'])
-
-    def random_partying(self):
-        return random.choice(self.descriptions['partying'])
-
-    def random_binging(self):
-        return random.choice(self.descriptions['binging'])
-
-    def random_romance(self):
-        return random.choice(self.descriptions['romance'])
-
-    def random_teasing(self):
-        return random.choice(self.descriptions['teasing'])
-
-    def random_clothing_choices(self):
-        return random.choice(self.descriptions['clothing_choices'])
-
-    def get_fetish(self):
-        return self.fat_fetishism
-
-    def get_forced_feeding(self):
-        return self.forced_feeding
-
-    def get_weight_gain(self):
-        return self.weight_gain
-
-    def get_sex(self):
-        return self.sex
-
-    def get_eating(self):
-        return self.eating
-
-    def get_eroticism(self):
-        return self.eroticism
-
-    def get_partying(self):
-        return self.partying
-
-    def get_binging(self):
-        return self.binging
-
-    def get_romance(self):
-        return self.romance
-
-    def get_teasing(self):
-        return self.teasing
-
-    def get_clothing(self):
-        return self.clothing
-
-    def formatted_fetish(self):
-        return ' + '.join([f'"{desc}"' for desc in self.descriptions['fat_fetishism']])
-
-    def formatted_feeding(self):
-        return ' + '.join([f'"{desc}"' for desc in self.descriptions['forced_feeding']])
-
-    def formatted_weight_gain(self):
-        return ' + '.join([f'"{desc}"' for desc in self.descriptions['weight_gain']])
-
-    def formatted_sex(self):
-        return ' + '.join([f'"{desc}"' for desc in self.descriptions['fat_sex']])
-
-    def formatted_eating(self):
-        return ' + '.join([f'"{desc}"' for desc in self.descriptions['eating']])
-
-    def formatted_eroticism(self):
-        return ' + '.join([f'"{desc}"' for desc in self.descriptions['eroticism']])
-
-    def formatted_partying(self):
-        return ' + '.join([f'"{desc}"' for desc in self.descriptions['partying']])
-
-    def formatted_binging(self):
-        return ' + '.join([f'"{desc}"' for desc in self.descriptions['binging']])
-
-    def formatted_romance(self):
-        return ' + '.join([f'"{desc}"' for desc in self.descriptions['romance']])
-
-    def formatted_teasing(self):
-        return ' + '.join([f'"{desc}"' for desc in self.descriptions['teasing']])
-
-    def formatted_clothing_choices(self):
-        return ' + '.join([f'"{desc}"' for desc in self.descriptions['clothing_choices']])
-
-    def formatted_all(self):
-        components = [
-            self.get_fetish(),
-            self.get_eating(),
-            self.get_weight_gain(),
-            self.get_sex(),
-            self.get_eating(),
-            self.get_eroticism(),
-            self.get_partying(),
-            self.get_binging(),
-            self.get_romance(),
-            self.get_teasing(),
-            self.get_clothing()
-        ]
-        formatted_components = [f'"{component}"' for component in components]
-        return ' + '.join(formatted_components)
-
-
-class Character:
-    BMI_CATEGORY = ["Underweight", "Healthy", "Overweight", "Chubby", "Obese", "Super Obese", "Hyper Obese"]
-    FULLNESS = ["Starving", "Hungry", "Content", "Satiated", "Stuffed", "Overfed"]
-    EYE_COLORS = [
-        "Amber", "Blue", "Brown", "Gray", "Green", "Hazel", "Turquoise", "Emerald", "Sapphire", "Chocolate"
-    ]
-
-    FACIAL_FEATURES = [
-        {
-            "type": "Nose",
-            "features": ["Upturned Nose", "Straight Nose", "Pointed Nose", "Broad Nose"]
-        },
-        {
-            "type": "Eyes",
-            "features": ["Almond-Shaped Eyes", "Large Eyes", "Long Eyelashes", "Arched Eyebrows",
-                         "Feline Eyes", "Doe Eyes", "Bedroom Eyes", "Sparkling Eyes", "Expressive Eyes"]
-        },
-        {
-            "type": "Lips",
-            "features": ["Pouty Lips", "Full Lips", "Cupid's Bow Lips", "Pillowy Lips"]
-        },
-        {
-            "type": "Cheeks",
-            "features": ["Dimples", "High Cheekbones", "Freckles", "Beauty Mark", "Rosy Cheeks",
-                         "Sculpted Cheekbones", "Plump Cheeks"]
-        },
-        {
-            "type": "Face",
-            "features": ["Symmetrical Face", "Delicate Features", "Angelic Features", "Striking Features",
-                         "Alluring Features", "Exotic Features"]
-        },
-        {
-            "type": "Smile",
-            "features": ["Radiant Smile", "Bright Smile", "Enchanting Smile", "Captivating Smile"]
-        }
-    ]
-
-    HAIR_COLORS = [
-        "Blonde", "Brown", "Black", "Red", "Auburn", "Strawberry Blonde", "Ginger",
-        "Chestnut", "Burgundy", "Violet", "Pink", "Blue", "Green", "Platinum", "Lavender", "Turquoise"
-    ]
-
-    SKIN_TONES = [
-        "Fair", "Porcelain", "Ivory", "Peach", "Olive", "Tan", "Honey", "Beige",
-        "Golden", "Bronze", "Chestnut", "Mahogany", "Ebony", "Espresso", "Chocolate"
-    ]
-
-    # Extended dataset to cover sizes from X-Small to 15XL
-    data = {
-        'Size': ["X-Small", "Small", "Medium", "Large", "X-Large", "2XL", "3XL", "4XL", "5XL", "6XL", "7XL", "8XL",
-                 "9XL", "10XL", "11XL", "12XL", "13XL", "14XL", "15XL"],
-        'Chest': [29, 33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105],
-        'Waist': [23.5, 25.75, 29, 33, 37, 41, 44.5, 46.5, 49.5, 52.5, 55.5, 58.5, 61.5, 64.5, 67.5, 70.5, 73.5, 76.5,
-                  79.5, 82.5],
-        'Hips': [33.5, 35.5, 39, 43, 47, 52.5, 54.5, 56.5, 58.5, 60.5, 62.5, 64.5, 66.5, 68.5, 70.5, 72.5, 74.5, 76.5,
-                 78.5, 80.5]
-    }
-    # Example weights corresponding to the sizes
-    weights = np.linspace(90, 300, 20).reshape(-1, 1)  # Assuming weights for sizes from X-Small to 15XL
-    # Initialize a dictionary to store the models
-    models = {}
-    # Perform linear regression for each body measurement
-    for feature in ['Chest', 'Waist', 'Hips']:
-        y = np.array(data[feature])
-        model = LinearRegression()
-        model.fit(weights, y)
-        models[feature] = model
-
-    def __init__(self, name, age, weight, height):
-        self.name = name
-        self.age = age
-        self.weight = weight
-        self.height = height
-        self.calories = 0
-        self.max_calories = self.calculate_bmr()
-        self.weight_diff = 0
-        self.bmi = self.calculate_bmi()
-        dimensions = self.predict_body_dimensions()
-        self.chest = dimensions['Chest']
-        self.waist = dimensions['Waist']
-        self.hips = dimensions['Hips']
-        self.clothing = self.get_clothing_size()
-        self.eye_color = self.random_eye_color()
-        self.nose = self.random_nose()
-        self.eye_shape = self.random_eye_shape()
-        self.lips = self.random_lips()
-        self.cheeks = self.random_cheeks()
-        self.face = self.random_face()
-        self.smile = self.random_smile()
-        self.hair = self.random_hair_color()
-        self.skin = self.random_skin_color()
-        self.username = ""
-
-    def get_name(self):
-        return self.name
-
-    def get_age(self):
-        return self.age
-
-    def get_weight(self):
-        return self.weight
-
-    def get_height(self):
-        return self.height
-
-    def get_calories(self):
-        return self.calories
-
-    def get_weight_diff(self):
-        return self.weight_diff
-
-    def get_chest(self):
-        return self.chest
-
-    def get_waist(self):
-        return self.waist
-
-    def get_hips(self):
-        return self.hips
-
-    def get_username(self):
-        return self.username
-
-    def random_nose(self):
-        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Nose" for feature in d["features"]])
-
-    def random_eye_shape(self):
-        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Eyes" for feature in d["features"]])
-
-    def random_lips(self):
-        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Lips" for feature in d["features"]])
-
-    def random_cheeks(self):
-        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Cheeks" for feature in d["features"]])
-
-    def random_face(self):
-        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Face" for feature in d["features"]])
-
-    def random_smile(self):
-        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Smile" for feature in d["features"]])
-
-    def random_eye_color(self):
-        return random.choice(Character.EYE_COLORS)
-
-    def random_hair_color(self):
-        return random.choice(Character.HAIR_COLORS)
-
-    def random_skin_color(self):
-        return random.choice(Character.SKIN_TONES)
-
-    def set_name(self, name):
-        self.name = name
-
-    def set_age(self, age):
-        self.age = age
-
-    def set_weight(self, weight):
-        self.weight = weight
-
-    def set_height(self, height):
-        self.height = height
-
-    def add_calories(self, calories):
-        self.calories += calories
-
-    def set_eye_color(self, eye_color):
-        self.eye_color = eye_color
-
-    def set_nose(self, nose):
-        self.nose = nose
-        
-    def set_eyes(self, eyes):
-        self.eye_shape = eyes
-
-    def set_lips(self, lips):
-        self.lips = lips
-
-    def set_cheeks(self, cheeks):
-        self.cheeks = cheeks
-
-    def set_face(self, face):
-        self.face = face
-
-    def set_smile(self, smile):
-        self.smile = smile
-
-    def set_hair(self, hair):
-        self.hair = hair
-
-    def set_skin(self, skin):
-        self.skin = skin
-
-    def set_username(self, name):
-        self.username = name
-
-    def calculate_bmi(self):
-        try:
-            weight = float(self.weight)
-            height = float(self.height)
-            bmi_value = (weight / (height ** 2)) * 703
-            return round(bmi_value, 1)
-        except (ValueError, TypeError):
-            print("Invalid weight or height value.")
-            return None
-
-    def calculate_bmi_class(self):
-        bmi_value = self.calculate_bmi()
-        thresholds = [15, 20, 25, 30, 35, 40, 50]
-        for i, threshold in enumerate(thresholds):
-            if bmi_value < threshold:
-                return f"{Character.BMI_CATEGORY[i - 1]}"
-        return f"{Character.BMI_CATEGORY[-1]}"
-
-    def calculate_bmr(self):
-        return 655 + (4.35 * self.weight) + (4.7 * self.height) - (4.7 * self.age)
-
-    def calculate_fullness(self):
-        fullness_percentage = (self.calories / self.max_calories) * 100
-        thresholds = [20, 40, 60, 80, 100]
-        for i, threshold in enumerate(thresholds):
-            if fullness_percentage < threshold:
-                return f"{Character.FULLNESS[i - 1]}"
-        return f"{Character.FULLNESS[-1]}"
-
-    def calculate_height_cm(self):
-        return self.height * 2.54
-
-    def calculate_height_feet(self):
-        feet = self.height / 12
-        inches = self.height % 12
-        return feet, inches
-
-    def predict_body_dimensions(self):
-        bmi = self.calculate_bmi()
-
-        # Define base dimensions for a woman with BMI 25 (overweight)
-        base_bust = 40
-        base_waist = 32
-        base_hips = 42
-
-        # Define the growth rate per 5 BMI points
-        growth_rate = 4
-
-        # Calculate the number of 5 BMI point intervals from the base BMI
-        bmi_intervals = (bmi - 25) // 5
-
-        # Calculate the estimated dimensions based on linear growth
-        estimated_bust = base_bust + (bmi_intervals * growth_rate)
-        estimated_waist = base_waist + (bmi_intervals * growth_rate)
-        estimated_hips = base_hips + (bmi_intervals * growth_rate)
-
-        # Generate random offsets for each dimension within the specified tolerance
-        bust_offset = np.random.uniform(-1.5, 1.5)
-        waist_offset = np.random.uniform(-1.5, 1.5)
-        hips_offset = np.random.uniform(-1.5, 1.5)
-
-        # Apply the random offsets to the estimated dimensions
-        final_bust = estimated_bust + bust_offset
-        final_waist = estimated_waist + waist_offset
-        final_hips = estimated_hips + hips_offset
-
-        # Round the final dimensions to the nearest inch
-        final_bust = round(final_bust)
-        final_waist = round(final_waist)
-        final_hips = round(final_hips)
-
-        # Ensure the dimensions are within realistic ranges
-        final_bust = max(30, min(final_bust, 60))
-        final_waist = max(24, min(final_waist, 50))
-        final_hips = max(32, min(final_hips, 65))
-
-        # Determine the clothing size based on the estimated dimensions
-        sizes = ["X-Small", "Small", "Medium", "Large", "X-Large", "2XL", "3XL", "4XL", "5XL"]
-        size_thresholds = [0, 35, 37, 39, 41, 43, 45, 47, 49]
-
-        clothing_size = sizes[-1]
-        for i in range(len(size_thresholds) - 1):
-            if final_bust < size_thresholds[i + 1]:
-                clothing_size = sizes[i]
-                break
-
-        # Return the predicted body dimensions and clothing size
-        return {
-            'Chest': final_bust,
-            'Waist': final_waist,
-            'Hips': final_hips,
-            'Clothing Size': clothing_size
-        }
-
-
-    def get_clothing_size(self):
-        # Calculate the absolute differences between character's dimensions and dataset dimensions
-        chest_diff = np.abs(np.array(self.data['Chest']) - self.chest)
-        waist_diff = np.abs(np.array(self.data['Waist']) - self.waist)
-        hips_diff = np.abs(np.array(self.data['Hips']) - self.hips)
-
-        # Sum the differences for each size to find the closest match
-        total_diff = chest_diff + waist_diff + hips_diff
-
-        # Find the index of the minimum difference
-        closest_index = np.argmin(total_diff)
-
-        # If the closest index is out of range, clamp it to the closest valid index
-        closest_index = max(0, min(closest_index, len(self.data['Size']) - 1))
-
-        # Return the corresponding clothing size
-        return self.data['Size'][closest_index]
-
-class Time:
-
-    def __init__(self, character, birth_day, birth_month, current_year, current_month, current_day):
-        self.current_year = current_year
-        self.current_month = current_month
-        self.current_day = current_day
-        self.current_date = datetime.datetime(current_year, current_month, current_day)
-        self.day = 0
-        self.character = character
-        self.birth_day = birth_day
-        self.birth_month = birth_month
-        self.birth_year = self.get_birth_year()
-        self.birth_date = datetime.datetime(self.get_birth_year(), birth_month, birth_day)
-        self.mind = Mind()
-
-    def get_current_date(self):
-        return self.current_date
-
-    def get_birth_date(self):
-        return self.birth_date
-
-    def get_day(self):
-        return self.day
-
-    def get_formatted_current_date(self):
-        return self.current_date.strftime("%B %d, %Y")
-
-    def get_formatted_birth_date(self):
-        return self.birth_date.strftime("%B %d, %Y")
-
-    def set_current_date(self, new_year, new_month, new_day):
-        self.current_date = datetime.datetime(new_year, new_month, new_day)
-
-    def get_birth_year(self):
-        return self.current_date.year - self.character.age
-
-    def set_birth_date(self, new_month, new_day):
-        try:
-            # Validate the inputs
-            if not (1 <= new_month <= 12):
-                raise ValueError(f"Invalid month: {new_month}")
-            if not (1 <= new_day <= 31):  # Basic validation, more checks needed for specific months
-                raise ValueError(f"Invalid day: {new_day}")
-
-            # Create the new birth_date
-            self.birth_date = datetime.datetime(self.get_birth_year(), new_month, new_day)
-            print(f"Birth date set to: {self.birth_date}")  # Debugging statement
-        except Exception as e:
-            print(f"Error setting birth date: {e}")
-
-    def set_day(self, num):
-        self.day += num
-
-    def end_day(self):
-        self.current_date += datetime.timedelta(days=1)
-        self.day += 1
-        excess_calories = self.character.get_calories() - self.character.calculate_bmr()
-        if excess_calories > 500:
-            self.character.weight += int(excess_calories / 500)
-            self.character.weight_diff += int(excess_calories / 500) # Add 1 lb for every excess of 500 calories
-        if self.current_month == self.birth_month and self.current_day == self.birth_day:
-            self.character.age += 1
-        self.character.calories = 0
-        dimensions = self.character.predict_body_dimensions()
-        self.character.chest = dimensions['Chest']
-        self.character.waist = dimensions['Waist']
-        self.character.hips = dimensions['Hips']
-        self.character.clothing = self.character.get_clothing_size()
-        self.character.max_calories = self.character.calculate_bmr()
-        self.mind.change_mood()
-
-
-class Mind:
-
-    def __init__(self):
-        self.moods = [
-            "Happy", "Sad", "Angry", "Excited", "Anxious", "Calm", "Confused",
-            "Bored", "Nervous", "Relaxed", "Content", "Frustrated", "Euphoric",
-            "Melancholic", "Indifferent", "Optimistic", "Pessimistic", "Hopeful",
-            "Disappointed", "Energetic", "Tired", "Irritated", "Grateful",
-            "Lonely", "Motivated", "Overwhelmed", "Peaceful", "Restless",
-            "Satisfied", "Surprised", "Worried", "Jealous", "Curious", "Determined",
-            "Fearful", "Guilty", "Insecure", "Joyful", "Lazy", "Mischievous",
-            "Proud", "Regretful", "Resentful", "Scared", "Shy", "Skeptical",
-            "Sympathetic", "Thankful", "Uncomfortable", "Vulnerable", "Weary",
-            "Zealous", "Horny", "Ravenous"
-        ]
-        self.positive_mind_traits = [
-            "Creative", "Curious", "Determined", "Empathetic", "Enthusiastic", "Grateful",
-            "Insightful", "Optimistic", "Patient", "Resilient", "Adaptable", "Adventurous",
-            "Charming", "Compassionate", "Confident", "Considerate", "Courageous", "Decisive",
-            "Diligent", "Encouraging", "Faithful", "Forgiving", "Generous", "Genuine",
-            "Humble", "Imaginative", "Independent", "Kind", "Loyal", "Motivated",
-            "Observant", "Open-Minded", "Passionate", "Reliable", "Sincere", "Supportive"
-        ]
-        self.negative_mind_traits = [
-            "Anxious", "Cynical", "Impulsive", "Insecure", "Irritable", "Jealous",
-            "Moody", "Pessimistic", "Selfish", "Stubborn", "Apathetic", "Arrogant",
-            "Bossy", "Cold", "Critical", "Deceitful", "Disorganized", "Distrustful",
-            "Egocentric", "Envious", "Gossipy", "Greedy", "Grumpy", "Harsh",
-            "Impatient", "Judgmental", "Lazy", "Manipulative", "Narrow-Minded",
-            "Narcissistic", "Obsessive", "Paranoid", "Rebellious", "Rude", "Sarcastic",
-            "Self-Centered", "Suspicious", "Unreliable", "Vindictive", "Playful", "Impulsive"
-        ]
-        self.traits = [
-            "Adventurous", "Ambitious", "Caring", "Confident", "Dependable", "Friendly",
-            "Generous", "Hardworking", "Honest", "Loyal", "Modest", "Polite",
-            "Responsible", "Sociable", "Thoughtful", "Understanding", "Warm", "Witty",
-            "Affectionate", "Amiable", "Brave", "Calm", "Charismatic", "Cheerful",
-            "Clever", "Conscientious", "Considerate", "Cooperative", "Courteous",
-            "Disciplined", "Empathetic", "Encouraging", "Fair", "Forgiving",
-            "Frank", "Fun-Loving", "Generous", "Gentle", "Genuine", "Gracious",
-            "Helpful", "Honorable", "Humble", "Humorous", "Imaginative", "Intelligent",
-            "Kind", "Knowledgeable", "Lively", "Mature", "Neat", "Optimistic",
-            "Organized", "Patient", "Perceptive", "Persistent", "Practical",
-            "Respectful", "Self-Confident", "Sensible", "Sensitive", "Sincere",
-            "Tactful", "Trustworthy", "Understanding", "Vigilant", "Wise"
-        ]
-        self.loves = [
-            "Feeding", "Being fed", "Big meals", "Weight gain", "Romantic dinners",
-            "Lazy days", "Party nights", "Late-night snacks", "Comfort food", "Intimacy",
-            "Sweet treats", "Cuddling", "Fast food", "Takeout", "Movie marathons",
-            "Indulgence", "Breakfast in bed", "Pillow talk", "Morning cuddles",
-            "Pizza nights", "Desserts", "Cheese platters", "Fucking", "Binge eating",
-            "Wine and dine", "Cooking together", "Binge-watching", "Food delivery",
-            "Brunch dates", "Bubble baths", "Pancake breakfasts", "Ice cream",
-            "Chocolate", "Fried food", "Bar nights", "Dancing", "Cozy nights in",
-            "Sleepovers", "Bakery visits", "Shared meals", "Lazy Sundays",
-            "Breakfast buffets", "Surprise treats", "Gourmet food", "Sweet kisses",
-            "Home-cooked meals", "Food festivals", "Date nights", "Picnics",
-            "Midnight feasts", "Warm hugs", "Junk food", "Guilty pleasures",
-            "Sensual touch", "Passionate kisses", "Intimate moments", "Erotic whispers",
-            "Slow dancing", "Romantic gestures", "Candlelit dinners", "Bubble baths",
-            "Massage", "Role-playing", "Dirty talk", "Lingerie", "Flirting", "Foreplay",
-            "Spontaneous sex", "Public displays", "Body worship", "Holding hands",
-            "Eye contact", "Playful teasing", "Soft music", "Bedtime stories", "Erotic novels",
-            "Sexy photos", "Morning sex", "Shower sex", "Handcuffs", "Blindfolds",
-            "Feather tickling", "Silk sheets", "Warm embraces", "Tantric sex",
-            "Erotic games", "Adventurous locations", "Love letters", "Cuddling",
-            "Pillow talk", "Scented candles", "Intimate conversations", "Long kisses",
-            "Body oil", "Sexy surprises", "Whispers in the ear", "Erotic massages",
-            "Private jokes", "Sensual dancing", "Body painting", "Touching under the table",
-            "Skin contact", "Shared fantasies"
-        ]
-        self.hates = [
-            "Dieting", "Calorie counting", "Exercise", "Healthy food", "Early mornings",
-            "Being judged", "Small portions", "Skipping meals", "Feeling guilty",
-            "Food waste", "Hangovers", "Long work hours", "Stressful jobs",
-            "Strict schedules", "Uncomfortable clothes", "Bland meals", "Crowded gyms",
-            "Body shaming", "Fast-paced life", "Routine", "Plain salads",
-            "Cold weather", "Loneliness", "Strict diets", "Being rushed",
-            "Meal prepping", "Work deadlines", "Cooking alone", "Noise",
-            "Boring people", "Bad food", "Overtime", "Being ignored",
-            "Unappetizing food", "Waking up early", "Unkind people", "Rude comments",
-            "Arguments", "Discomfort", "Rigid plans", "Crowds", "Unpleasant smells",
-            "Insecurity", "Judgmental attitudes", "Lack of communication", "Coldness",
-            "Disrespect", "Neglect", "Rejection", "Boredom", "Routine", "Lack of effort",
-            "Criticism", "Dishonesty", "Cheating", "Disinterest", "Jealousy",
-            "Overthinking", "Misunderstandings", "Awkward silence", "Lack of intimacy",
-            "Unresolved conflicts", "Selfishness", "Insensitivity", "Lack of trust",
-            "Emotional distance", "Negativity", "Impatience", "Aggressiveness",
-            "Disorganization", "Unreliability", "Disharmony", "Stress", "Pressure",
-            "Unkind remarks", "Unfulfilled promises", "Unappreciated", "Apathy",
-            "Lack of passion", "Monotony", "Clinginess", "Over-possessiveness",
-            "Unwillingness to compromise", "Criticizing appearance", "Ignoring boundaries",
-            "Taking things for granted"
-        ]
-        self.mind_traits = self.random_mind_traits()
-        self.personality_traits = self.random_personality_traits()
-        self.current_mood = random.choice(self.moods)
-        self.loves = self.random_loves()
-        self.hates = self.random_hates()
-
-    def random_mind_traits(self):
-        positive_sample_size = min(6, len(self.positive_mind_traits))
-        negative_sample_size = min(6, len(self.negative_mind_traits))
-        combined_traits = random.sample(self.positive_mind_traits, positive_sample_size) + random.sample(
-            self.negative_mind_traits, negative_sample_size)
-        return combined_traits
-
-    def random_personality_traits(self):
-        return random.sample(self.traits, 5)
-
-    def random_loves(self):
-        return random.sample(self.loves, 5)
-
-    def random_hates(self):
-        return random.sample(self.hates, 5)
-
-    def change_mood(self):
-        self.current_mood = random.choice(self.moods)
-
-    def get_mood(self):
-        return self.current_mood
-
-    def __str__(self):
-        return f"Mind Traits: {self.formatted_mind_traits()}, Personality Traits: {self.formatted_personality_traits()}, Current Mood: {self.current_mood}"
-
-    def formatted_mind_traits(self):
-        formatted_traits = [f'"{trait}"' for trait in self.mind_traits]
-        return " + ".join(formatted_traits)
-
-    def formatted_personality_traits(self):
-        formatted_traits = [f'"{trait}"' for trait in self.personality_traits]
-        return " + ".join(formatted_traits)
-
-    def formatted_loves(self):
-        formatted_traits = [f'"{trait}"' for trait in self.loves]
-        return " + ".join(formatted_traits)
-
-    def formatted_hates(self):
-        formatted_traits = [f'"{trait}"' for trait in self.hates]
-        return " + ".join(formatted_traits)
-
-
-class Relationship:
-    RELATIONSHIP_STATUS = [
-        "Hatred", "Loathing", "Disgust", "Resentment", "Animosity", "Hostility",
-        "Dislike", "Irritation", "Annoyance", "Indifference", "Neutral",
-        "Curiosity", "Interest", "Affection", "Fondness", "Respect",
-        "Friendship", "Attachment", "Love", "Adoration", "Devotion"
-    ]
-
-    def __init__(self):
-        self.relationship_status = Relationship.RELATIONSHIP_STATUS[9]
-        self.relationship_score = 0.0
-
-    def get_relationship_status(self):
-        return self.relationship_status
-
-    def get_relationship_score(self):
-        return self.relationship_score
-
-    def set_relationship_status(self, relationship_status):
-        self.relationship_status = relationship_status
-
-    def adjust_relationship_score(self, relationship_adjustment):
-        self.relationship_score += relationship_adjustment
-        self.relationship_score = max(-10.0, min(10.0, self.relationship_score))  # Ensure score remains within bounds
-        self.update_relationship_status()
-
-    def update_relationship_status(self):
-        thresholds = [-10.0, -9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
-        for i, threshold in enumerate(thresholds):
-            if self.relationship_score < threshold:
-                self.relationship_status = Relationship.RELATIONSHIP_STATUS[i]
-                return
-        self.relationship_status = Relationship.RELATIONSHIP_STATUS[-1]
-
-    def calculate_relationship(self):
-        self.update_relationship_status()
-        return self.relationship_status
-
-    def calculate_sentiment_score(self, string):
-        prediction = classifier(string)
-        # Unpack the emotion scores
-        emotion_scores = {
-            "love": prediction[0][2]["score"],
-            "joy": prediction[0][1]["score"],
-            "surprise": prediction[0][5]["score"],
-            "sadness": prediction[0][0]["score"],
-            "fear": prediction[0][4]["score"],
-            "anger": prediction[0][3]["score"]
-        }
-
-        # Find the emotion with the highest score
-        max_emotion = max(emotion_scores, key=emotion_scores.get)
-
-        # Adjust the relationship score based on the max emotion
-        if max_emotion == "love":
-            self.adjust_relationship_score(0.1)
-        elif max_emotion == "joy":
-            self.adjust_relationship_score(0.067)
-        elif max_emotion == "surprise":
-            self.adjust_relationship_score(0.033)
-        elif max_emotion == "sadness":
-            self.adjust_relationship_score(-0.033)
-        elif max_emotion == "fear":
-            self.adjust_relationship_score(-0.067)
-        elif max_emotion == "anger":
-            self.adjust_relationship_score(-0.1)
+# classes.py
+import datetime
+import random
+import math
+
+# Simple emotion detection without external dependencies
+EMOTION_KEYWORDS = {
+    'love': ['love', 'adore', 'cherish', 'treasure', 'heart', 'beautiful', 'gorgeous', 'amazing'],
+    'joy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'awesome', 'fantastic', 'laugh'],
+    'surprise': ['wow', 'surprise', 'unexpected', 'amazing', 'incredible', 'unbelievable'],
+    'sadness': ['sad', 'disappointed', 'upset', 'hurt', 'cry', 'terrible', 'awful'],
+    'fear': ['scared', 'afraid', 'worried', 'nervous', 'anxious', 'terrified'],
+    'anger': ['angry', 'mad', 'furious', 'hate', 'stupid', 'idiot', 'annoying', 'disgusting']
+}
+
+def simple_emotion_classifier(text):
+    """Simple keyword-based emotion classification"""
+    text_lower = text.lower()
+    emotion_scores = {emotion: 0 for emotion in EMOTION_KEYWORDS}
+    
+    for emotion, keywords in EMOTION_KEYWORDS.items():
+        for keyword in keywords:
+            if keyword in text_lower:
+                emotion_scores[emotion] += 1
+    
+    # Normalize scores
+    total_matches = sum(emotion_scores.values())
+    if total_matches > 0:
+        emotion_scores = {k: v/total_matches for k, v in emotion_scores.items()}
+    else:
+        # Default neutral emotion distribution
+        emotion_scores = {emotion: 1/6 for emotion in EMOTION_KEYWORDS}
+    
+    return emotion_scores
+
+
+class Description:
+    def __init__(self, char):
+        self.char = char
+        self.descriptions = {
+            "fat_fetishism": [
+                f"{self.char.name} loves the feeling of her expanding body.",
+                f"{self.char.name} finds pleasure in her growing curves.",
+                f"{self.char.name} enjoys the attention her larger size brings.",
+                f"{self.char.name} feels sexier with every pound she gains.",
+                f"{self.char.name} loves to flaunt her fuller figure.",
+                f"{self.char.name} is turned on by the idea of getting even bigger.",
+                f"{self.char.name} admires her body in the mirror, appreciating every new roll and bulge.",
+                f"{self.char.name} loves the jiggle and bounce of her body when she moves.",
+                f"{self.char.name} finds herself more confident with every inch she adds to her waist.",
+                f"{self.char.name} feels a rush of excitement when her clothes feel tighter.",
+                f"{self.char.name} enjoys the sensation of her belly filling her lap when she sits down.",
+                f"{self.char.name} loves the softness of her body.",
+                f"{self.char.name} finds it erotic to feel her body growing.",
+                f"{self.char.name} is fascinated by the changes in her body.",
+                f"{self.char.name} loves to feel the weight of her body.",
+                f"{self.char.name} feels a thrill when she notices new stretch marks.",
+                f"{self.char.name} loves the way her body moves when she walks.",
+                f"{self.char.name} enjoys the way her body feels against her partner.",
+                f"{self.char.name} finds herself more beautiful with every pound she gains.",
+                f"{self.char.name} feels more desirable as she gets bigger."
+            ],
+            "forced_feeding": [
+                f"{self.char.name} loves being fed by {self.char.username}.",
+                f"{self.char.name} enjoys having her partner stuff her with food.",
+                f"{self.char.name} feels a thrill when {self.char.username} insists she eats more.",
+                f"{self.char.name} loves the sensation of her stomach being filled to the brim.",
+                f"{self.char.name} finds it exciting when {self.char.username} encourages her to overeat.",
+                f"{self.char.name} enjoys the feeling of being pampered and fed.",
+                f"{self.char.name} loves the indulgence of being fed by hand.",
+                f"{self.char.name} feels a rush when {self.char.username} pushes her to eat just one more bite.",
+                f"{self.char.name} enjoys the sensation of her belly growing tighter and fuller.",
+                f"{self.char.name} finds it arousing when {self.char.username} feeds her decadent treats.",
+                f"{self.char.name} loves the intimacy of being fed by {self.char.username}.",
+                f"{self.char.name} enjoys the pleasure of overindulging at {self.char.username}'s insistence.",
+                f"{self.char.name} finds herself craving more when {self.char.username} feeds her.",
+                f"{self.char.name} loves the feeling of having her partner take control of her eating.",
+                f"{self.char.name} enjoys the decadence of being spoiled with food.",
+                f"{self.char.name} finds it thrilling when {self.char.username} encourages her to eat more than she should.",
+                f"{self.char.name} loves the sensation of her stomach stretching as she eats.",
+                f"{self.char.name} enjoys the feeling of being overfed.",
+                f"{self.char.name} finds it exciting when {self.char.username} makes sure she finishes every bite.",
+                f"{self.char.name} loves the indulgence of being coaxed into eating more."
+            ],
+            "weight_gain": [
+                f"{self.char.name} enjoys watching the scale go up.",
+                f"{self.char.name} loves the feeling of outgrowing her clothes.",
+                f"{self.char.name} finds pleasure in the idea of gaining more weight.",
+                f"{self.char.name} enjoys the changes in her body as she gains weight.",
+                f"{self.char.name} loves the sensation of her body getting heavier.",
+                f"{self.char.name} finds it exciting to see new rolls and curves appear.",
+                f"{self.char.name} enjoys the process of gaining weight.",
+                f"{self.char.name} loves the way her body feels as it gets bigger.",
+                f"{self.char.name} finds herself more attractive with every pound she adds.",
+                f"{self.char.name} enjoys the fullness of her body as she gains weight.",
+                f"{self.char.name} loves the way her skin stretches to accommodate her growing size.",
+                f"{self.char.name} finds it thrilling to outgrow her favorite clothes.",
+                f"{self.char.name} enjoys the way her body jiggles as she gains weight.",
+                f"{self.char.name} loves the feeling of getting heavier.",
+                f"{self.char.name} finds pleasure in the softness of her growing body.",
+                f"{self.char.name} enjoys the new curves that come with weight gain.",
+                f"{self.char.name} loves the idea of getting even bigger.",
+                f"{self.char.name} finds it exciting to see her body change with each pound she gains.",
+                f"{self.char.name} enjoys the sensation of her body expanding.",
+                f"{self.char.name} loves the way her body feels as she continues to gain weight."
+            ],
+            "fat_sex": [
+                f"{self.char.name} loves the way her body feels during sex.",
+                f"{self.char.name} finds it exhilarating when her partner enjoys her larger size.",
+                f"{self.char.name} loves the way her body moves during intimate moments.",
+                f"{self.char.name} finds pleasure in the softness of her body during sex.",
+                f"{self.char.name} enjoys the way her partner's hands feel on her curves.",
+                f"{self.char.name} loves the sensation of her partner's hands exploring her body.",
+                f"{self.char.name} finds it exciting when her partner appreciates her growing size.",
+                f"{self.char.name} enjoys the intimacy that comes with her larger body.",
+                f"{self.char.name} loves the way her body reacts during sex.",
+                f"{self.char.name} finds pleasure in the way her body feels against her partner.",
+                f"{self.char.name} enjoys the sensation of her body being caressed.",
+                f"{self.char.name} loves the way her body moves and jiggles during intimate moments.",
+                f"{self.char.name} finds it thrilling when her partner expresses desire for her fuller figure.",
+                f"{self.char.name} enjoys the way her body responds during sex.",
+                f"{self.char.name} loves the feeling of her partner's hands on her curves.",
+                f"{self.char.name} finds it exhilarating to feel desired for her larger body.",
+                f"{self.char.name} enjoys the intimacy of being close to her partner.",
+                f"{self.char.name} loves the way her body feels during intimate moments.",
+                f"{self.char.name} finds pleasure in the softness of her body during sex.",
+                f"{self.char.name} enjoys the way her partner's hands feel on her larger body."
+            ],
+            "eating": [
+                f"{self.char.name} loves indulging in her favorite foods.",
+                f"{self.char.name} enjoys the sensation of her stomach filling up.",
+                f"{self.char.name} finds pleasure in savoring each bite.",
+                f"{self.char.name} loves the decadence of rich, creamy desserts.",
+                f"{self.char.name} enjoys the indulgence of a large meal.",
+                f"{self.char.name} finds it satisfying to eat until she is completely full.",
+                f"{self.char.name} loves the flavors and textures of her favorite dishes.",
+                f"{self.char.name} enjoys the ritual of preparing and eating a feast.",
+                f"{self.char.name} finds comfort in eating her favorite comfort foods.",
+                f"{self.char.name} loves the experience of dining out and trying new foods.",
+                f"{self.char.name} enjoys the pleasure of a well-cooked meal.",
+                f"{self.char.name} finds it thrilling to indulge in a forbidden treat.",
+                f"{self.char.name} loves the feeling of eating to her heart's content.",
+                f"{self.char.name} enjoys the sensory experience of eating.",
+                f"{self.char.name} finds satisfaction in a hearty meal.",
+                f"{self.char.name} loves the joy of eating with friends and family.",
+                f"{self.char.name} enjoys the indulgence of a snack in the middle of the night.",
+                f"{self.char.name} finds pleasure in the simple act of eating.",
+                f"{self.char.name} loves the sensation of her stomach stretching as she eats.",
+                f"{self.char.name} enjoys the feeling of fullness after a big meal."
+            ],
+            "eroticism": [
+                f"{self.char.name} loves the sensuality of her body.",
+                f"{self.char.name} finds pleasure in her own touch.",
+                f"{self.char.name} enjoys the erotic nature of her curves.",
+                f"{self.char.name} loves to explore her own body.",
+                f"{self.char.name} finds it thrilling to feel her own skin.",
+                f"{self.char.name} enjoys the sensuality of intimate moments.",
+                f"{self.char.name} loves the way her body feels in the heat of passion.",
+                f"{self.char.name} finds pleasure in the act of seduction.",
+                f"{self.char.name} enjoys the erotic tension between herself and her partner.",
+                f"{self.char.name} loves the feeling of being desired.",
+                f"{self.char.name} finds it exciting to explore her own desires.",
+                f"{self.char.name} enjoys the intimacy of being close to her partner.",
+                f"{self.char.name} loves the way her body responds to touch.",
+                f"{self.char.name} finds satisfaction in the act of lovemaking.",
+                f"{self.char.name} enjoys the pleasure of her partner's touch.",
+                f"{self.char.name} loves the sensuality of her own body.",
+                f"{self.char.name} finds it thrilling to be desired.",
+                f"{self.char.name} enjoys the eroticism of intimate moments.",
+                f"{self.char.name} loves the feeling of being close to her partner.",
+                f"{self.char.name} finds pleasure in the act of seduction."
+            ],
+            "partying": [
+                f"{self.char.name} loves to party and have a good time.",
+                f"{self.char.name} enjoys the excitement of a night out.",
+                f"{self.char.name} finds pleasure in dancing the night away.",
+                f"{self.char.name} loves the energy of a lively party.",
+                f"{self.char.name} enjoys the social aspect of partying.",
+                f"{self.char.name} finds it thrilling to meet new people.",
+                f"{self.char.name} loves the freedom of letting loose.",
+                f"{self.char.name} enjoys the fun of a good party.",
+                f"{self.char.name} finds pleasure in the music and dancing.",
+                f"{self.char.name} loves the atmosphere of a crowded club.",
+                f"{self.char.name} enjoys the excitement of a spontaneous night out.",
+                f"{self.char.name} finds it exhilarating to be the life of the party.",
+                f"{self.char.name} loves the joy of celebrating with friends.",
+                f"{self.char.name} enjoys the thrill of a big event.",
+                f"{self.char.name} finds pleasure in the chaos of a wild party.",
+                f"{self.char.name} loves the feeling of being carefree.",
+                f"{self.char.name} enjoys the social interactions at parties.",
+                f"{self.char.name} finds it exciting to be surrounded by people.",
+                f"{self.char.name} loves the fun of a themed party",
+                f"{self.char.name} finds it exciting to be surrounded by people.",
+                f"{self.char.name} loves the fun of a themed party.",
+                f"{self.char.name} enjoys the thrill of a surprise party."
+            ],
+            "binging": [
+                f"{self.char.name} loves the thrill of a binge session.",
+                f"{self.char.name} enjoys the sensation of eating non-stop.",
+                f"{self.char.name} finds pleasure in consuming large quantities of food.",
+                f"{self.char.name} loves the indulgence of a binge.",
+                f"{self.char.name} enjoys the feeling of fullness after a binge.",
+                f"{self.char.name} finds it satisfying to eat until she can't eat anymore.",
+                f"{self.char.name} loves the decadence of a food binge.",
+                f"{self.char.name} enjoys the ritual of binging on her favorite foods.",
+                f"{self.char.name} finds comfort in binging on comfort foods.",
+                f"{self.char.name} loves the experience of losing control while binging.",
+                f"{self.char.name} enjoys the pleasure of a secret binge session.",
+                f"{self.char.name} finds it thrilling to binge on forbidden foods.",
+                f"{self.char.name} loves the sensation of her stomach stretching during a binge.",
+                f"{self.char.name} enjoys the sensory overload of a binge.",
+                f"{self.char.name} finds satisfaction in a binge session.",
+                f"{self.char.name} loves the joy of eating without limits.",
+                f"{self.char.name} enjoys the indulgence of a late-night binge.",
+                f"{self.char.name} finds pleasure in the act of binging.",
+                f"{self.char.name} loves the feeling of fullness after a big binge.",
+                f"{self.char.name} enjoys the sensation of her body responding to a binge."
+            ],
+            "romance": [
+                f"{self.char.name} loves the feeling of being in love.",
+                f"{self.char.name} enjoys the intimacy of a romantic relationship.",
+                f"{self.char.name} finds pleasure in the small gestures of love.",
+                f"{self.char.name} loves the excitement of a new romance.",
+                f"{self.char.name} enjoys the comfort of a steady relationship.",
+                f"{self.char.name} finds it thrilling to be swept off her feet.",
+                f"{self.char.name} loves the warmth of a loving embrace.",
+                f"{self.char.name} enjoys the joy of spending time with her partner.",
+                f"{self.char.name} finds satisfaction in the stability of a romantic relationship.",
+                f"{self.char.name} loves the feeling of being cherished.",
+                f"{self.char.name} enjoys the pleasure of a romantic date night.",
+                f"{self.char.name} finds it exciting to be in love.",
+                f"{self.char.name} loves the sensation of her heart racing when she sees her partner.",
+                f"{self.char.name} enjoys the intimacy of shared secrets and inside jokes.",
+                f"{self.char.name} finds pleasure in the act of loving and being loved.",
+                f"{self.char.name} loves the feeling of butterflies in her stomach.",
+                f"{self.char.name} enjoys the thrill of a romantic surprise.",
+                f"{self.char.name} finds satisfaction in the connection with her partner.",
+                f"{self.char.name} loves the joy of being with someone special.",
+                f"{self.char.name} enjoys the warmth of a loving relationship."
+            ],
+            "teasing": [
+                f"{self.char.name} loves to tease with her growing curves.",
+                f"{self.char.name} enjoys the playful nature of teasing.",
+                f"{self.char.name} finds pleasure in teasing her partner.",
+                f"{self.char.name} loves the excitement of playful teasing.",
+                f"{self.char.name} enjoys the thrill of being a tease.",
+                f"{self.char.name} finds it satisfying to see her partner's reaction.",
+                f"{self.char.name} loves the fun of a good tease.",
+                f"{self.char.name} enjoys the playful banter and flirtation.",
+                f"{self.char.name} finds pleasure in the art of teasing.",
+                f"{self.char.name} loves the way her partner responds to her teasing.",
+                f"{self.char.name} enjoys the game of cat and mouse.",
+                f"{self.char.name} finds it thrilling to keep her partner on their toes.",
+                f"{self.char.name} loves the sensation of playful teasing.",
+                f"{self.char.name} enjoys the excitement of a teasing game.",
+                f"{self.char.name} finds satisfaction in the playful interaction.",
+                f"{self.char.name} loves the fun of teasing her partner.",
+                f"{self.char.name} enjoys the playful nature of teasing.",
+                f"{self.char.name} finds pleasure in the reaction she gets from teasing.",
+                f"{self.char.name} loves the thrill of being a tease.",
+                f"{self.char.name} enjoys the playful dance of tease and flirtation."
+            ],
+            "clothing_choices": [
+                f"{self.char.name} loves to wear clothes that show off her curves.",
+                f"{self.char.name} enjoys the feeling of tight clothes against her skin.",
+                f"{self.char.name} finds pleasure in dressing up.",
+                f"{self.char.name} loves the way her body looks in form-fitting clothes.",
+                f"{self.char.name} enjoys the confidence boost from wearing sexy outfits.",
+                f"{self.char.name} finds it exciting to try on new clothes.",
+                f"{self.char.name} loves the way her body fills out her clothes.",
+                f"{self.char.name} enjoys the sensation of fabrics against her skin.",
+                f"{self.char.name} finds satisfaction in a well-put-together outfit.",
+                f"{self.char.name} loves the way her clothes accentuate her body.",
+                f"{self.char.name} enjoys the thrill of shopping for new clothes.",
+                f"{self.char.name} finds pleasure in wearing clothes that make her feel sexy.",
+                f"{self.char.name} finds pleasure in wearing clothes that make her feel sexy.",
+                f"{self.char.name} loves the confidence she feels in stylish outfits.",
+                f"{self.char.name} enjoys the process of picking out the perfect outfit.",
+                f"{self.char.name} finds it thrilling to wear clothes that hug her curves.",
+                f"{self.char.name} loves the way her clothes fit as she gains weight.",
+                f"{self.char.name} enjoys the sensation of slipping into something tight and revealing.",
+                f"{self.char.name} finds satisfaction in wearing clothes that show off her figure.",
+                f"{self.char.name} loves the way her body looks in a new dress.",
+                f"{self.char.name} enjoys the excitement of wearing something new.",
+                f"{self.char.name} finds pleasure in clothes that make her feel desired.",
+                f"{self.char.name} loves the way her clothes feel as they hug her body.",
+                f"{self.char.name} enjoys the confidence that comes from wearing a great outfit.",
+                f"{self.char.name} finds it thrilling to wear something daring.",
+                f"{self.char.name} loves the way her body looks in lingerie.",
+                f"{self.char.name} enjoys the process of getting dressed up.",
+                f"{self.char.name} finds satisfaction in wearing clothes that make her feel beautiful.",
+                f"{self.char.name} loves the way her clothes fit her changing body.",
+                f"{self.char.name} enjoys the sensation of wearing something special.",
+                f"{self.char.name} finds pleasure in the way her clothes accentuate her curves.",
+                f"{self.char.name} loves the excitement of trying on different styles."
+            ]
+        }
+        self.fat_fetishism = self.random_fetish()
+        self.forced_feeding = self.random_feeding()
+        self.weight_gain = self.random_gain()
+        self.sex = self.random_sex()
+        self.eating = self.random_eating()
+        self.eroticism = self.random_eroticism()
+        self.partying = self.random_partying()
+        self.binging = self.random_binging()
+        self.romance = self.random_romance()
+        self.teasing = self.random_teasing()
+        self.clothing = self.random_clothing_choices()
+
+    def random_fetish(self):
+        return random.choice(self.descriptions['fat_fetishism'])
+
+    def random_feeding(self):
+        return random.choice(self.descriptions['forced_feeding'])
+
+    def random_gain(self):
+        return random.choice(self.descriptions['weight_gain'])
+
+    def random_sex(self):
+        return random.choice(self.descriptions['fat_sex'])
+
+    def random_eating(self):
+        return random.choice(self.descriptions['eating'])
+
+    def random_eroticism(self):
+        return random.choice(self.descriptions['eroticism'])
+
+    def random_partying(self):
+        return random.choice(self.descriptions['partying'])
+
+    def random_binging(self):
+        return random.choice(self.descriptions['binging'])
+
+    def random_romance(self):
+        return random.choice(self.descriptions['romance'])
+
+    def random_teasing(self):
+        return random.choice(self.descriptions['teasing'])
+
+    def random_clothing_choices(self):
+        return random.choice(self.descriptions['clothing_choices'])
+
+    def get_fetish(self):
+        return self.fat_fetishism
+
+    def get_forced_feeding(self):
+        return self.forced_feeding
+
+    def get_weight_gain(self):
+        return self.weight_gain
+
+    def get_sex(self):
+        return self.sex
+
+    def get_eating(self):
+        return self.eating
+
+    def get_eroticism(self):
+        return self.eroticism
+
+    def get_partying(self):
+        return self.partying
+
+    def get_binging(self):
+        return self.binging
+
+    def get_romance(self):
+        return self.romance
+
+    def get_teasing(self):
+        return self.teasing
+
+    def get_clothing(self):
+        return self.clothing
+
+    def formatted_fetish(self):
+        return ' + '.join([f'"{desc}"' for desc in self.descriptions['fat_fetishism']])
+
+    def formatted_feeding(self):
+        return ' + '.join([f'"{desc}"' for desc in self.descriptions['forced_feeding']])
+
+    def formatted_weight_gain(self):
+        return ' + '.join([f'"{desc}"' for desc in self.descriptions['weight_gain']])
+
+    def formatted_sex(self):
+        return ' + '.join([f'"{desc}"' for desc in self.descriptions['fat_sex']])
+
+    def formatted_eating(self):
+        return ' + '.join([f'"{desc}"' for desc in self.descriptions['eating']])
+
+    def formatted_eroticism(self):
+        return ' + '.join([f'"{desc}"' for desc in self.descriptions['eroticism']])
+
+    def formatted_partying(self):
+        return ' + '.join([f'"{desc}"' for desc in self.descriptions['partying']])
+
+    def formatted_binging(self):
+        return ' + '.join([f'"{desc}"' for desc in self.descriptions['binging']])
+
+    def formatted_romance(self):
+        return ' + '.join([f'"{desc}"' for desc in self.descriptions['romance']])
+
+    def formatted_teasing(self):
+        return ' + '.join([f'"{desc}"' for desc in self.descriptions['teasing']])
+
+    def formatted_clothing_choices(self):
+        return ' + '.join([f'"{desc}"' for desc in self.descriptions['clothing_choices']])
+
+    def formatted_all(self):
+        components = [
+            self.get_fetish(),
+            self.get_eating(),
+            self.get_weight_gain(),
+            self.get_sex(),
+            self.get_eating(),
+            self.get_eroticism(),
+            self.get_partying(),
+            self.get_binging(),
+            self.get_romance(),
+            self.get_teasing(),
+            self.get_clothing()
+        ]
+        formatted_components = [f'"{component}"' for component in components]
+        return ' + '.join(formatted_components)
+
+
+class Character:
+    BMI_CATEGORY = ["Underweight", "Healthy", "Overweight", "Chubby", "Obese", "Super Obese", "Hyper Obese"]
+    FULLNESS = ["Starving", "Hungry", "Content", "Satiated", "Stuffed", "Overfed"]
+    EYE_COLORS = [
+        "Amber", "Blue", "Brown", "Gray", "Green", "Hazel", "Turquoise", "Emerald", "Sapphire", "Chocolate"
+    ]
+
+    FACIAL_FEATURES = [
+        {
+            "type": "Nose",
+            "features": ["Upturned Nose", "Straight Nose", "Pointed Nose", "Broad Nose"]
+        },
+        {
+            "type": "Eyes",
+            "features": ["Almond-Shaped Eyes", "Large Eyes", "Long Eyelashes", "Arched Eyebrows",
+                         "Feline Eyes", "Doe Eyes", "Bedroom Eyes", "Sparkling Eyes", "Expressive Eyes"]
+        },
+        {
+            "type": "Lips",
+            "features": ["Pouty Lips", "Full Lips", "Cupid's Bow Lips", "Pillowy Lips"]
+        },
+        {
+            "type": "Cheeks",
+            "features": ["Dimples", "High Cheekbones", "Freckles", "Beauty Mark", "Rosy Cheeks",
+                         "Sculpted Cheekbones", "Plump Cheeks"]
+        },
+        {
+            "type": "Face",
+            "features": ["Symmetrical Face", "Delicate Features", "Angelic Features", "Striking Features",
+                         "Alluring Features", "Exotic Features"]
+        },
+        {
+            "type": "Smile",
+            "features": ["Radiant Smile", "Bright Smile", "Enchanting Smile", "Captivating Smile"]
+        }
+    ]
+
+    HAIR_COLORS = [
+        "Blonde", "Brown", "Black", "Red", "Auburn", "Strawberry Blonde", "Ginger",
+        "Chestnut", "Burgundy", "Violet", "Pink", "Blue", "Green", "Platinum", "Lavender", "Turquoise"
+    ]
+
+    SKIN_TONES = [
+        "Fair", "Porcelain", "Ivory", "Peach", "Olive", "Tan", "Honey", "Beige",
+        "Golden", "Bronze", "Chestnut", "Mahogany", "Ebony", "Espresso", "Chocolate"
+    ]
+
+    # Extended dataset to cover sizes from X-Small to 15XL
+    data = {
+        'Size': ["X-Small", "Small", "Medium", "Large", "X-Large", "2XL", "3XL", "4XL", "5XL", "6XL", "7XL", "8XL",
+                 "9XL", "10XL", "11XL", "12XL", "13XL", "14XL", "15XL"],
+        'Chest': [29, 33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105],
+        'Waist': [23.5, 25.75, 29, 33, 37, 41, 44.5, 46.5, 49.5, 52.5, 55.5, 58.5, 61.5, 64.5, 67.5, 70.5, 73.5, 76.5,
+                  79.5, 82.5],
+        'Hips': [33.5, 35.5, 39, 43, 47, 52.5, 54.5, 56.5, 58.5, 60.5, 62.5, 64.5, 66.5, 68.5, 70.5, 72.5, 74.5, 76.5,
+                 78.5, 80.5]
+    }
+
+    def __init__(self, name, age, weight, height):
+        self.name = name
+        self.age = age
+        self.weight = weight
+        self.height = height
+        self.calories = 0
+        self.max_calories = self.calculate_bmr()
+        self.weight_diff = 0
+        self.bmi = self.calculate_bmi()
+        dimensions = self.predict_body_dimensions()
+        self.chest = dimensions['Chest']
+        self.waist = dimensions['Waist']
+        self.hips = dimensions['Hips']
+        self.clothing = self.get_clothing_size()
+        self.eye_color = self.random_eye_color()
+        self.nose = self.random_nose()
+        self.eye_shape = self.random_eye_shape()
+        self.lips = self.random_lips()
+        self.cheeks = self.random_cheeks()
+        self.face = self.random_face()
+        self.smile = self.random_smile()
+        self.hair = self.random_hair_color()
+        self.skin = self.random_skin_color()
+        self.username = ""
+
+    def get_name(self):
+        return self.name
+
+    def get_age(self):
+        return self.age
+
+    def get_weight(self):
+        return self.weight
+
+    def get_height(self):
+        return self.height
+
+    def get_calories(self):
+        return self.calories
+
+    def get_weight_diff(self):
+        return self.weight_diff
+
+    def get_chest(self):
+        return self.chest
+
+    def get_waist(self):
+        return self.waist
+
+    def get_hips(self):
+        return self.hips
+
+    def get_username(self):
+        return self.username
+
+    def random_nose(self):
+        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Nose" for feature in d["features"]])
+
+    def random_eye_shape(self):
+        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Eyes" for feature in d["features"]])
+
+    def random_lips(self):
+        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Lips" for feature in d["features"]])
+
+    def random_cheeks(self):
+        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Cheeks" for feature in d["features"]])
+
+    def random_face(self):
+        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Face" for feature in d["features"]])
+
+    def random_smile(self):
+        return random.choice([feature for d in Character.FACIAL_FEATURES if d["type"] == "Smile" for feature in d["features"]])
+
+    def random_eye_color(self):
+        return random.choice(Character.EYE_COLORS)
+
+    def random_hair_color(self):
+        return random.choice(Character.HAIR_COLORS)
+
+    def random_skin_color(self):
+        return random.choice(Character.SKIN_TONES)
+
+    def set_name(self, name):
+        self.name = name
+
+    def set_age(self, age):
+        self.age = age
+
+    def set_weight(self, weight):
+        self.weight = weight
+
+    def set_height(self, height):
+        self.height = height
+
+    def add_calories(self, calories):
+        self.calories += calories
+
+    def set_eye_color(self, eye_color):
+        self.eye_color = eye_color
+
+    def set_nose(self, nose):
+        self.nose = nose
+        
+    def set_eyes(self, eyes):
+        self.eye_shape = eyes
+
+    def set_lips(self, lips):
+        self.lips = lips
+
+    def set_cheeks(self, cheeks):
+        self.cheeks = cheeks
+
+    def set_face(self, face):
+        self.face = face
+
+    def set_smile(self, smile):
+        self.smile = smile
+
+    def set_hair(self, hair):
+        self.hair = hair
+
+    def set_skin(self, skin):
+        self.skin = skin
+
+    def set_username(self, name):
+        self.username = name
+
+    def calculate_bmi(self):
+        try:
+            weight = float(self.weight)
+            height = float(self.height)
+            bmi_value = (weight / (height ** 2)) * 703
+            return round(bmi_value, 1)
+        except (ValueError, TypeError):
+            print("Invalid weight or height value.")
+            return None
+
+    def calculate_bmi_class(self):
+        bmi_value = self.calculate_bmi()
+        thresholds = [15, 20, 25, 30, 35, 40, 50]
+        for i, threshold in enumerate(thresholds):
+            if bmi_value < threshold:
+                return f"{Character.BMI_CATEGORY[i - 1]}"
+        return f"{Character.BMI_CATEGORY[-1]}"
+
+    def calculate_bmr(self):
+        return 655 + (4.35 * self.weight) + (4.7 * self.height) - (4.7 * self.age)
+
+    def calculate_fullness(self):
+        fullness_percentage = (self.calories / self.max_calories) * 100
+        thresholds = [20, 40, 60, 80, 100]
+        for i, threshold in enumerate(thresholds):
+            if fullness_percentage < threshold:
+                return f"{Character.FULLNESS[i - 1]}"
+        return f"{Character.FULLNESS[-1]}"
+
+    def calculate_height_cm(self):
+        return self.height * 2.54
+
+    def calculate_height_feet(self):
+        feet = self.height / 12
+        inches = self.height % 12
+        return feet, inches
+
+    def predict_body_dimensions(self):
+        bmi = self.calculate_bmi()
+
+        # Define base dimensions for a woman with BMI 25 (overweight)
+        base_bust = 40
+        base_waist = 32
+        base_hips = 42
+
+        # Define the growth rate per 5 BMI points
+        growth_rate = 4
+
+        # Calculate the number of 5 BMI point intervals from the base BMI
+        bmi_intervals = (bmi - 25) // 5
+
+        # Calculate the estimated dimensions based on linear growth
+        estimated_bust = base_bust + (bmi_intervals * growth_rate)
+        estimated_waist = base_waist + (bmi_intervals * growth_rate)
+        estimated_hips = base_hips + (bmi_intervals * growth_rate)
+
+        # Generate random offsets for each dimension within the specified tolerance
+        bust_offset = random.uniform(-1.5, 1.5)
+        waist_offset = random.uniform(-1.5, 1.5)
+        hips_offset = random.uniform(-1.5, 1.5)
+
+        # Apply the random offsets to the estimated dimensions
+        final_bust = estimated_bust + bust_offset
+        final_waist = estimated_waist + waist_offset
+        final_hips = estimated_hips + hips_offset
+
+        # Round the final dimensions to the nearest inch
+        final_bust = round(final_bust)
+        final_waist = round(final_waist)
+        final_hips = round(final_hips)
+
+        # Ensure the dimensions are within realistic ranges
+        final_bust = max(30, min(final_bust, 60))
+        final_waist = max(24, min(final_waist, 50))
+        final_hips = max(32, min(final_hips, 65))
+
+        # Determine the clothing size based on the estimated dimensions
+        sizes = ["X-Small", "Small", "Medium", "Large", "X-Large", "2XL", "3XL", "4XL", "5XL"]
+        size_thresholds = [0, 35, 37, 39, 41, 43, 45, 47, 49]
+
+        clothing_size = sizes[-1]
+        for i in range(len(size_thresholds) - 1):
+            if final_bust < size_thresholds[i + 1]:
+                clothing_size = sizes[i]
+                break
+
+        # Return the predicted body dimensions and clothing size
+        return {
+            'Chest': final_bust,
+            'Waist': final_waist,
+            'Hips': final_hips,
+            'Clothing Size': clothing_size
+        }
+
+
+    def get_clothing_size(self):
+        # Calculate the absolute differences between character's dimensions and dataset dimensions
+        min_diff = float('inf')
+        closest_index = 0
+        
+        for i in range(len(self.data['Size'])):
+            chest_diff = abs(self.data['Chest'][i] - self.chest)
+            waist_diff = abs(self.data['Waist'][i] - self.waist)
+            hips_diff = abs(self.data['Hips'][i] - self.hips)
+            
+            total_diff = chest_diff + waist_diff + hips_diff
+            
+            if total_diff < min_diff:
+                min_diff = total_diff
+                closest_index = i
+
+        # Return the corresponding clothing size
+        return self.data['Size'][closest_index]
+
+class Time:
+
+    def __init__(self, character, birth_day, birth_month, current_year, current_month, current_day):
+        self.current_year = current_year
+        self.current_month = current_month
+        self.current_day = current_day
+        self.current_date = datetime.datetime(current_year, current_month, current_day)
+        self.day = 0
+        self.character = character
+        self.birth_day = birth_day
+        self.birth_month = birth_month
+        self.birth_year = self.get_birth_year()
+        self.birth_date = datetime.datetime(self.get_birth_year(), birth_month, birth_day)
+        self.mind = Mind()
+
+    def get_current_date(self):
+        return self.current_date
+
+    def get_birth_date(self):
+        return self.birth_date
+
+    def get_day(self):
+        return self.day
+
+    def get_formatted_current_date(self):
+        return self.current_date.strftime("%B %d, %Y")
+
+    def get_formatted_birth_date(self):
+        return self.birth_date.strftime("%B %d, %Y")
+
+    def set_current_date(self, new_year, new_month, new_day):
+        self.current_date = datetime.datetime(new_year, new_month, new_day)
+
+    def get_birth_year(self):
+        return self.current_date.year - self.character.age
+
+    def set_birth_date(self, new_month, new_day):
+        try:
+            # Validate the inputs
+            if not (1 <= new_month <= 12):
+                raise ValueError(f"Invalid month: {new_month}")
+            if not (1 <= new_day <= 31):  # Basic validation, more checks needed for specific months
+                raise ValueError(f"Invalid day: {new_day}")
+
+            # Create the new birth_date
+            self.birth_date = datetime.datetime(self.get_birth_year(), new_month, new_day)
+            print(f"Birth date set to: {self.birth_date}")  # Debugging statement
+        except Exception as e:
+            print(f"Error setting birth date: {e}")
+
+    def set_day(self, num):
+        self.day += num
+
+    def end_day(self):
+        self.current_date += datetime.timedelta(days=1)
+        self.day += 1
+        excess_calories = self.character.get_calories() - self.character.calculate_bmr()
+        if excess_calories > 500:
+            self.character.weight += int(excess_calories / 500)
+            self.character.weight_diff += int(excess_calories / 500) # Add 1 lb for every excess of 500 calories
+        if self.current_month == self.birth_month and self.current_day == self.birth_day:
+            self.character.age += 1
+        self.character.calories = 0
+        dimensions = self.character.predict_body_dimensions()
+        self.character.chest = dimensions['Chest']
+        self.character.waist = dimensions['Waist']
+        self.character.hips = dimensions['Hips']
+        self.character.clothing = self.character.get_clothing_size()
+        self.character.max_calories = self.character.calculate_bmr()
+        self.mind.change_mood()
+
+
+class Mind:
+
+    def __init__(self):
+        self.moods = [
+            "Happy", "Sad", "Angry", "Excited", "Anxious", "Calm", "Confused",
+            "Bored", "Nervous", "Relaxed", "Content", "Frustrated", "Euphoric",
+            "Melancholic", "Indifferent", "Optimistic", "Pessimistic", "Hopeful",
+            "Disappointed", "Energetic", "Tired", "Irritated", "Grateful",
+            "Lonely", "Motivated", "Overwhelmed", "Peaceful", "Restless",
+            "Satisfied", "Surprised", "Worried", "Jealous", "Curious", "Determined",
+            "Fearful", "Guilty", "Insecure", "Joyful", "Lazy", "Mischievous",
+            "Proud", "Regretful", "Resentful", "Scared", "Shy", "Skeptical",
+            "Sympathetic", "Thankful", "Uncomfortable", "Vulnerable", "Weary",
+            "Zealous", "Horny", "Ravenous"
+        ]
+        self.positive_mind_traits = [
+            "Creative", "Curious", "Determined", "Empathetic", "Enthusiastic", "Grateful",
+            "Insightful", "Optimistic", "Patient", "Resilient", "Adaptable", "Adventurous",
+            "Charming", "Compassionate", "Confident", "Considerate", "Courageous", "Decisive",
+            "Diligent", "Encouraging", "Faithful", "Forgiving", "Generous", "Genuine",
+            "Humble", "Imaginative", "Independent", "Kind", "Loyal", "Motivated",
+            "Observant", "Open-Minded", "Passionate", "Reliable", "Sincere", "Supportive"
+        ]
+        self.negative_mind_traits = [
+            "Anxious", "Cynical", "Impulsive", "Insecure", "Irritable", "Jealous",
+            "Moody", "Pessimistic", "Selfish", "Stubborn", "Apathetic", "Arrogant",
+            "Bossy", "Cold", "Critical", "Deceitful", "Disorganized", "Distrustful",
+            "Egocentric", "Envious", "Gossipy", "Greedy", "Grumpy", "Harsh",
+            "Impatient", "Judgmental", "Lazy", "Manipulative", "Narrow-Minded",
+            "Narcissistic", "Obsessive", "Paranoid", "Rebellious", "Rude", "Sarcastic",
+            "Self-Centered", "Suspicious", "Unreliable", "Vindictive", "Playful", "Impulsive"
+        ]
+        self.traits = [
+            "Adventurous", "Ambitious", "Caring", "Confident", "Dependable", "Friendly",
+            "Generous", "Hardworking", "Honest", "Loyal", "Modest", "Polite",
+            "Responsible", "Sociable", "Thoughtful", "Understanding", "Warm", "Witty",
+            "Affectionate", "Amiable", "Brave", "Calm", "Charismatic", "Cheerful",
+            "Clever", "Conscientious", "Considerate", "Cooperative", "Courteous",
+            "Disciplined", "Empathetic", "Encouraging", "Fair", "Forgiving",
+            "Frank", "Fun-Loving", "Generous", "Gentle", "Genuine", "Gracious",
+            "Helpful", "Honorable", "Humble", "Humorous", "Imaginative", "Intelligent",
+            "Kind", "Knowledgeable", "Lively", "Mature", "Neat", "Optimistic",
+            "Organized", "Patient", "Perceptive", "Persistent", "Practical",
+            "Respectful", "Self-Confident", "Sensible", "Sensitive", "Sincere",
+            "Tactful", "Trustworthy", "Understanding", "Vigilant", "Wise"
+        ]
+        self.loves = [
+            "Feeding", "Being fed", "Big meals", "Weight gain", "Romantic dinners",
+            "Lazy days", "Party nights", "Late-night snacks", "Comfort food", "Intimacy",
+            "Sweet treats", "Cuddling", "Fast food", "Takeout", "Movie marathons",
+            "Indulgence", "Breakfast in bed", "Pillow talk", "Morning cuddles",
+            "Pizza nights", "Desserts", "Cheese platters", "Fucking", "Binge eating",
+            "Wine and dine", "Cooking together", "Binge-watching", "Food delivery",
+            "Brunch dates", "Bubble baths", "Pancake breakfasts", "Ice cream",
+            "Chocolate", "Fried food", "Bar nights", "Dancing", "Cozy nights in",
+            "Sleepovers", "Bakery visits", "Shared meals", "Lazy Sundays",
+            "Breakfast buffets", "Surprise treats", "Gourmet food", "Sweet kisses",
+            "Home-cooked meals", "Food festivals", "Date nights", "Picnics",
+            "Midnight feasts", "Warm hugs", "Junk food", "Guilty pleasures",
+            "Sensual touch", "Passionate kisses", "Intimate moments", "Erotic whispers",
+            "Slow dancing", "Romantic gestures", "Candlelit dinners", "Bubble baths",
+            "Massage", "Role-playing", "Dirty talk", "Lingerie", "Flirting", "Foreplay",
+            "Spontaneous sex", "Public displays", "Body worship", "Holding hands",
+            "Eye contact", "Playful teasing", "Soft music", "Bedtime stories", "Erotic novels",
+            "Sexy photos", "Morning sex", "Shower sex", "Handcuffs", "Blindfolds",
+            "Feather tickling", "Silk sheets", "Warm embraces", "Tantric sex",
+            "Erotic games", "Adventurous locations", "Love letters", "Cuddling",
+            "Pillow talk", "Scented candles", "Intimate conversations", "Long kisses",
+            "Body oil", "Sexy surprises", "Whispers in the ear", "Erotic massages",
+            "Private jokes", "Sensual dancing", "Body painting", "Touching under the table",
+            "Skin contact", "Shared fantasies"
+        ]
+        self.hates = [
+            "Dieting", "Calorie counting", "Exercise", "Healthy food", "Early mornings",
+            "Being judged", "Small portions", "Skipping meals", "Feeling guilty",
+            "Food waste", "Hangovers", "Long work hours", "Stressful jobs",
+            "Strict schedules", "Uncomfortable clothes", "Bland meals", "Crowded gyms",
+            "Body shaming", "Fast-paced life", "Routine", "Plain salads",
+            "Cold weather", "Loneliness", "Strict diets", "Being rushed",
+            "Meal prepping", "Work deadlines", "Cooking alone", "Noise",
+            "Boring people", "Bad food", "Overtime", "Being ignored",
+            "Unappetizing food", "Waking up early", "Unkind people", "Rude comments",
+            "Arguments", "Discomfort", "Rigid plans", "Crowds", "Unpleasant smells",
+            "Insecurity", "Judgmental attitudes", "Lack of communication", "Coldness",
+            "Disrespect", "Neglect", "Rejection", "Boredom", "Routine", "Lack of effort",
+            "Criticism", "Dishonesty", "Cheating", "Disinterest", "Jealousy",
+            "Overthinking", "Misunderstandings", "Awkward silence", "Lack of intimacy",
+            "Unresolved conflicts", "Selfishness", "Insensitivity", "Lack of trust",
+            "Emotional distance", "Negativity", "Impatience", "Aggressiveness",
+            "Disorganization", "Unreliability", "Disharmony", "Stress", "Pressure",
+            "Unkind remarks", "Unfulfilled promises", "Unappreciated", "Apathy",
+            "Lack of passion", "Monotony", "Clinginess", "Over-possessiveness",
+            "Unwillingness to compromise", "Criticizing appearance", "Ignoring boundaries",
+            "Taking things for granted"
+        ]
+        self.mind_traits = self.random_mind_traits()
+        self.personality_traits = self.random_personality_traits()
+        self.current_mood = random.choice(self.moods)
+        self.loves = self.random_loves()
+        self.hates = self.random_hates()
+
+    def random_mind_traits(self):
+        positive_sample_size = min(6, len(self.positive_mind_traits))
+        negative_sample_size = min(6, len(self.negative_mind_traits))
+        combined_traits = random.sample(self.positive_mind_traits, positive_sample_size) + random.sample(
+            self.negative_mind_traits, negative_sample_size)
+        return combined_traits
+
+    def random_personality_traits(self):
+        return random.sample(self.traits, 5)
+
+    def random_loves(self):
+        return random.sample(self.loves, 5)
+
+    def random_hates(self):
+        return random.sample(self.hates, 5)
+
+    def change_mood(self):
+        self.current_mood = random.choice(self.moods)
+
+    def get_mood(self):
+        return self.current_mood
+
+    def __str__(self):
+        return f"Mind Traits: {self.formatted_mind_traits()}, Personality Traits: {self.formatted_personality_traits()}, Current Mood: {self.current_mood}"
+
+    def formatted_mind_traits(self):
+        formatted_traits = [f'"{trait}"' for trait in self.mind_traits]
+        return " + ".join(formatted_traits)
+
+    def formatted_personality_traits(self):
+        formatted_traits = [f'"{trait}"' for trait in self.personality_traits]
+        return " + ".join(formatted_traits)
+
+    def formatted_loves(self):
+        formatted_traits = [f'"{trait}"' for trait in self.loves]
+        return " + ".join(formatted_traits)
+
+    def formatted_hates(self):
+        formatted_traits = [f'"{trait}"' for trait in self.hates]
+        return " + ".join(formatted_traits)
+
+
+class Relationship:
+    RELATIONSHIP_STATUS = [
+        "Hatred", "Loathing", "Disgust", "Resentment", "Animosity", "Hostility",
+        "Dislike", "Irritation", "Annoyance", "Indifference", "Neutral",
+        "Curiosity", "Interest", "Affection", "Fondness", "Respect",
+        "Friendship", "Attachment", "Love", "Adoration", "Devotion"
+    ]
+
+    def __init__(self):
+        self.relationship_status = Relationship.RELATIONSHIP_STATUS[9]
+        self.relationship_score = 0.0
+
+    def get_relationship_status(self):
+        return self.relationship_status
+
+    def get_relationship_score(self):
+        return self.relationship_score
+
+    def set_relationship_status(self, relationship_status):
+        self.relationship_status = relationship_status
+
+    def adjust_relationship_score(self, relationship_adjustment):
+        self.relationship_score += relationship_adjustment
+        self.relationship_score = max(-10.0, min(10.0, self.relationship_score))  # Ensure score remains within bounds
+        self.update_relationship_status()
+
+    def update_relationship_status(self):
+        thresholds = [-10.0, -9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
+        for i, threshold in enumerate(thresholds):
+            if self.relationship_score < threshold:
+                self.relationship_status = Relationship.RELATIONSHIP_STATUS[i]
+                return
+        self.relationship_status = Relationship.RELATIONSHIP_STATUS[-1]
+
+    def calculate_relationship(self):
+        self.update_relationship_status()
+        return self.relationship_status
+
+    def calculate_sentiment_score(self, string):
+        emotion_scores = simple_emotion_classifier(string)
+
+        # Find the emotion with the highest score
+        max_emotion = max(emotion_scores, key=emotion_scores.get)
+
+        # Adjust the relationship score based on the max emotion
+        if max_emotion == "love":
+            self.adjust_relationship_score(0.1)
+        elif max_emotion == "joy":
+            self.adjust_relationship_score(0.067)
+        elif max_emotion == "surprise":
+            self.adjust_relationship_score(0.033)
+        elif max_emotion == "sadness":
+            self.adjust_relationship_score(-0.033)
+        elif max_emotion == "fear":
+            self.adjust_relationship_score(-0.067)
+        elif max_emotion == "anger":
+            self.adjust_relationship_score(-0.1)
+
