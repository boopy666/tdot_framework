#!/usr/bin/env python3
"""
Standalone Dating Simulator with Weight Gain Mechanics
Uses LM Studio API for language model interactions
CLI-based interface
"""

import os
import sys
import json
import requests
import random
import datetime
import time
from typing import Dict, Any, List
from classes import Character, Time, Mind, Relationship, Description, simple_emotion_classifier
from memory_system import ConversationalMemorySystem, MemoryCategories
from event_system import EventManager, GameEvent, EventType

class LMStudioAPI:
    """Interface for LM Studio API"""
    
    def __init__(self, base_url: str = "http://localhost:1234", model_name: str = None):
        self.base_url = base_url.rstrip('/')
        self.model_name = model_name
        self.session = requests.Session()
        
    def generate_response(self, prompt: str, max_tokens: int = 1028, temperature: float = 1.0, 
                         top_p: float = 0.9) -> str:
        """Generate response using LM Studio API"""
        url = f"{self.base_url}/v1/chat/completions"
        
        payload = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "stream": False
        }
        
        if self.model_name:
            payload["model"] = self.model_name
            
        try:
            response = self.session.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            return data['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with LM Studio: {e}")
            return "I'm having trouble responding right now. Please try again."
        except KeyError as e:
            print(f"Unexpected response format from LM Studio: {e}")
            return "I received an unexpected response format. Please try again."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Something went wrong. Please try again."

class DatingSimulator:
    """Main dating simulator game engine"""
    
    def __init__(self, lm_studio_url: str = "http://localhost:1234"):
        # Initialize LM Studio API
        self.llm = LMStudioAPI(lm_studio_url)
        
        # Initialize game objects
        self.character = Character("Maddy", 19, 230, 62)
        self.time = Time(self.character, birth_day=6, birth_month=5, 
                        current_year=2024, current_month=6, current_day=20)
        self.mind = Mind()
        self.relationship = Relationship()
        self.description = Description(self.character)
        
        # Initialize advanced memory system
        self.memory_system = ConversationalMemorySystem(max_memories=1000, refinement_interval=25)
        
        # Initialize event system
        self.event_manager = EventManager(self.character, self.time, self.relationship, self.mind)
        
        # Game state
        self.conversation_history = []
        self.user_name = "Player"
        self.game_running = True
        self.pending_event = None
        
    def generate_context_prompt(self, user_input: str = "") -> str:
        """Generate the character context prompt for the LLM with memory integration"""
        height = self.character.calculate_height_feet()
        
        # Get relevant memories for context
        relevant_memories = []
        if user_input:
            relevant_memories = self.memory_system.retrieve_relevant_memories(
                user_input, 
                context=f"Current conversation with {self.user_name}",
                max_memories=3
            )
        
        # Build memory context
        memory_context = ""
        if relevant_memories:
            memory_context = "\n\nRelevant memories and personality traits:\n"
            for memory in relevant_memories:
                memory_context += f"- {memory.content}\n"
        
        # Get character summary for personality consistency
        character_summary = self.memory_system.get_character_summary()
        
        # Build personality traits from memory
        personality_from_memory = ""
        if character_summary['personality_traits']:
            personality_from_memory = f"\nEstablished personality: {'; '.join(character_summary['personality_traits'][:3])}"
        
        # Add event context if there's a pending event
        event_context = ""
        if self.pending_event:
            event_prompt = random.choice(self.pending_event.prompts)
            event_context = f"\n\nCurrent situation: {event_prompt}"
            
        # Add environmental enhancement
        base_context = f"""[character("{self.character.name}")
{{
Species("Human")
Age("{self.character.get_age()} years old")
Weight("{self.character.get_weight()} lbs")
Obesity("BMI: {self.character.calculate_bmi()}" + "Class: {self.character.calculate_bmi_class()}")
Features("{self.character.hair} hair" + "{self.character.eye_color} eyes" + "{self.character.skin} skin tone" + "{self.character.nose}" + "{self.character.eye_shape}" + "{self.character.lips}" + "{self.character.cheeks}" + "{self.character.face}" + "{self.character.smile}")
Height("{self.character.calculate_height_cm()} cm" + "{int(height[0])} feet {height[1]} inches tall")
Mind({self.mind.formatted_mind_traits()})
Personality({self.mind.formatted_personality_traits()})
Mood("{self.mind.get_mood()}")
Relationship("Relationship status with {self.user_name} is: {self.relationship.calculate_relationship()}")
Loves({self.mind.formatted_loves()})
Hates({self.mind.formatted_hates()})
Time("Today's date is {self.time.get_formatted_current_date()}" + "{self.character.name}'s birthday is {self.time.get_formatted_birth_date()}" + "In {self.time.get_day()} days {self.character.name} has gained {self.character.get_weight_diff()} lbs")
Description("Introverted yet yearning to break out of her shell and be accepted." + "Passionate video game geek with an encyclopedic knowledge of gaming trivia." + "Follows pop culture and social media trends to stay connected and relevant." + "Kindhearted but socially awkward, often misreading signals from her peers." + "Struggles with low self-esteem, body image issues, and bouts of anxiety.")
{personality_from_memory}
}}]{memory_context}

You are roleplaying as {self.character.name}. Respond as her in first person. Be authentic to her personality, current mood, and relationship status. Show character growth and development over time. React appropriately to food, social situations, and relationship developments. Remember and reference past conversations and established personality traits.

Current situation: You are spending time with {self.user_name}.{event_context}"""
        
        # Apply random environmental enhancement
        enhanced_context = self.event_manager.get_random_prompt_enhancement(base_context)
        
        return enhanced_context
        
    def process_user_input(self, user_input: str) -> str:
        """Process user input and return character response with memory integration"""
        # Check for special commands
        if user_input.startswith('=='):
            return self.handle_special_command(user_input)
            
        # Process food offerings
        food_response = self.process_food_input(user_input)
        
        # Calculate sentiment for relationship changes
        self.relationship.calculate_sentiment_score(user_input)
        
        # Determine emotional tone of user input
        emotion_scores = simple_emotion_classifier(user_input)
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        
        # Generate LLM response with memory context
        context = self.generate_context_prompt(user_input)
        
        # Build conversation history for context (shorter since we have memory system)
        conversation_context = ""
        if self.conversation_history:
            conversation_context = "\n\nRecent conversation:\n"
            for exchange in self.conversation_history[-2:]:  # Last 2 exchanges only
                conversation_context += f"{self.user_name}: {exchange['user']}\n{self.character.name}: {exchange['character']}\n"
                
        full_prompt = f"{context}\n{conversation_context}\n{self.user_name}: {user_input}\n{self.character.name}:"
        
        character_response = self.llm.generate_response(full_prompt)
        
        # Calculate sentiment for character response
        self.relationship.calculate_sentiment_score(character_response)
        character_emotion_scores = simple_emotion_classifier(character_response)
        character_emotion = max(character_emotion_scores, key=character_emotion_scores.get)
        
        # Add conversation turn to memory system
        self.memory_system.add_conversation_turn(
            user_input=user_input,
            character_response=character_response,
            emotional_tone=character_emotion
        )
        
        # Update event system and check for new events
        triggered_event = self.event_manager.update(
            conversation_context=character_response,
            user_input=user_input,
            character_response=character_response
        )
        
        # Handle event triggers
        event_response = ""
        if triggered_event:
            self.pending_event = triggered_event
            event_response = f"\n\n🎭 *{triggered_event.description}*"
            
            # Show user suggestions if available
            if triggered_event.user_suggestions:
                suggestions = triggered_event.user_suggestions
                event_response += "\n\n💡 *You could say:*"
                for i, suggestion in enumerate(suggestions[:3], 1):
                    event_response += f"\n{i}. \"{suggestion}\""
        
        # Clear pending event if user responded to it
        if self.pending_event and user_input:
            self.pending_event = None
            
        # Add to conversation history (keep for backwards compatibility)
        self.conversation_history.append({
            'user': user_input,
            'character': character_response
        })
        
        # Combine all responses
        full_response = ""
        if food_response:
            full_response += food_response + "\n\n"
        full_response += character_response
        if event_response:
            full_response += event_response
        
        return full_response
        
    def process_food_input(self, user_input: str) -> str:
        """Process food offerings in user input"""
        import re
        
        food_matches = re.findall(r"\{([^}]+):(\d+)\}", user_input)
        food_messages = []
        
        for food_item, calories in food_matches:
            self.character.add_calories(int(calories))
            fullness_status = self.character.calculate_fullness()
            food_messages.append(
                f"*[{self.character.name} just ate {food_item}]*\n"
                f"*After eating this, {self.character.name} is feeling {fullness_status}.*"
            )
            
        return "\n".join(food_messages)
        
    def handle_special_command(self, command: str) -> str:
        """Handle special game commands"""
        command = command.strip()
        
        if command == "==END_DAY==":
            return self.end_day()
        elif command.startswith("==STATS=="):
            return self.show_stats()
        elif command.startswith("==HELP=="):
            return self.show_help()
        elif command.startswith("==SAVE=="):
            return self.save_game()
        elif command.startswith("==LOAD=="):
            return self.load_game()
        elif command.startswith("==MEMORY=="):
            return self.show_memory_stats()
        elif command.startswith("==MEMORIES=="):
            return self.show_recent_memories()
        elif command.startswith("==PERSONALITY=="):
            return self.show_personality_summary()
        elif command.startswith("==EVENTS=="):
            return self.show_event_status()
        elif command.startswith("==SUGGESTIONS=="):
            return self.show_scene_suggestions()
        else:
            return "Unknown command. Type ==HELP== for available commands."
            
    def end_day(self) -> str:
        """End the current day and advance time"""
        self.time.end_day()
        
        birthday_message = ""
        if self.time.current_month == self.time.birth_month and self.time.current_day == self.time.birth_day:
            birthday_message = f"\n🎉 It's {self.character.name}'s birthday! She is now {self.character.age} years old! 🎂"
            
        weight_change = ""
        if self.character.get_weight_diff() > 0:
            weight_change = f"\n📈 {self.character.name} has gained {self.character.get_weight_diff()} lbs recently!"
            
        return f"🌅 *A new day begins!*{birthday_message}{weight_change}\n💭 {self.character.name} is feeling {self.mind.get_mood()} today."
        
    def show_stats(self) -> str:
        """Show character stats"""
        stats = f"""📊 **Character Stats for {self.character.name}**
        
👤 **Basic Info:**
• Age: {self.character.get_age()} years old
• Weight: {self.character.get_weight()} lbs
• Height: {self.character.calculate_height_cm()} cm ({int(self.character.calculate_height_feet()[0])} feet {self.character.calculate_height_feet()[1]} inches)
• BMI: {self.character.calculate_bmi()} ({self.character.calculate_bmi_class()})

📏 **Measurements:**
• Chest: {self.character.get_chest()}"
• Waist: {self.character.get_waist()}"  
• Hips: {self.character.get_hips()}"
• Clothing Size: {self.character.clothing}

🍽️ **Nutrition:**
• Daily Calories: {self.character.get_calories()}/{int(self.character.max_calories)}
• Fullness: {self.character.calculate_fullness()}

💭 **Mental State:**
• Current Mood: {self.mind.get_mood()}
• Personality: {', '.join(self.mind.personality_traits[:3])}...

❤️ **Relationship:**
• Status: {self.relationship.calculate_relationship()}
• Score: {self.relationship.get_relationship_score():.1f}/10.0

📅 **Time:**
• Current Date: {self.time.get_formatted_current_date()}
• Days in Simulation: {self.time.get_day()}
• Birthday: {self.time.get_formatted_birth_date()}
"""
        return stats
        
    def show_help(self) -> str:
        """Show help information"""
        help_text = """🆘 **Dating Simulator Help**

**Basic Interaction:**
Just type normally to chat with {character_name}!

**Food System:**
Offer food using: {{food_name:calories}}
Example: "Want some pizza? {{pizza:800}}"

**Special Commands:**
• ==END_DAY== - Advance to the next day
• ==STATS== - Show character statistics  
• ==MEMORY== - Show memory system statistics
• ==MEMORIES== - Show recent character memories
• ==PERSONALITY== - Show personality summary from memories
• ==EVENTS== - Show active events and event history
• ==SUGGESTIONS== - Get scene suggestions for interaction
• ==HELP== - Show this help message
• ==SAVE== - Save your game progress
• ==LOAD== - Load saved game progress
• ==QUIT== - Exit the game

**Tips:**
• Be kind and considerate to improve your relationship
• Food choices affect weight and mood
• Character personality evolves over time
• Pay attention to moods and reactions

Have fun exploring your relationship with {character_name}! 💕
""".format(character_name=self.character.name)
        return help_text
        
    def save_game(self) -> str:
        """Save game state to file"""
        try:
            save_data = {
                'character': {
                    'name': self.character.name,
                    'age': self.character.age,
                    'weight': self.character.weight,
                    'height': self.character.height,
                    'calories': self.character.calories,
                    'weight_diff': self.character.weight_diff,
                    'eye_color': self.character.eye_color,
                    'hair': self.character.hair,
                    'skin': self.character.skin
                },
                'time': {
                    'current_year': self.time.current_year,
                    'current_month': self.time.current_month,
                    'current_day': self.time.current_day,
                    'day': self.time.day,
                    'birth_day': self.time.birth_day,
                    'birth_month': self.time.birth_month
                },
                'mind': {
                    'current_mood': self.mind.current_mood,
                    'mind_traits': self.mind.mind_traits,
                    'personality_traits': self.mind.personality_traits,
                    'loves': self.mind.loves,
                    'hates': self.mind.hates
                },
                'relationship': {
                    'relationship_score': self.relationship.relationship_score,
                    'relationship_status': self.relationship.relationship_status
                },
                'user_name': self.user_name,
                'conversation_history': self.conversation_history[-10:]  # Save last 10 exchanges
            }
            
            with open('savegame.json', 'w') as f:
                json.dump(save_data, f, indent=2)
                
            # Export memory system separately
            self.memory_system.export_memories('memory_data.json')
            
            # Export event system
            self.event_manager.export_events('events_data.json')
                
            return "💾 Game, memory, and event data saved successfully!"
            
        except Exception as e:
            return f"❌ Error saving game: {e}"
            
    def load_game(self) -> str:
        """Load game state from file"""
        try:
            if not os.path.exists('savegame.json'):
                return "❌ No save file found!"
                
            with open('savegame.json', 'r') as f:
                save_data = json.load(f)
                
            # Restore character
            char_data = save_data['character']
            self.character.name = char_data['name']
            self.character.age = char_data['age']
            self.character.weight = char_data['weight']
            self.character.height = char_data['height']
            self.character.calories = char_data['calories']
            self.character.weight_diff = char_data['weight_diff']
            self.character.eye_color = char_data['eye_color']
            self.character.hair = char_data['hair']
            self.character.skin = char_data['skin']
            
            # Restore time
            time_data = save_data['time']
            self.time.current_year = time_data['current_year']
            self.time.current_month = time_data['current_month']
            self.time.current_day = time_data['current_day']
            self.time.day = time_data['day']
            self.time.birth_day = time_data['birth_day']
            self.time.birth_month = time_data['birth_month']
            
            # Restore mind
            mind_data = save_data['mind']
            self.mind.current_mood = mind_data['current_mood']
            self.mind.mind_traits = mind_data['mind_traits']
            self.mind.personality_traits = mind_data['personality_traits']
            self.mind.loves = mind_data['loves']
            self.mind.hates = mind_data['hates']
            
            # Restore relationship
            rel_data = save_data['relationship']
            self.relationship.relationship_score = rel_data['relationship_score']
            self.relationship.relationship_status = rel_data['relationship_status']
            
            # Restore other data
            self.user_name = save_data['user_name']
            self.conversation_history = save_data['conversation_history']
            
            # Import memory system if available
            memory_loaded = self.memory_system.import_memories('memory_data.json')
            
            # Import event system if available
            events_loaded = self.event_manager.import_events('events_data.json')
            
            if memory_loaded and events_loaded:
                return "💾 Game, memory, and event data loaded successfully!"
            elif memory_loaded:
                return "💾 Game and memory data loaded successfully! (Events data not found)"
            elif events_loaded:
                return "💾 Game and event data loaded successfully! (Memory data not found)"
            else:
                return "💾 Game loaded successfully! (Memory and event data not found)"
            
        except Exception as e:
            return f"❌ Error loading game: {e}"
            
    def show_memory_stats(self) -> str:
        """Show comprehensive memory system statistics"""
        stats = self.memory_system.get_memory_stats()
        
        memory_display = f"""🧠 **Memory System Statistics**

📊 **Overview:**
• Total Memories: {stats['total_memories']}
• Conversation Turns: {stats['conversation_turns']}
• Average Importance: {stats['average_importance']:.2f}
• Recent Memories (24h): {stats['recent_memories']}

📁 **Memories by Category:**"""
        
        for category, count in stats['memories_by_category'].items():
            if count > 0:
                memory_display += f"\n• {category.title()}: {count}"
                
        if stats['most_accessed_memories']:
            memory_display += f"\n\n🔥 **Most Referenced Memories:**"
            for i, memory in enumerate(stats['most_accessed_memories'][:3], 1):
                memory_display += f"\n{i}. {memory[:60]}..."
                
        return memory_display
        
    def show_recent_memories(self) -> str:
        """Show recent character memories"""
        # Get memories from the last 24 hours
        recent_memories = []
        current_time = time.time()
        
        for memory in self.memory_system.memories.values():
            if current_time - memory.timestamp < 24 * 3600:  # Last 24 hours
                recent_memories.append(memory)
                
        recent_memories.sort(key=lambda m: m.timestamp, reverse=True)
        
        if not recent_memories:
            return "💭 No recent memories found."
            
        memory_display = "💭 **Recent Character Memories (Last 24 Hours):**\n"
        
        for i, memory in enumerate(recent_memories[:10], 1):
            category_emoji = {
                'personality': '🎭', 'relationship': '❤️', 'preference': '👍',
                'event': '📝', 'physical': '💪', 'emotional': '😊', 'goal': '🎯'
            }
            emoji = category_emoji.get(memory.category, '💭')
            
            memory_display += f"\n{i}. {emoji} {memory.content}"
            if memory.importance > 0.7:
                memory_display += " ⭐"
                
        return memory_display
        
    def show_personality_summary(self) -> str:
        """Show personality summary derived from memories"""
        summary = self.memory_system.get_character_summary()
        
        personality_display = f"🎭 **{self.character.name}'s Personality Summary**\n"
        
        if summary['personality_traits']:
            personality_display += "\n**Core Personality Traits:**"
            for trait in summary['personality_traits'][:5]:
                personality_display += f"\n• {trait}"
                
        if summary['preferences']['likes']:
            personality_display += "\n\n**Things She Enjoys:**"
            for like in summary['preferences']['likes'][:3]:
                personality_display += f"\n• {like}"
                
        if summary['preferences']['dislikes']:
            personality_display += "\n\n**Things She Dislikes:**"
            for dislike in summary['preferences']['dislikes'][:3]:
                personality_display += f"\n• {dislike}"
                
        if summary['goals']:
            personality_display += "\n\n**Goals & Aspirations:**"
            for goal in summary['goals'][:3]:
                personality_display += f"\n• {goal}"
                
        if summary['emotional_patterns']:
            personality_display += "\n\n**Recent Emotional Patterns:**"
            for emotion, count in summary['emotional_patterns'].items():
                if count > 0:
                    personality_display += f"\n• {emotion.title()}: {count} times"
                    
        return personality_display
        
    def show_event_status(self) -> str:
        """Show current event status and recent event history"""
        event_display = "🎭 **Event System Status**\n"
        
        # Show pending event
        if self.pending_event:
            event_display += f"\n🔥 **Active Event:** {self.pending_event.name}"
            event_display += f"\n📝 {self.pending_event.description}"
            event_display += f"\n⏱️ Duration remaining: {self.pending_event.duration} turns"
        else:
            event_display += "\n✨ No active events"
            
        # Show scene momentum
        momentum_desc = "Low" if self.event_manager.scene_momentum < 0.3 else "Medium" if self.event_manager.scene_momentum < 0.7 else "High"
        event_display += f"\n⚡ Scene Energy: {momentum_desc} ({self.event_manager.scene_momentum:.1f})"
        
        # Show recent event history
        history_summary = self.event_manager.get_event_history_summary()
        if "No recent events" not in history_summary:
            event_display += f"\n\n📚 **{history_summary}**"
            
        # Show conversation state
        silence_count = self.event_manager.conversation_silence_count
        if silence_count > 0:
            event_display += f"\n🤐 Conversation lull detected ({silence_count} turns)"
            
        return event_display
        
    def show_scene_suggestions(self) -> str:
        """Show AI-generated suggestions for scene direction"""
        suggestions = self.event_manager.get_scene_suggestions()
        
        suggestion_display = "💡 **Scene Direction Suggestions**\n"
        suggestion_display += "\nBased on current relationship and mood:\n"
        
        for i, suggestion in enumerate(suggestions, 1):
            suggestion_display += f"\n{i}. {suggestion}"
            
        # Add context about current state
        game_state = self.event_manager._get_current_game_state()
        suggestion_display += f"\n\n📊 **Current Context:**"
        suggestion_display += f"\n• Relationship Level: {game_state['relationship_score']:.1f}/10"
        suggestion_display += f"\n• Current Mood: {game_state['current_mood']}"
        suggestion_display += f"\n• Scene Energy: {game_state['scene_momentum']:.1f}/1.0"
        
        return suggestion_display
            
    def run(self):
        """Main game loop"""
        print("🌹 Welcome to the Dating Simulator! 🌹")
        print("A weight gain romance adventure powered by AI")
        print("=" * 50)
        
        # Get user name
        self.user_name = input("What's your name? ").strip() or "Player"
        self.character.set_username(self.user_name)
        
        print(f"\nHello {self.user_name}! You're about to meet {self.character.name}.")
        print("Type ==HELP== at any time for commands and tips.")
        print("=" * 50)
        
        # Initial introduction
        intro_prompt = f"""You are meeting {self.user_name} for the first time. Give a natural, character-appropriate introduction. Be a bit shy but friendly, showing your personality."""
        
        context = self.generate_context_prompt()
        full_prompt = f"{context}\n\nScenario: You are meeting {self.user_name} for the first time.\n{self.character.name}:"
        
        intro_response = self.llm.generate_response(full_prompt)
        print(f"\n{self.character.name}: {intro_response}")
        
        # Main game loop
        while self.game_running:
            try:
                user_input = input(f"\n{self.user_name}: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', '==QUIT==']:
                    print(f"\n{self.character.name}: Goodbye {self.user_name}! Thanks for spending time with me! 💕")
                    self.game_running = False
                    break
                    
                response = self.process_user_input(user_input)
                print(f"\n{self.character.name}: {response}")
                
            except KeyboardInterrupt:
                print(f"\n\n{self.character.name}: Oh! Are you leaving? Goodbye {self.user_name}! 👋")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                print("The game will continue...")

def main():
    """Main entry point"""
    print("🚀 Starting Dating Simulator...")
    
    # Check if LM Studio is running
    try:
        import requests
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code != 200:
            print("⚠️ Warning: LM Studio may not be running or accessible at http://localhost:1234")
            print("Please make sure LM Studio is running with a model loaded.")
            
            choice = input("Continue anyway? (y/N): ").strip().lower()
            if choice != 'y':
                return
                
    except requests.exceptions.RequestException:
        print("⚠️ Warning: Cannot connect to LM Studio at http://localhost:1234")
        print("Please make sure LM Studio is running with a model loaded.")
        
        choice = input("Continue anyway? (y/N): ").strip().lower()
        if choice != 'y':
            return
    
    # Create and run the game
    game = DatingSimulator()
    game.run()

if __name__ == "__main__":
    main()