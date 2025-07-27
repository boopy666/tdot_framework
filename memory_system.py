diff --git a/memory_system.py b/memory_system.py
--- a/memory_system.py
+++ b/memory_system.py
@@ -0,0 +1,687 @@
+#!/usr/bin/env python3
+"""
+Advanced Memory and RAG System for Dating Simulator
+Intelligently stores, retrieves, and refines conversational data
+"""
+
+import json
+import time
+import re
+import hashlib
+from typing import Dict, List, Any, Optional, Tuple
+from dataclasses import dataclass, asdict
+from datetime import datetime, timedelta
+from collections import defaultdict, Counter
+
+@dataclass
+class MemoryEntry:
+    """Single memory entry with metadata"""
+    id: str
+    content: str
+    category: str  # personality, plot, relationship, preference, event
+    importance: float  # 0.0 - 1.0
+    timestamp: float
+    context: str  # surrounding conversation context
+    tags: List[str]
+    frequency_accessed: int = 0
+    last_accessed: float = 0.0
+    emotional_weight: float = 0.0
+    plot_relevance: float = 0.0
+    
+    def update_access(self):
+        """Update access statistics"""
+        self.frequency_accessed += 1
+        self.last_accessed = time.time()
+
+@dataclass
+class ConversationTurn:
+    """Single conversation exchange"""
+    user_input: str
+    character_response: str
+    timestamp: float
+    emotional_tone: str
+    topics: List[str]
+    memory_triggers: List[str]
+
+class MemoryCategories:
+    """Memory categorization constants"""
+    PERSONALITY = "personality"
+    PLOT = "plot"
+    RELATIONSHIP = "relationship"
+    PREFERENCE = "preference"
+    EVENT = "event"
+    PHYSICAL = "physical"
+    EMOTIONAL = "emotional"
+    GOAL = "goal"
+
+class ConversationalMemorySystem:
+    """Advanced memory system with RAG capabilities"""
+    
+    def __init__(self, max_memories: int = 1000, refinement_interval: int = 50):
+        self.memories: Dict[str, MemoryEntry] = {}
+        self.conversation_history: List[ConversationTurn] = []
+        self.max_memories = max_memories
+        self.refinement_interval = refinement_interval
+        self.conversation_count = 0
+        
+        # Memory indexing for fast retrieval
+        self.category_index: Dict[str, List[str]] = defaultdict(list)
+        self.tag_index: Dict[str, List[str]] = defaultdict(list)
+        self.topic_index: Dict[str, List[str]] = defaultdict(list)
+        
+        # Personality tracking
+        self.personality_traits: Dict[str, float] = {}
+        self.preference_patterns: Dict[str, int] = Counter()
+        self.emotional_patterns: Dict[str, List[float]] = defaultdict(list)
+        
+        # Plot tracking
+        self.plot_threads: Dict[str, Dict] = {}
+        self.character_development: List[Dict] = []
+        
+        # Keywords for different categories
+        self.category_keywords = {
+            MemoryCategories.PERSONALITY: [
+                'personality', 'character', 'trait', 'behavior', 'nature', 'tendency',
+                'always', 'never', 'usually', 'often', 'sometimes', 'habits'
+            ],
+            MemoryCategories.RELATIONSHIP: [
+                'relationship', 'love', 'like', 'hate', 'trust', 'friendship',
+                'feelings', 'together', 'couple', 'dating', 'bond', 'connection'
+            ],
+            MemoryCategories.PREFERENCE: [
+                'favorite', 'prefer', 'like', 'dislike', 'enjoy', 'hate',
+                'love', 'want', 'need', 'desire', 'wish', 'hope'
+            ],
+            MemoryCategories.EVENT: [
+                'happened', 'occurred', 'event', 'story', 'experience',
+                'memory', 'remember', 'forgot', 'recall', 'past', 'yesterday'
+            ],
+            MemoryCategories.PHYSICAL: [
+                'weight', 'size', 'clothing', 'appearance', 'body', 'look',
+                'height', 'measurement', 'physical', 'gained', 'lost'
+            ],
+            MemoryCategories.EMOTIONAL: [
+                'feel', 'emotion', 'mood', 'happy', 'sad', 'angry', 'excited',
+                'nervous', 'anxious', 'calm', 'stressed', 'relaxed'
+            ],
+            MemoryCategories.GOAL: [
+                'goal', 'want', 'plan', 'future', 'dream', 'ambition',
+                'achieve', 'accomplish', 'succeed', 'aspire', 'hope'
+            ]
+        }
+        
+    def add_conversation_turn(self, user_input: str, character_response: str, 
+                           emotional_tone: str = "neutral") -> None:
+        """Add a new conversation turn and extract memories"""
+        timestamp = time.time()
+        
+        # Extract topics and themes
+        topics = self._extract_topics(user_input + " " + character_response)
+        memory_triggers = self._extract_memory_triggers(user_input, character_response)
+        
+        # Create conversation turn
+        turn = ConversationTurn(
+            user_input=user_input,
+            character_response=character_response,
+            timestamp=timestamp,
+            emotional_tone=emotional_tone,
+            topics=topics,
+            memory_triggers=memory_triggers
+        )
+        
+        self.conversation_history.append(turn)
+        self.conversation_count += 1
+        
+        # Extract and store memories from this turn
+        self._extract_memories_from_turn(turn)
+        
+        # Update patterns
+        self._update_patterns(turn)
+        
+        # Periodic memory refinement
+        if self.conversation_count % self.refinement_interval == 0:
+            self._refine_memories()
+            
+    def _extract_topics(self, text: str) -> List[str]:
+        """Extract main topics from text"""
+        # Simple keyword-based topic extraction
+        topics = []
+        text_lower = text.lower()
+        
+        topic_keywords = {
+            'food': ['eat', 'food', 'hungry', 'meal', 'cooking', 'restaurant', 'diet'],
+            'gaming': ['game', 'gaming', 'video', 'play', 'console', 'pc', 'stream'],
+            'relationship': ['love', 'relationship', 'dating', 'boyfriend', 'girlfriend'],
+            'body': ['weight', 'body', 'size', 'appearance', 'clothes', 'fat', 'thin'],
+            'emotions': ['feel', 'emotion', 'happy', 'sad', 'angry', 'excited'],
+            'future': ['future', 'plan', 'goal', 'dream', 'want', 'hope'],
+            'past': ['past', 'remember', 'used to', 'before', 'history'],
+            'social': ['friends', 'family', 'people', 'social', 'party', 'meet']
+        }
+        
+        for topic, keywords in topic_keywords.items():
+            if any(keyword in text_lower for keyword in keywords):
+                topics.append(topic)
+                
+        return topics
+        
+    def _extract_memory_triggers(self, user_input: str, character_response: str) -> List[str]:
+        """Extract memory triggers that should recall past conversations"""
+        triggers = []
+        combined_text = (user_input + " " + character_response).lower()
+        
+        # Look for references to past events
+        past_references = [
+            'remember', 'recall', 'mentioned', 'told', 'said', 'discussed',
+            'talked about', 'brought up', 'like before', 'as usual'
+        ]
+        
+        for ref in past_references:
+            if ref in combined_text:
+                triggers.append(ref)
+                
+        return triggers
+        
+    def _extract_memories_from_turn(self, turn: ConversationTurn) -> None:
+        """Extract and store important memories from a conversation turn"""
+        combined_text = turn.user_input + " " + turn.character_response
+        
+        # Extract different types of memories
+        self._extract_personality_memories(turn)
+        self._extract_preference_memories(turn)
+        self._extract_event_memories(turn)
+        self._extract_relationship_memories(turn)
+        self._extract_physical_memories(turn)
+        self._extract_emotional_memories(turn)
+        self._extract_goal_memories(turn)
+        
+    def _extract_personality_memories(self, turn: ConversationTurn) -> None:
+        """Extract personality-related memories"""
+        patterns = [
+            r"(i am|i'm|i feel like i'm|i tend to be|i usually|i always|i never) ([^.!?]+)",
+            r"(that's just how i am|that's me|that's my personality|i'm the type of person who) ([^.!?]+)",
+            r"(i have a tendency to|my nature is to|i'm naturally) ([^.!?]+)"
+        ]
+        
+        for pattern in patterns:
+            matches = re.finditer(pattern, turn.character_response.lower())
+            for match in matches:
+                trait = match.group(2).strip()
+                if len(trait) > 5:  # Filter out very short matches
+                    self._store_memory(
+                        content=f"Personality trait: {trait}",
+                        category=MemoryCategories.PERSONALITY,
+                        importance=0.8,
+                        context=turn.character_response,
+                        tags=['personality', 'trait'],
+                        emotional_weight=self._calculate_emotional_weight(turn.emotional_tone),
+                        plot_relevance=0.6
+                    )
+                    
+    def _extract_preference_memories(self, turn: ConversationTurn) -> None:
+        """Extract preference-related memories"""
+        patterns = [
+            r"(i love|i really like|i enjoy|i prefer|my favorite) ([^.!?]+)",
+            r"(i hate|i dislike|i can't stand|i don't like) ([^.!?]+)",
+            r"(i want|i need|i desire|i crave|i wish for) ([^.!?]+)"
+        ]
+        
+        for pattern in patterns:
+            matches = re.finditer(pattern, turn.character_response.lower())
+            for match in matches:
+                preference = match.group(2).strip()
+                sentiment = "positive" if any(word in match.group(1) for word in ['love', 'like', 'enjoy', 'prefer', 'favorite']) else "negative"
+                
+                if len(preference) > 3:
+                    self._store_memory(
+                        content=f"Preference ({sentiment}): {preference}",
+                        category=MemoryCategories.PREFERENCE,
+                        importance=0.7,
+                        context=turn.character_response,
+                        tags=['preference', sentiment],
+                        emotional_weight=self._calculate_emotional_weight(turn.emotional_tone),
+                        plot_relevance=0.5
+                    )
+                    
+    def _extract_event_memories(self, turn: ConversationTurn) -> None:
+        """Extract event and experience memories"""
+        event_indicators = [
+            'happened', 'occurred', 'experienced', 'went through', 'remember when',
+            'last time', 'yesterday', 'today', 'this morning', 'earlier'
+        ]
+        
+        for indicator in event_indicators:
+            if indicator in turn.user_input.lower() or indicator in turn.character_response.lower():
+                # Extract the context around the event
+                sentences = re.split(r'[.!?]+', turn.character_response)
+                for sentence in sentences:
+                    if indicator in sentence.lower() and len(sentence.strip()) > 10:
+                        self._store_memory(
+                            content=f"Event: {sentence.strip()}",
+                            category=MemoryCategories.EVENT,
+                            importance=0.6,
+                            context=turn.character_response,
+                            tags=['event', 'experience'],
+                            emotional_weight=self._calculate_emotional_weight(turn.emotional_tone),
+                            plot_relevance=0.8
+                        )
+                        
+    def _extract_relationship_memories(self, turn: ConversationTurn) -> None:
+        """Extract relationship development memories"""
+        relationship_patterns = [
+            r"(our relationship|we are|we're|between us|i feel about you|you make me feel) ([^.!?]+)",
+            r"(i trust you|i care about you|you mean|you're important|our bond) ([^.!?]*)",
+            r"(we should|we could|together we|let's|maybe we can) ([^.!?]+)"
+        ]
+        
+        for pattern in relationship_patterns:
+            matches = re.finditer(pattern, turn.character_response.lower())
+            for match in matches:
+                relationship_note = match.group(0).strip()
+                if len(relationship_note) > 10:
+                    self._store_memory(
+                        content=f"Relationship: {relationship_note}",
+                        category=MemoryCategories.RELATIONSHIP,
+                        importance=0.9,
+                        context=turn.character_response,
+                        tags=['relationship', 'bond'],
+                        emotional_weight=self._calculate_emotional_weight(turn.emotional_tone),
+                        plot_relevance=0.9
+                    )
+                    
+    def _extract_physical_memories(self, turn: ConversationTurn) -> None:
+        """Extract physical changes and body-related memories"""
+        physical_patterns = [
+            r"(gained|lost|weigh|weight|size|clothes|clothing|fit|tight|loose) ([^.!?]*)",
+            r"(my body|appearance|look|physical|measurements) ([^.!?]*)",
+            r"(eating|food|hungry|full|stuffed|calories) ([^.!?]*)"
+        ]
+        
+        for pattern in physical_patterns:
+            matches = re.finditer(pattern, turn.character_response.lower())
+            for match in matches:
+                physical_note = match.group(0).strip()
+                if len(physical_note) > 5:
+                    self._store_memory(
+                        content=f"Physical: {physical_note}",
+                        category=MemoryCategories.PHYSICAL,
+                        importance=0.7,
+                        context=turn.character_response,
+                        tags=['physical', 'body'],
+                        emotional_weight=self._calculate_emotional_weight(turn.emotional_tone),
+                        plot_relevance=0.7
+                    )
+                    
+    def _extract_emotional_memories(self, turn: ConversationTurn) -> None:
+        """Extract emotional states and feelings"""
+        emotional_patterns = [
+            r"(i feel|i'm feeling|makes me feel|i get|i become) ([^.!?]+)",
+            r"(emotionally|my emotions|my feelings|my mood) ([^.!?]*)",
+            r"(when i'm|if i'm|makes me|i tend to get) ([^.!?]+)"
+        ]
+        
+        for pattern in emotional_patterns:
+            matches = re.finditer(pattern, turn.character_response.lower())
+            for match in matches:
+                emotional_note = match.group(0).strip()
+                if len(emotional_note) > 8:
+                    self._store_memory(
+                        content=f"Emotional: {emotional_note}",
+                        category=MemoryCategories.EMOTIONAL,
+                        importance=0.6,
+                        context=turn.character_response,
+                        tags=['emotional', 'feelings'],
+                        emotional_weight=self._calculate_emotional_weight(turn.emotional_tone),
+                        plot_relevance=0.5
+                    )
+                    
+    def _extract_goal_memories(self, turn: ConversationTurn) -> None:
+        """Extract goals and aspirations"""
+        goal_patterns = [
+            r"(i want to|i hope to|i plan to|my goal|i dream of|i wish i could) ([^.!?]+)",
+            r"(someday|in the future|eventually|i'd like to) ([^.!?]+)",
+            r"(my ambition|i aspire|i aim to|i'm working toward) ([^.!?]+)"
+        ]
+        
+        for pattern in goal_patterns:
+            matches = re.finditer(pattern, turn.character_response.lower())
+            for match in matches:
+                goal_note = match.group(0).strip()
+                if len(goal_note) > 10:
+                    self._store_memory(
+                        content=f"Goal: {goal_note}",
+                        category=MemoryCategories.GOAL,
+                        importance=0.8,
+                        context=turn.character_response,
+                        tags=['goal', 'aspiration'],
+                        emotional_weight=self._calculate_emotional_weight(turn.emotional_tone),
+                        plot_relevance=0.8
+                    )
+                    
+    def _store_memory(self, content: str, category: str, importance: float,
+                     context: str, tags: List[str], emotional_weight: float = 0.0,
+                     plot_relevance: float = 0.0) -> str:
+        """Store a memory entry with deduplication"""
+        # Create content hash for deduplication
+        content_hash = hashlib.md5(content.lower().encode()).hexdigest()[:12]
+        
+        # Check for similar existing memories
+        similar_memory = self._find_similar_memory(content, category)
+        if similar_memory:
+            # Update existing memory instead of creating duplicate
+            similar_memory.importance = max(similar_memory.importance, importance)
+            similar_memory.frequency_accessed += 1
+            similar_memory.emotional_weight = max(similar_memory.emotional_weight, emotional_weight)
+            similar_memory.plot_relevance = max(similar_memory.plot_relevance, plot_relevance)
+            return similar_memory.id
+            
+        # Create new memory
+        memory_id = f"{category}_{content_hash}_{int(time.time())}"
+        memory = MemoryEntry(
+            id=memory_id,
+            content=content,
+            category=category,
+            importance=importance,
+            timestamp=time.time(),
+            context=context,
+            tags=tags,
+            emotional_weight=emotional_weight,
+            plot_relevance=plot_relevance
+        )
+        
+        self.memories[memory_id] = memory
+        
+        # Update indexes
+        self.category_index[category].append(memory_id)
+        for tag in tags:
+            self.tag_index[tag].append(memory_id)
+            
+        return memory_id
+        
+    def _find_similar_memory(self, content: str, category: str) -> Optional[MemoryEntry]:
+        """Find similar existing memory to avoid duplication"""
+        content_words = set(content.lower().split())
+        
+        for memory_id in self.category_index.get(category, []):
+            memory = self.memories.get(memory_id)
+            if memory:
+                memory_words = set(memory.content.lower().split())
+                # Calculate word overlap
+                overlap = len(content_words.intersection(memory_words))
+                total_words = len(content_words.union(memory_words))
+                
+                if total_words > 0 and overlap / total_words > 0.7:  # 70% similarity threshold
+                    return memory
+                    
+        return None
+        
+    def _calculate_emotional_weight(self, emotional_tone: str) -> float:
+        """Calculate emotional weight based on tone"""
+        weights = {
+            'love': 0.9, 'joy': 0.8, 'excitement': 0.7, 'happiness': 0.7,
+            'anger': 0.8, 'sadness': 0.7, 'fear': 0.6, 'anxiety': 0.5,
+            'neutral': 0.3, 'calm': 0.4, 'content': 0.5
+        }
+        return weights.get(emotional_tone.lower(), 0.3)
+        
+    def _update_patterns(self, turn: ConversationTurn) -> None:
+        """Update personality and behavioral patterns"""
+        # Update emotional patterns
+        self.emotional_patterns[turn.emotional_tone].append(time.time())
+        
+        # Update topic preferences
+        for topic in turn.topics:
+            self.preference_patterns[topic] += 1
+            
+    def retrieve_relevant_memories(self, query: str, context: str = "", 
+                                 max_memories: int = 5) -> List[MemoryEntry]:
+        """Retrieve most relevant memories for given query"""
+        query_words = set(query.lower().split())
+        context_words = set(context.lower().split()) if context else set()
+        all_query_words = query_words.union(context_words)
+        
+        # Score all memories
+        memory_scores = []
+        
+        for memory in self.memories.values():
+            score = self._calculate_relevance_score(memory, all_query_words, query)
+            if score > 0.1:  # Minimum relevance threshold
+                memory_scores.append((memory, score))
+                
+        # Sort by score and return top memories
+        memory_scores.sort(key=lambda x: x[1], reverse=True)
+        
+        # Update access statistics for retrieved memories
+        retrieved_memories = []
+        for memory, score in memory_scores[:max_memories]:
+            memory.update_access()
+            retrieved_memories.append(memory)
+            
+        return retrieved_memories
+        
+    def _calculate_relevance_score(self, memory: MemoryEntry, query_words: set, 
+                                 original_query: str) -> float:
+        """Calculate relevance score for a memory"""
+        memory_words = set(memory.content.lower().split())
+        
+        # Word overlap score
+        overlap = len(query_words.intersection(memory_words))
+        word_score = overlap / max(len(query_words), 1) if query_words else 0
+        
+        # Category relevance
+        category_score = 0.0
+        for category, keywords in self.category_keywords.items():
+            if memory.category == category and any(kw in original_query.lower() for kw in keywords):
+                category_score = 0.3
+                break
+                
+        # Recency score (more recent memories are slightly more relevant)
+        time_diff = time.time() - memory.timestamp
+        recency_score = max(0, 0.2 - (time_diff / (7 * 24 * 3600)))  # Decay over a week
+        
+        # Frequency and importance boost
+        frequency_score = min(0.2, memory.frequency_accessed * 0.05)
+        importance_score = memory.importance * 0.3
+        
+        # Emotional and plot relevance
+        emotional_score = memory.emotional_weight * 0.1
+        plot_score = memory.plot_relevance * 0.2
+        
+        total_score = (word_score * 0.4 + category_score + recency_score + 
+                      frequency_score + importance_score + emotional_score + plot_score)
+        
+        return min(1.0, total_score)
+        
+    def _refine_memories(self) -> None:
+        """Periodically refine memories by removing redundant or low-value entries"""
+        if len(self.memories) < self.max_memories * 0.8:
+            return  # Only refine when approaching memory limit
+            
+        print(f"🧠 Refining memory system... (Current: {len(self.memories)} memories)")
+        
+        # Identify memories to remove
+        memories_to_remove = []
+        
+        # Group memories by category for analysis
+        category_memories = defaultdict(list)
+        for memory in self.memories.values():
+            category_memories[memory.category].append(memory)
+            
+        for category, memories in category_memories.items():
+            # Sort by importance and recency
+            memories.sort(key=lambda m: (m.importance, m.timestamp, m.frequency_accessed), reverse=True)
+            
+            # Remove bottom 20% of low-importance, rarely accessed memories
+            cutoff = max(1, len(memories) // 5)
+            for memory in memories[-cutoff:]:
+                if memory.importance < 0.4 and memory.frequency_accessed < 2:
+                    memories_to_remove.append(memory.id)
+                    
+        # Remove duplicate and similar memories
+        self._remove_duplicate_memories(memories_to_remove)
+        
+        # Clean up indexes
+        self._rebuild_indexes()
+        
+        print(f"🧠 Memory refinement complete. Removed {len(memories_to_remove)} memories. Current: {len(self.memories)}")
+        
+    def _remove_duplicate_memories(self, already_marked: List[str]) -> None:
+        """Remove duplicate or very similar memories"""
+        memories_list = list(self.memories.values())
+        
+        for i, memory1 in enumerate(memories_list):
+            if memory1.id in already_marked:
+                continue
+                
+            for memory2 in memories_list[i+1:]:
+                if memory2.id in already_marked:
+                    continue
+                    
+                # Check similarity
+                if self._are_memories_duplicate(memory1, memory2):
+                    # Keep the more important/recent one
+                    if memory1.importance >= memory2.importance:
+                        already_marked.append(memory2.id)
+                    else:
+                        already_marked.append(memory1.id)
+                        break
+                        
+        # Remove marked memories
+        for memory_id in already_marked:
+            if memory_id in self.memories:
+                del self.memories[memory_id]
+                
+    def _are_memories_duplicate(self, memory1: MemoryEntry, memory2: MemoryEntry) -> bool:
+        """Check if two memories are duplicates"""
+        if memory1.category != memory2.category:
+            return False
+            
+        words1 = set(memory1.content.lower().split())
+        words2 = set(memory2.content.lower().split())
+        
+        overlap = len(words1.intersection(words2))
+        total_unique = len(words1.union(words2))
+        
+        return total_unique > 0 and overlap / total_unique > 0.8
+        
+    def _rebuild_indexes(self) -> None:
+        """Rebuild memory indexes after cleanup"""
+        self.category_index.clear()
+        self.tag_index.clear()
+        
+        for memory in self.memories.values():
+            self.category_index[memory.category].append(memory.id)
+            for tag in memory.tags:
+                self.tag_index[tag].append(memory.id)
+                
+    def get_character_summary(self) -> Dict[str, Any]:
+        """Generate a comprehensive character summary from memories"""
+        summary = {
+            'personality_traits': [],
+            'preferences': {'likes': [], 'dislikes': []},
+            'goals': [],
+            'emotional_patterns': {},
+            'relationship_status': [],
+            'physical_changes': [],
+            'key_events': []
+        }
+        
+        # Aggregate memories by category
+        for memory in self.memories.values():
+            if memory.importance > 0.5:  # Only include important memories
+                if memory.category == MemoryCategories.PERSONALITY:
+                    summary['personality_traits'].append(memory.content)
+                elif memory.category == MemoryCategories.PREFERENCE:
+                    if 'positive' in memory.tags:
+                        summary['preferences']['likes'].append(memory.content)
+                    else:
+                        summary['preferences']['dislikes'].append(memory.content)
+                elif memory.category == MemoryCategories.GOAL:
+                    summary['goals'].append(memory.content)
+                elif memory.category == MemoryCategories.RELATIONSHIP:
+                    summary['relationship_status'].append(memory.content)
+                elif memory.category == MemoryCategories.PHYSICAL:
+                    summary['physical_changes'].append(memory.content)
+                elif memory.category == MemoryCategories.EVENT:
+                    summary['key_events'].append(memory.content)
+                    
+        # Emotional patterns
+        for emotion, timestamps in self.emotional_patterns.items():
+            recent_count = sum(1 for ts in timestamps if time.time() - ts < 24*3600)  # Last 24h
+            summary['emotional_patterns'][emotion] = recent_count
+            
+        return summary
+        
+    def export_memories(self, filename: str = "memory_export.json") -> None:
+        """Export memories to JSON file"""
+        export_data = {
+            'memories': {mid: asdict(memory) for mid, memory in self.memories.items()},
+            'conversation_history': [asdict(turn) for turn in self.conversation_history[-50:]],  # Last 50 turns
+            'patterns': {
+                'emotional_patterns': dict(self.emotional_patterns),
+                'preference_patterns': dict(self.preference_patterns)
+            },
+            'export_timestamp': time.time()
+        }
+        
+        with open(filename, 'w') as f:
+            json.dump(export_data, f, indent=2)
+            
+    def import_memories(self, filename: str = "memory_export.json") -> bool:
+        """Import memories from JSON file"""
+        try:
+            with open(filename, 'r') as f:
+                data = json.load(f)
+                
+            # Import memories
+            for mid, memory_data in data['memories'].items():
+                memory = MemoryEntry(**memory_data)
+                self.memories[mid] = memory
+                
+            # Import conversation history
+            self.conversation_history = [ConversationTurn(**turn_data) for turn_data in data['conversation_history']]
+            
+            # Import patterns
+            patterns = data.get('patterns', {})
+            self.emotional_patterns = defaultdict(list, patterns.get('emotional_patterns', {}))
+            self.preference_patterns = Counter(patterns.get('preference_patterns', {}))
+            
+            # Rebuild indexes
+            self._rebuild_indexes()
+            
+            return True
+            
+        except Exception as e:
+            print(f"Error importing memories: {e}")
+            return False
+            
+    def get_memory_stats(self) -> Dict[str, Any]:
+        """Get comprehensive memory system statistics"""
+        stats = {
+            'total_memories': len(self.memories),
+            'memories_by_category': {},
+            'average_importance': 0.0,
+            'most_accessed_memories': [],
+            'recent_memories': 0,
+            'conversation_turns': len(self.conversation_history)
+        }
+        
+        # Category breakdown
+        for category in MemoryCategories.__dict__.values():
+            if isinstance(category, str) and not category.startswith('_'):
+                count = len(self.category_index.get(category, []))
+                stats['memories_by_category'][category] = count
+                
+        # Average importance
+        if self.memories:
+            stats['average_importance'] = sum(m.importance for m in self.memories.values()) / len(self.memories)
+            
+        # Most accessed memories
+        most_accessed = sorted(self.memories.values(), key=lambda m: m.frequency_accessed, reverse=True)[:5]
+        stats['most_accessed_memories'] = [m.content for m in most_accessed]
+        
+        # Recent memories (last 24 hours)
+        recent_threshold = time.time() - 24*3600
+        stats['recent_memories'] = sum(1 for m in self.memories.values() if m.timestamp > recent_threshold)
+        
+        return stats
