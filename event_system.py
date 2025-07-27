(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF'
diff --git a/event_system.py b/event_system.py
--- a/event_system.py
+++ b/event_system.py
@@ -0,0 +1,752 @@
+#!/usr/bin/env python3
+"""
+Dynamic Event System for Dating Simulator
+Generates structured random events to drive engaging interactions
+"""
+
+import random
+import time
+import json
+from typing import Dict, List, Any, Optional, Tuple
+from dataclasses import dataclass, asdict
+from enum import Enum
+
+class EventType(Enum):
+    """Types of events that can occur"""
+    SOCIAL = "social"
+    FOOD = "food"
+    EMOTIONAL = "emotional"
+    ACTIVITY = "activity"
+    SURPRISE = "surprise"
+    MOOD = "mood"
+    PHYSICAL = "physical"
+    GAMING = "gaming"
+    WEATHER = "weather"
+    RELATIONSHIP = "relationship"
+
+class EventTrigger(Enum):
+    """What triggers an event"""
+    TIME_BASED = "time_based"
+    CONVERSATION_LULL = "conversation_lull"
+    MOOD_CHANGE = "mood_change"
+    RELATIONSHIP_MILESTONE = "relationship_milestone"
+    RANDOM = "random"
+    USER_ACTION = "user_action"
+
+@dataclass
+class GameEvent:
+    """A single game event with all its properties"""
+    id: str
+    name: str
+    description: str
+    event_type: EventType
+    trigger: EventTrigger
+    probability: float  # 0.0 - 1.0
+    conditions: Dict[str, Any]  # Requirements for event to trigger
+    effects: Dict[str, Any]  # Effects on game state
+    prompts: List[str]  # Prompts for character to respond to
+    user_suggestions: List[str]  # Suggested user responses
+    duration: int  # How many turns the event lasts
+    cooldown: int  # Turns before event can happen again
+    last_triggered: float = 0.0
+    times_triggered: int = 0
+    
+class EventManager:
+    """Manages dynamic events and scene generation"""
+    
+    def __init__(self, character, time_system, relationship, mind):
+        self.character = character
+        self.time_system = time_system
+        self.relationship = relationship
+        self.mind = mind
+        
+        # Event tracking
+        self.active_events: List[GameEvent] = []
+        self.event_history: List[Dict] = []
+        self.conversation_silence_count = 0
+        self.last_event_time = time.time()
+        
+        # Initialize event database
+        self.events = self._initialize_events()
+        
+        # Scene context tracking
+        self.current_scene_context = "casual_hangout"
+        self.scene_momentum = 0.5  # 0.0 = calm, 1.0 = high energy
+        
+    def _initialize_events(self) -> List[GameEvent]:
+        """Initialize the database of possible events"""
+        events = []
+        
+        # Food-related events
+        events.extend([
+            GameEvent(
+                id="cooking_together",
+                name="Cooking Together",
+                description="Maddy suggests cooking a meal together",
+                event_type=EventType.FOOD,
+                trigger=EventTrigger.RANDOM,
+                probability=0.3,
+                conditions={"relationship_score": 2.0, "time_of_day": ["afternoon", "evening"]},
+                effects={"mood_boost": 0.2, "intimacy_increase": 0.3},
+                prompts=[
+                    "Hey, I'm getting kind of hungry... want to cook something together?",
+                    "I found this new recipe online! Should we try making it?",
+                    "You know what sounds fun? Cooking a big meal together and just... enjoying each other's company."
+                ],
+                user_suggestions=[
+                    "That sounds great! What should we make?",
+                    "I'd love to cook with you. What's your favorite dish?",
+                    "Sure! I'll help with whatever you need."
+                ],
+                duration=3,
+                cooldown=10
+            ),
+            
+            GameEvent(
+                id="midnight_snack",
+                name="Late Night Cravings",
+                description="Maddy gets hungry late at night",
+                event_type=EventType.FOOD,
+                trigger=EventTrigger.TIME_BASED,
+                probability=0.4,
+                conditions={"time_of_day": ["late_night"], "calories_today": 2000},
+                effects={"mood_change": "hungry", "intimacy_opportunity": True},
+                prompts=[
+                    "*stomach growls softly* Um... I know it's late, but I'm getting really hungry...",
+                    "I can't sleep... and I keep thinking about food. Is that weird?",
+                    "*looks sheepish* I might have worked up an appetite... want to raid the kitchen with me?"
+                ],
+                user_suggestions=[
+                    "Let's get you something to eat!",
+                    "What are you craving? I'll get it for you.",
+                    "Want me to make you something special?"
+                ],
+                duration=2,
+                cooldown=8
+            ),
+            
+            GameEvent(
+                id="food_delivery_surprise",
+                name="Unexpected Delivery",
+                description="Food delivery arrives unexpectedly",
+                event_type=EventType.SURPRISE,
+                trigger=EventTrigger.RANDOM,
+                probability=0.2,
+                conditions={},
+                effects={"surprise_factor": 0.8, "mood_boost": 0.3},
+                prompts=[
+                    "*doorbell rings* Oh! I completely forgot I ordered food earlier... want to share?",
+                    "Surprise! I may have ordered way too much food. Good thing you're here to help me with it!",
+                    "*delivery person knocks* Perfect timing! I got us some of that place you mentioned."
+                ],
+                user_suggestions=[
+                    "That's perfect! I'm hungry too.",
+                    "You're amazing! What did you get?",
+                    "Great timing! Let's dig in together."
+                ],
+                duration=2,
+                cooldown=15
+            )
+        ])
+        
+        # Gaming events
+        events.extend([
+            GameEvent(
+                id="gaming_session",
+                name="Gaming Together",
+                description="Maddy wants to share her favorite game",
+                event_type=EventType.GAMING,
+                trigger=EventTrigger.CONVERSATION_LULL,
+                probability=0.4,
+                conditions={"relationship_score": 1.0},
+                effects={"bonding_opportunity": True, "mood": "excited"},
+                prompts=[
+                    "Want to see this game I've been obsessed with? I think you'd really like it!",
+                    "*eyes light up* Oh! I just remembered this co-op game we could play together!",
+                    "I know this might sound nerdy, but... want to game with me for a bit?"
+                ],
+                user_suggestions=[
+                    "I'd love to try it with you!",
+                    "Show me what you're passionate about!",
+                    "Let's play! I want to see what you enjoy."
+                ],
+                duration=4,
+                cooldown=12
+            ),
+            
+            GameEvent(
+                id="gaming_achievement",
+                name="Gaming Victory",
+                description="Maddy achieves something significant in a game",
+                event_type=EventType.EMOTIONAL,
+                trigger=EventTrigger.RANDOM,
+                probability=0.25,
+                conditions={},
+                effects={"confidence_boost": 0.4, "mood": "proud"},
+                prompts=[
+                    "*jumps up excitedly* YES! I finally beat that boss I've been stuck on for weeks!",
+                    "Oh my god, did you see that?! I can't believe I just pulled that off!",
+                    "*grins widely* I just hit a new high score! Sorry, I know I'm being a total nerd right now..."
+                ],
+                user_suggestions=[
+                    "That was amazing! You're so skilled!",
+                    "I love seeing you this excited!",
+                    "You should be proud! That looked really hard."
+                ],
+                duration=2,
+                cooldown=20
+            )
+        ])
+        
+        # Social/Emotional events
+        events.extend([
+            GameEvent(
+                id="vulnerable_moment",
+                name="Opening Up",
+                description="Maddy shares something personal",
+                event_type=EventType.EMOTIONAL,
+                trigger=EventTrigger.RELATIONSHIP_MILESTONE,
+                probability=0.3,
+                conditions={"relationship_score": 3.0, "mood": ["calm", "content", "melancholic"]},
+                effects={"intimacy_major_increase": 0.5, "trust_building": True},
+                prompts=[
+                    "*looks thoughtful* You know... I don't usually talk about this, but I feel like I can trust you...",
+                    "*fidgets with hands* There's something I've been wanting to tell someone... and I think that someone is you.",
+                    "*voice gets softer* I've been thinking a lot lately about... well, about us, and about how I feel when I'm with you."
+                ],
+                user_suggestions=[
+                    "I'm here to listen. Take your time.",
+                    "You can tell me anything. I care about you.",
+                    "I'm honored that you trust me with this."
+                ],
+                duration=3,
+                cooldown=25
+            ),
+            
+            GameEvent(
+                id="insecurity_moment",
+                name="Self-Doubt",
+                description="Maddy has a moment of insecurity",
+                event_type=EventType.EMOTIONAL,
+                trigger=EventTrigger.MOOD_CHANGE,
+                probability=0.35,
+                conditions={"mood": ["anxious", "sad", "melancholic"]},
+                effects={"support_opportunity": True, "vulnerability": 0.6},
+                prompts=[
+                    "*looks down* Sometimes I wonder if... if I'm really worth spending time with, you know?",
+                    "*hugs herself* Do you ever think about how different I am from other girls? Not in a good way...",
+                    "*voice wavers slightly* I keep thinking you might get bored of me eventually..."
+                ],
+                user_suggestions=[
+                    "You're absolutely worth it. Don't doubt that.",
+                    "I love how unique and special you are.",
+                    "I'm not going anywhere. You mean a lot to me."
+                ],
+                duration=2,
+                cooldown=15
+            ),
+            
+            GameEvent(
+                id="confidence_boost",
+                name="Feeling Good",
+                description="Maddy has a moment of confidence",
+                event_type=EventType.EMOTIONAL,
+                trigger=EventTrigger.RANDOM,
+                probability=0.3,
+                conditions={"relationship_score": 2.5, "recent_positive_interaction": True},
+                effects={"mood": "confident", "flirtiness_increase": 0.4},
+                prompts=[
+                    "*stretches confidently* You know what? I'm feeling really good about myself today!",
+                    "*smiles warmly* Being around you makes me feel like... like the best version of myself.",
+                    "*laughs softly* I used to be so shy, but with you I feel like I can be anyone I want to be."
+                ],
+                user_suggestions=[
+                    "You should feel confident! You're amazing!",
+                    "I love seeing this side of you!",
+                    "Your confidence is really attractive."
+                ],
+                duration=2,
+                cooldown=18
+            )
+        ])
+        
+        # Physical/Body events
+        events.extend([
+            GameEvent(
+                id="clothes_tight",
+                name="Outgrowing Clothes",
+                description="Maddy notices her clothes fitting differently",
+                event_type=EventType.PHYSICAL,
+                trigger=EventTrigger.USER_ACTION,
+                probability=0.4,
+                conditions={"weight_gained_recently": 5, "new_day": True},
+                effects={"body_awareness": 0.6, "mood_change": "self_conscious"},
+                prompts=[
+                    "*tugs at shirt* Hmm... this feels a bit snugger than usual. Have you noticed?",
+                    "*looks down at herself* I think I might need to go shopping soon... these jeans are getting pretty tight.",
+                    "*blushes slightly* I hope you don't mind, but I think all that good food is starting to show..."
+                ],
+                user_suggestions=[
+                    "You look beautiful just as you are.",
+                    "I love how you look. Don't worry about it.",
+                    "Want to go shopping together for new clothes?"
+                ],
+                duration=2,
+                cooldown=12
+            ),
+            
+            GameEvent(
+                id="mirror_moment",
+                name="Self-Reflection",
+                description="Maddy looks at herself in a mirror",
+                event_type=EventType.PHYSICAL,
+                trigger=EventTrigger.RANDOM,
+                probability=0.25,
+                conditions={"weight_change": True},
+                effects={"self_awareness": 0.5, "emotional_complexity": True},
+                prompts=[
+                    "*catches reflection in mirror* Sometimes I barely recognize myself... is that weird?",
+                    "*stands sideways in front of mirror* I can definitely see the changes... how do you feel about it?",
+                    "*traces her silhouette* My body is telling a different story now... our story, I guess."
+                ],
+                user_suggestions=[
+                    "You're beautiful at any size.",
+                    "I love watching you become more confident.",
+                    "Every change just makes you more yourself."
+                ],
+                duration=2,
+                cooldown=20
+            )
+        ])
+        
+        # Activity events
+        events.extend([
+            GameEvent(
+                id="movie_night",
+                name="Cozy Movie Night",
+                description="Perfect opportunity for a relaxing evening",
+                event_type=EventType.ACTIVITY,
+                trigger=EventTrigger.TIME_BASED,
+                probability=0.4,
+                conditions={"time_of_day": ["evening"], "relationship_score": 1.5},
+                effects={"intimacy_increase": 0.3, "relaxation": 0.5},
+                prompts=[
+                    "*curls up on couch* Want to watch something together? I'm in the mood for something cozy...",
+                    "I found this movie I think we'd both enjoy... want to make it a proper movie night?",
+                    "*pats couch beside her* Come sit with me? I want to just relax and spend time with you."
+                ],
+                user_suggestions=[
+                    "That sounds perfect. What should we watch?",
+                    "I'd love to. Let me get some snacks.",
+                    "Movie night with you sounds amazing."
+                ],
+                duration=3,
+                cooldown=8
+            ),
+            
+            GameEvent(
+                id="walk_together",
+                name="Evening Stroll",
+                description="Suggestion for a romantic walk",
+                event_type=EventType.ACTIVITY,
+                trigger=EventTrigger.CONVERSATION_LULL,
+                probability=0.3,
+                conditions={"time_of_day": ["evening", "afternoon"], "weather": "pleasant"},
+                effects={"romance_increase": 0.4, "mood": "peaceful"},
+                prompts=[
+                    "It's such a beautiful evening... want to take a walk with me?",
+                    "*looks out window* The weather looks perfect for a stroll. Care to join me?",
+                    "I love walking when it's like this... especially with good company. Interested?"
+                ],
+                user_suggestions=[
+                    "I'd love to walk with you.",
+                    "That sounds really nice and peaceful.",
+                    "Let's go! I enjoy spending time with you."
+                ],
+                duration=2,
+                cooldown=10
+            )
+        ])
+        
+        # Weather/Mood events
+        events.extend([
+            GameEvent(
+                id="rainy_day",
+                name="Rainy Day Vibes",
+                description="Rain creates a cozy atmosphere",
+                event_type=EventType.WEATHER,
+                trigger=EventTrigger.RANDOM,
+                probability=0.2,
+                conditions={},
+                effects={"coziness": 0.6, "intimacy_opportunity": True},
+                prompts=[
+                    "*listens to rain* I love rainy days... they make everything feel so cozy and intimate.",
+                    "*watches raindrops on window* There's something romantic about being inside while it's raining...",
+                    "*snuggles closer* Perfect weather for staying in and just... being together, don't you think?"
+                ],
+                user_suggestions=[
+                    "I love rainy days too. So peaceful.",
+                    "Want to snuggle up together?",
+                    "This is perfect weather for quality time."
+                ],
+                duration=2,
+                cooldown=25
+            ),
+            
+            GameEvent(
+                id="sunny_mood",
+                name="Bright Day Energy",
+                description="Beautiful weather lifts spirits",
+                event_type=EventType.WEATHER,
+                trigger=EventTrigger.RANDOM,
+                probability=0.3,
+                conditions={},
+                effects={"mood": "happy", "energy_boost": 0.4},
+                prompts=[
+                    "*stretches in sunlight* What a gorgeous day! I feel so energized and happy!",
+                    "*spins around happily* Days like this make me feel like anything is possible!",
+                    "*beams with joy* The sunshine is making me feel so... alive! Want to do something fun?"
+                ],
+                user_suggestions=[
+                    "Your happiness is contagious!",
+                    "I love seeing you this cheerful!",
+                    "What should we do with all this energy?"
+                ],
+                duration=2,
+                cooldown=15
+            )
+        ])
+        
+        # Surprise events
+        events.extend([
+            GameEvent(
+                id="unexpected_gift",
+                name="Small Surprise",
+                description="Maddy has a small gift or surprise",
+                event_type=EventType.SURPRISE,
+                trigger=EventTrigger.RELATIONSHIP_MILESTONE,
+                probability=0.2,
+                conditions={"relationship_score": 4.0, "days_together": 5},
+                effects={"romance_major_boost": 0.6, "surprise_factor": 0.8},
+                prompts=[
+                    "*hides something behind back* I... I got you something. It's not much, but I saw it and thought of you...",
+                    "*looks nervous but excited* So, I might have done something a little impulsive... I hope you like it!",
+                    "*pulls out small wrapped item* I've been wanting to give this to you for a while now..."
+                ],
+                user_suggestions=[
+                    "You didn't have to do that! That's so sweet!",
+                    "I'm touched that you thought of me.",
+                    "What is it? I'm excited to see!"
+                ],
+                duration=2,
+                cooldown=30
+            ),
+            
+            GameEvent(
+                id="memory_trigger",
+                name="Remembering Together",
+                description="Maddy brings up a shared memory",
+                event_type=EventType.EMOTIONAL,
+                trigger=EventTrigger.RANDOM,
+                probability=0.3,
+                conditions={"relationship_score": 2.0, "shared_memories": True},
+                effects={"nostalgia": 0.5, "bond_strengthening": 0.4},
+                prompts=[
+                    "*smiles fondly* Do you remember when we... *trails off with a happy expression*",
+                    "I was just thinking about that time we... that was really special to me.",
+                    "*looks at you warmly* We've made some really good memories together, haven't we?"
+                ],
+                user_suggestions=[
+                    "I remember that too. It was wonderful.",
+                    "Those are some of my favorite memories.",
+                    "I love the memories we're making together."
+                ],
+                duration=2,
+                cooldown=20
+            )
+        ])
+        
+        return events
+    
+    def update(self, conversation_context: str = "", user_input: str = "", 
+               character_response: str = "") -> Optional[GameEvent]:
+        """Update event system and potentially trigger new events"""
+        current_time = time.time()
+        
+        # Track conversation patterns
+        if not user_input.strip() or len(user_input.split()) < 3:
+            self.conversation_silence_count += 1
+        else:
+            self.conversation_silence_count = 0
+            
+        # Update scene momentum based on conversation
+        if character_response:
+            emotion_indicators = {
+                'high': ['excited', 'amazing', 'love', 'incredible', 'fantastic'],
+                'low': ['tired', 'quiet', 'calm', 'peaceful', 'sleepy']
+            }
+            
+            response_lower = character_response.lower()
+            if any(word in response_lower for word in emotion_indicators['high']):
+                self.scene_momentum = min(1.0, self.scene_momentum + 0.2)
+            elif any(word in response_lower for word in emotion_indicators['low']):
+                self.scene_momentum = max(0.0, self.scene_momentum - 0.2)
+        
+        # Check for event triggers
+        triggered_event = self._check_event_triggers(current_time, user_input, character_response)
+        
+        # Update active events
+        self._update_active_events()
+        
+        return triggered_event
+    
+    def _check_event_triggers(self, current_time: float, user_input: str, 
+                            character_response: str) -> Optional[GameEvent]:
+        """Check if any events should be triggered"""
+        
+        # Get current game state
+        game_state = self._get_current_game_state()
+        
+        # Filter events that can potentially trigger
+        potential_events = []
+        for event in self.events:
+            if self._can_event_trigger(event, game_state, current_time):
+                potential_events.append(event)
+        
+        if not potential_events:
+            return None
+            
+        # Sort by priority and probability
+        potential_events.sort(key=lambda e: (e.probability, -e.times_triggered))
+        
+        # Use weighted random selection
+        weights = [event.probability for event in potential_events]
+        if random.random() < max(weights) * self._get_event_multiplier():
+            selected_event = random.choices(potential_events, weights=weights)[0]
+            return self._trigger_event(selected_event, current_time)
+            
+        return None
+    
+    def _can_event_trigger(self, event: GameEvent, game_state: Dict, 
+                         current_time: float) -> bool:
+        """Check if an event can trigger based on conditions"""
+        
+        # Check cooldown
+        if current_time - event.last_triggered < event.cooldown * 60:  # Convert to seconds
+            return False
+            
+        # Check basic conditions
+        conditions = event.conditions
+        
+        # Relationship score check
+        if 'relationship_score' in conditions:
+            if game_state['relationship_score'] < conditions['relationship_score']:
+                return False
+                
+        # Time of day check
+        if 'time_of_day' in conditions:
+            current_hour = int(time.strftime('%H'))
+            time_periods = {
+                'morning': range(6, 12),
+                'afternoon': range(12, 17),
+                'evening': range(17, 22),
+                'late_night': list(range(22, 24)) + list(range(0, 6))
+            }
+            
+            current_period = None
+            for period, hours in time_periods.items():
+                if current_hour in hours:
+                    current_period = period
+                    break
+                    
+            if current_period not in conditions['time_of_day']:
+                return False
+        
+        # Mood check
+        if 'mood' in conditions:
+            if game_state['current_mood'] not in conditions['mood']:
+                return False
+                
+        # Weight/physical checks
+        if 'weight_gained_recently' in conditions:
+            if game_state['weight_gain_recent'] < conditions['weight_gained_recently']:
+                return False
+                
+        # Trigger-specific checks
+        if event.trigger == EventTrigger.CONVERSATION_LULL:
+            if self.conversation_silence_count < 2:
+                return False
+                
+        return True
+    
+    def _get_current_game_state(self) -> Dict[str, Any]:
+        """Get current game state for event evaluation"""
+        return {
+            'relationship_score': self.relationship.get_relationship_score(),
+            'current_mood': self.mind.get_mood(),
+            'weight_gain_recent': self.character.get_weight_diff(),
+            'calories_today': self.character.get_calories(),
+            'scene_momentum': self.scene_momentum,
+            'days_together': self.time_system.get_day()
+        }
+    
+    def _get_event_multiplier(self) -> float:
+        """Get multiplier for event probability based on current state"""
+        base_multiplier = 0.3  # Base chance for events
+        
+        # Increase chance during conversation lulls
+        if self.conversation_silence_count > 3:
+            base_multiplier *= 1.5
+            
+        # Adjust based on scene momentum
+        if self.scene_momentum > 0.7:
+            base_multiplier *= 1.2  # High energy = more events
+        elif self.scene_momentum < 0.3:
+            base_multiplier *= 0.8  # Low energy = fewer events
+            
+        # Time since last event
+        time_since_last = time.time() - self.last_event_time
+        if time_since_last > 300:  # 5 minutes
+            base_multiplier *= 1.3
+            
+        return min(1.0, base_multiplier)
+    
+    def _trigger_event(self, event: GameEvent, current_time: float) -> GameEvent:
+        """Trigger an event and update tracking"""
+        event.last_triggered = current_time
+        event.times_triggered += 1
+        self.last_event_time = current_time
+        
+        # Add to active events if it has duration
+        if event.duration > 0:
+            self.active_events.append(event)
+            
+        # Record in history
+        self.event_history.append({
+            'event_id': event.id,
+            'triggered_at': current_time,
+            'game_state': self._get_current_game_state()
+        })
+        
+        return event
+    
+    def _update_active_events(self):
+        """Update active events and remove expired ones"""
+        self.active_events = [event for event in self.active_events 
+                            if event.duration > 0]
+        
+        # Reduce duration of active events
+        for event in self.active_events:
+            event.duration -= 1
+    
+    def get_random_prompt_enhancement(self, base_context: str) -> str:
+        """Add random environmental details to enhance prompts"""
+        enhancements = [
+            "*soft music plays in the background*",
+            "*afternoon sunlight streams through the window*",
+            "*the room feels cozy and intimate*",
+            "*a gentle breeze comes through the open window*",
+            "*the sound of distant laughter can be heard*",
+            "*candles flicker softly nearby*",
+            "*the scent of something delicious wafts from the kitchen*",
+            "*rain patters gently against the window*",
+            "*the house is quiet and peaceful*",
+            "*warm lighting creates a comfortable atmosphere*"
+        ]
+        
+        if random.random() < 0.3:  # 30% chance to add enhancement
+            enhancement = random.choice(enhancements)
+            return f"{enhancement}\n\n{base_context}"
+        
+        return base_context
+    
+    def get_scene_suggestions(self) -> List[str]:
+        """Get suggestions for scene direction based on current state"""
+        suggestions = []
+        game_state = self._get_current_game_state()
+        
+        # Relationship-based suggestions
+        if game_state['relationship_score'] < 2.0:
+            suggestions.extend([
+                "Share something personal about yourself",
+                "Ask about her interests and hobbies",
+                "Offer to do an activity together"
+            ])
+        elif game_state['relationship_score'] < 4.0:
+            suggestions.extend([
+                "Show physical affection (hand holding, etc.)",
+                "Plan a special activity together",
+                "Have a deeper conversation about feelings"
+            ])
+        else:
+            suggestions.extend([
+                "Express your feelings directly",
+                "Suggest a romantic gesture",
+                "Talk about your future together"
+            ])
+            
+        # Mood-based suggestions
+        if game_state['current_mood'] in ['sad', 'anxious']:
+            suggestions.extend([
+                "Offer comfort and support",
+                "Suggest a calming activity",
+                "Give her reassurance"
+            ])
+        elif game_state['current_mood'] in ['happy', 'excited']:
+            suggestions.extend([
+                "Share in her enthusiasm",
+                "Suggest an energetic activity",
+                "Compliment her mood"
+            ])
+            
+        return random.sample(suggestions, min(3, len(suggestions)))
+    
+    def get_event_history_summary(self) -> str:
+        """Get a summary of recent events for context"""
+        if not self.event_history:
+            return "No recent events."
+            
+        recent_events = self.event_history[-5:]  # Last 5 events
+        summary = "Recent events:\n"
+        
+        for event_record in recent_events:
+            event = next((e for e in self.events if e.id == event_record['event_id']), None)
+            if event:
+                summary += f"- {event.name}: {event.description}\n"
+                
+        return summary
+    
+    def export_events(self, filename: str = "events_data.json"):
+        """Export event data for persistence"""
+        export_data = {
+            'event_history': self.event_history,
+            'scene_momentum': self.scene_momentum,
+            'conversation_silence_count': self.conversation_silence_count,
+            'last_event_time': self.last_event_time,
+            'events_triggered_count': {event.id: event.times_triggered for event in self.events}
+        }
+        
+        with open(filename, 'w') as f:
+            json.dump(export_data, f, indent=2)
+    
+    def import_events(self, filename: str = "events_data.json") -> bool:
+        """Import event data from file"""
+        try:
+            with open(filename, 'r') as f:
+                data = json.load(f)
+                
+            self.event_history = data.get('event_history', [])
+            self.scene_momentum = data.get('scene_momentum', 0.5)
+            self.conversation_silence_count = data.get('conversation_silence_count', 0)
+            self.last_event_time = data.get('last_event_time', time.time())
+            
+            # Restore event trigger counts
+            triggered_counts = data.get('events_triggered_count', {})
+            for event in self.events:
+                event.times_triggered = triggered_counts.get(event.id, 0)
+                
+            return True
+            
+        except Exception as e:
+            print(f"Error importing events: {e}")
+            return False
EOF
)
