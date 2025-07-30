#!/usr/bin/env python3
"""
Unified Memory System for Dating Simulator
Consolidates memory, event, learning, and knowledge storage into a single optimized system
"""

import json
import time
import re
import hashlib
import sqlite3
import threading
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class MemoryType(Enum):
    """Types of data that can be stored in unified memory"""
    CONVERSATION = "conversation"
    EVENT = "event"
    LEARNING = "learning"
    KNOWLEDGE = "knowledge"
    PERSONALITY = "personality"
    RELATIONSHIP = "relationship"
    PREFERENCE = "preference"
    PHYSICAL = "physical"
    EMOTIONAL = "emotional"
    GOAL = "goal"
    PLOT = "plot"
    SYSTEM_STATE = "system_state"

class StorageTier(Enum):
    """Storage tiers for performance optimization"""
    HOT = "hot"          # Frequently accessed, in-memory
    WARM = "warm"        # Occasionally accessed, cached
    COLD = "cold"        # Rarely accessed, disk only

@dataclass
class UnifiedMemoryEntry:
    """Universal memory entry that can store any type of data"""
    id: str
    content: Union[str, Dict, List]  # Flexible content type
    memory_type: MemoryType
    category: str
    importance: float  # 0.0 - 1.0
    timestamp: float
    context: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Access tracking
    frequency_accessed: int = 0
    last_accessed: float = 0.0
    
    # Relevance scoring
    emotional_weight: float = 0.0
    plot_relevance: float = 0.0
    relationship_relevance: float = 0.0
    
    # Storage optimization
    storage_tier: StorageTier = StorageTier.HOT
    compression_level: int = 0
    
    def update_access(self):
        """Update access statistics"""
        self.frequency_accessed += 1
        self.last_accessed = time.time()
        
    def calculate_relevance_score(self, query_context: str = "") -> float:
        """Calculate relevance score for retrieval ranking"""
        base_score = self.importance
        
        # Boost recent memories
        age_hours = (time.time() - self.timestamp) / 3600
        if age_hours < 24:
            base_score += 0.2
        elif age_hours < 168:  # 1 week
            base_score += 0.1
            
        # Boost frequently accessed memories
        if self.frequency_accessed > 5:
            base_score += 0.1
            
        # Boost emotionally significant memories
        base_score += self.emotional_weight * 0.3
        
        # Context matching
        if query_context:
            content_str = str(self.content).lower()
            context_words = query_context.lower().split()
            matches = sum(1 for word in context_words if word in content_str)
            if context_words:
                base_score += (matches / len(context_words)) * 0.2
        
        return min(1.0, base_score)

class UnifiedMemoryIndex:
    """Advanced indexing system for fast retrieval"""
    
    def __init__(self):
        self.type_index: Dict[MemoryType, List[str]] = defaultdict(list)
        self.category_index: Dict[str, List[str]] = defaultdict(list)
        self.tag_index: Dict[str, List[str]] = defaultdict(list)
        self.content_index: Dict[str, List[str]] = defaultdict(list)  # Word-based index
        self.timestamp_index: List[Tuple[float, str]] = []  # For temporal queries
        self.importance_index: List[Tuple[float, str]] = []  # For importance ranking
        self._lock = threading.RLock()
        
    def add_entry(self, memory_id: str, entry: UnifiedMemoryEntry):
        """Add entry to all relevant indexes"""
        with self._lock:
            self.type_index[entry.memory_type].append(memory_id)
            self.category_index[entry.category].append(memory_id)
            
            for tag in entry.tags:
                self.tag_index[tag].append(memory_id)
                
            # Index content words
            content_str = str(entry.content).lower()
            words = re.findall(r'\b\w+\b', content_str)
            for word in set(words):  # Unique words only
                self.content_index[word].append(memory_id)
                
            # Index by timestamp and importance
            self.timestamp_index.append((entry.timestamp, memory_id))
            self.importance_index.append((entry.importance, memory_id))
            
            # Keep indexes sorted
            self.timestamp_index.sort(reverse=True)  # Most recent first
            self.importance_index.sort(reverse=True)  # Most important first
            
    def remove_entry(self, memory_id: str, entry: UnifiedMemoryEntry):
        """Remove entry from all indexes"""
        with self._lock:
            # Remove from type and category indexes
            if memory_id in self.type_index[entry.memory_type]:
                self.type_index[entry.memory_type].remove(memory_id)
            if memory_id in self.category_index[entry.category]:
                self.category_index[entry.category].remove(memory_id)
                
            # Remove from tag indexes
            for tag in entry.tags:
                if memory_id in self.tag_index[tag]:
                    self.tag_index[tag].remove(memory_id)
                    
            # Remove from content index
            content_str = str(entry.content).lower()
            words = re.findall(r'\b\w+\b', content_str)
            for word in set(words):
                if memory_id in self.content_index[word]:
                    self.content_index[word].remove(memory_id)
                    
            # Remove from timestamp and importance indexes
            self.timestamp_index = [(ts, mid) for ts, mid in self.timestamp_index if mid != memory_id]
            self.importance_index = [(imp, mid) for imp, mid in self.importance_index if mid != memory_id]
            
    def search(self, query: str, memory_types: List[MemoryType] = None, 
               categories: List[str] = None, tags: List[str] = None,
               max_results: int = 50) -> List[str]:
        """Search indexes for matching memory IDs"""
        with self._lock:
            candidate_ids = set()
            
            # Content-based search
            if query:
                query_words = re.findall(r'\b\w+\b', query.lower())
                for word in query_words:
                    if word in self.content_index:
                        candidate_ids.update(self.content_index[word])
                        
            # Filter by memory types
            if memory_types:
                type_ids = set()
                for mem_type in memory_types:
                    type_ids.update(self.type_index[mem_type])
                if candidate_ids:
                    candidate_ids &= type_ids
                else:
                    candidate_ids = type_ids
                    
            # Filter by categories
            if categories:
                category_ids = set()
                for category in categories:
                    category_ids.update(self.category_index[category])
                if candidate_ids:
                    candidate_ids &= category_ids
                else:
                    candidate_ids = category_ids
                    
            # Filter by tags
            if tags:
                tag_ids = set()
                for tag in tags:
                    tag_ids.update(self.tag_index[tag])
                if candidate_ids:
                    candidate_ids &= tag_ids
                else:
                    candidate_ids = tag_ids
                    
            # If no filters provided, return recent memories
            if not query and not memory_types and not categories and not tags:
                candidate_ids = {mid for _, mid in self.timestamp_index[:max_results]}
                
            return list(candidate_ids)[:max_results]

class UnifiedMemorySystem:
    """Unified memory system that handles all types of data storage"""
    
    def __init__(self, 
                 db_path: str = "unified_memory.db",
                 max_hot_memories: int = 1000,
                 max_warm_memories: int = 5000,
                 cleanup_interval: int = 100):
        
        self.db_path = db_path
        self.max_hot_memories = max_hot_memories
        self.max_warm_memories = max_warm_memories
        self.cleanup_interval = cleanup_interval
        self.operation_count = 0
        
        # In-memory storage for hot data
        self.hot_memories: Dict[str, UnifiedMemoryEntry] = {}
        self.warm_memories: Dict[str, UnifiedMemoryEntry] = {}
        
        # Indexing system
        self.index = UnifiedMemoryIndex()
        
        # Performance tracking
        self.performance_metrics = {
            'retrieval_times': [],
            'storage_times': [],
            'cache_hits': 0,
            'cache_misses': 0
        }
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Initialize database
        self._init_database()
        
        # Load hot memories from database
        self._load_hot_memories()
        
    def _init_database(self):
        """Initialize SQLite database for persistent storage"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS memories (
                        id TEXT PRIMARY KEY,
                        content TEXT NOT NULL,
                        memory_type TEXT NOT NULL,
                        category TEXT NOT NULL,
                        importance REAL NOT NULL,
                        timestamp REAL NOT NULL,
                        context TEXT,
                        tags TEXT,
                        metadata TEXT,
                        frequency_accessed INTEGER DEFAULT 0,
                        last_accessed REAL DEFAULT 0.0,
                        emotional_weight REAL DEFAULT 0.0,
                        plot_relevance REAL DEFAULT 0.0,
                        relationship_relevance REAL DEFAULT 0.0,
                        storage_tier TEXT DEFAULT 'hot',
                        compression_level INTEGER DEFAULT 0
                    )
                ''')
                
                # Create indexes for performance
                conn.execute('CREATE INDEX IF NOT EXISTS idx_memory_type ON memories(memory_type)')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_category ON memories(category)')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)')
                conn.execute('CREATE INDEX IF NOT EXISTS idx_last_accessed ON memories(last_accessed)')
                
                conn.commit()
                logger.info("Unified memory database initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize memory database: {e}")
            raise
            
    def _load_hot_memories(self):
        """Load hot-tier memories into memory on startup"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT * FROM memories 
                    WHERE storage_tier = 'hot' 
                    ORDER BY importance DESC, last_accessed DESC
                    LIMIT ?
                ''', (self.max_hot_memories,))
                
                for row in cursor:
                    memory = self._row_to_memory(row)
                    self.hot_memories[memory.id] = memory
                    self.index.add_entry(memory.id, memory)
                    
                logger.info(f"Loaded {len(self.hot_memories)} hot memories into cache")
                
        except Exception as e:
            logger.error(f"Failed to load hot memories: {e}")
            
    def _row_to_memory(self, row) -> UnifiedMemoryEntry:
        """Convert database row to UnifiedMemoryEntry"""
        (id, content, memory_type, category, importance, timestamp, context,
         tags, metadata, frequency_accessed, last_accessed, emotional_weight,
         plot_relevance, relationship_relevance, storage_tier, compression_level) = row
         
        # Parse JSON fields
        try:
            content_data = json.loads(content)
        except:
            content_data = content
            
        tags_list = json.loads(tags) if tags else []
        metadata_dict = json.loads(metadata) if metadata else {}
        
        return UnifiedMemoryEntry(
            id=id,
            content=content_data,
            memory_type=MemoryType(memory_type),
            category=category,
            importance=importance,
            timestamp=timestamp,
            context=context or "",
            tags=tags_list,
            metadata=metadata_dict,
            frequency_accessed=frequency_accessed,
            last_accessed=last_accessed,
            emotional_weight=emotional_weight,
            plot_relevance=plot_relevance,
            relationship_relevance=relationship_relevance,
            storage_tier=StorageTier(storage_tier),
            compression_level=compression_level
        )
        
    def store_memory(self, 
                    content: Union[str, Dict, List],
                    memory_type: MemoryType,
                    category: str,
                    importance: float = 0.5,
                    context: str = "",
                    tags: List[str] = None,
                    metadata: Dict[str, Any] = None) -> str:
        """Store a new memory entry"""
        start_time = time.time()
        
        with self._lock:
            # Generate unique ID
            content_str = json.dumps(content, sort_keys=True) if not isinstance(content, str) else content
            memory_id = hashlib.md5(f"{content_str}_{memory_type.value}_{category}_{time.time()}".encode()).hexdigest()
            
            # Create memory entry
            memory = UnifiedMemoryEntry(
                id=memory_id,
                content=content,
                memory_type=memory_type,
                category=category,
                importance=importance,
                timestamp=time.time(),
                context=context,
                tags=tags or [],
                metadata=metadata or {}
            )
            
            # Check for duplicates
            if not self._check_for_duplicates(memory):
                # Store in appropriate tier
                self._store_in_tier(memory)
                
                # Add to index
                self.index.add_entry(memory_id, memory)
                
                # Persist to database
                self._persist_memory(memory)
                
                # Update performance metrics
                storage_time = time.time() - start_time
                self.performance_metrics['storage_times'].append(storage_time)
                
                # Periodic cleanup
                self.operation_count += 1
                if self.operation_count % self.cleanup_interval == 0:
                    self._perform_cleanup()
                    
                logger.debug(f"Stored memory {memory_id} in {storage_time:.3f}s")
                return memory_id
            else:
                logger.debug(f"Duplicate memory detected, skipping storage")
                return ""
                
    def _check_for_duplicates(self, new_memory: UnifiedMemoryEntry) -> bool:
        """Check for duplicate memories to avoid redundancy"""
        content_str = str(new_memory.content).lower()
        content_words = set(re.findall(r'\b\w+\b', content_str))
        
        # Search for similar memories in the same category
        similar_candidates = self.index.search(
            query="",
            memory_types=[new_memory.memory_type],
            categories=[new_memory.category],
            max_results=20
        )
        
        for candidate_id in similar_candidates:
            existing_memory = self._get_memory_by_id(candidate_id)
            if existing_memory:
                existing_content = str(existing_memory.content).lower()
                existing_words = set(re.findall(r'\b\w+\b', existing_content))
                
                # Calculate similarity
                if content_words and existing_words:
                    overlap = len(content_words.intersection(existing_words))
                    total = len(content_words.union(existing_words))
                    similarity = overlap / total if total > 0 else 0
                    
                    if similarity > 0.8:  # 80% similarity threshold
                        # Update existing memory instead of creating duplicate
                        existing_memory.frequency_accessed += 1
                        existing_memory.last_accessed = time.time()
                        if new_memory.importance > existing_memory.importance:
                            existing_memory.importance = new_memory.importance
                        self._persist_memory(existing_memory)
                        return True
                        
        return False
        
    def _store_in_tier(self, memory: UnifiedMemoryEntry):
        """Store memory in appropriate tier based on importance and access patterns"""
        if memory.importance >= 0.7 or memory.memory_type in [MemoryType.CONVERSATION, MemoryType.RELATIONSHIP]:
            memory.storage_tier = StorageTier.HOT
            self.hot_memories[memory.id] = memory
            
            # Manage hot memory limit
            if len(self.hot_memories) > self.max_hot_memories:
                self._demote_cold_hot_memories()
                
        elif memory.importance >= 0.4:
            memory.storage_tier = StorageTier.WARM
            self.warm_memories[memory.id] = memory
            
            # Manage warm memory limit
            if len(self.warm_memories) > self.max_warm_memories:
                self._demote_cold_warm_memories()
                
        else:
            memory.storage_tier = StorageTier.COLD
            # Cold memories are only stored in database
            
    def _demote_cold_hot_memories(self):
        """Move least important hot memories to warm tier"""
        hot_list = list(self.hot_memories.values())
        hot_list.sort(key=lambda m: (m.last_accessed, m.importance))
        
        # Move bottom 10% to warm tier
        demote_count = max(1, len(hot_list) // 10)
        for memory in hot_list[:demote_count]:
            memory.storage_tier = StorageTier.WARM
            self.warm_memories[memory.id] = memory
            del self.hot_memories[memory.id]
            self._persist_memory(memory)
            
    def _demote_cold_warm_memories(self):
        """Move least important warm memories to cold tier"""
        warm_list = list(self.warm_memories.values())
        warm_list.sort(key=lambda m: (m.last_accessed, m.importance))
        
        # Move bottom 10% to cold tier
        demote_count = max(1, len(warm_list) // 10)
        for memory in warm_list[:demote_count]:
            memory.storage_tier = StorageTier.COLD
            del self.warm_memories[memory.id]
            self._persist_memory(memory)
            
    def _persist_memory(self, memory: UnifiedMemoryEntry):
        """Persist memory to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO memories 
                    (id, content, memory_type, category, importance, timestamp, context,
                     tags, metadata, frequency_accessed, last_accessed, emotional_weight,
                     plot_relevance, relationship_relevance, storage_tier, compression_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    memory.id,
                    json.dumps(memory.content) if not isinstance(memory.content, str) else memory.content,
                    memory.memory_type.value,
                    memory.category,
                    memory.importance,
                    memory.timestamp,
                    memory.context,
                    json.dumps(memory.tags),
                    json.dumps(memory.metadata),
                    memory.frequency_accessed,
                    memory.last_accessed,
                    memory.emotional_weight,
                    memory.plot_relevance,
                    memory.relationship_relevance,
                    memory.storage_tier.value,
                    memory.compression_level
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Failed to persist memory {memory.id}: {e}")
            
    def retrieve_memories(self,
                         query: str = "",
                         memory_types: List[MemoryType] = None,
                         categories: List[str] = None,
                         tags: List[str] = None,
                         max_results: int = 10,
                         min_importance: float = 0.0) -> List[UnifiedMemoryEntry]:
        """Retrieve memories matching the given criteria"""
        start_time = time.time()
        
        with self._lock:
            # Search index for candidate IDs
            candidate_ids = self.index.search(
                query=query,
                memory_types=memory_types,
                categories=categories,
                tags=tags,
                max_results=max_results * 3  # Get more candidates for ranking
            )
            
            # Retrieve and rank memories
            memories = []
            for memory_id in candidate_ids:
                memory = self._get_memory_by_id(memory_id)
                if memory and memory.importance >= min_importance:
                    memory.update_access()
                    memories.append(memory)
                    
            # Rank by relevance
            memories.sort(key=lambda m: m.calculate_relevance_score(query), reverse=True)
            
            # Update performance metrics
            retrieval_time = time.time() - start_time
            self.performance_metrics['retrieval_times'].append(retrieval_time)
            
            logger.debug(f"Retrieved {len(memories[:max_results])} memories in {retrieval_time:.3f}s")
            return memories[:max_results]
            
    def _get_memory_by_id(self, memory_id: str) -> Optional[UnifiedMemoryEntry]:
        """Get memory by ID, checking all tiers"""
        # Check hot tier first
        if memory_id in self.hot_memories:
            self.performance_metrics['cache_hits'] += 1
            return self.hot_memories[memory_id]
            
        # Check warm tier
        if memory_id in self.warm_memories:
            self.performance_metrics['cache_hits'] += 1
            return self.warm_memories[memory_id]
            
        # Check database (cold tier)
        self.performance_metrics['cache_misses'] += 1
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('SELECT * FROM memories WHERE id = ?', (memory_id,))
                row = cursor.fetchone()
                if row:
                    return self._row_to_memory(row)
        except Exception as e:
            logger.error(f"Failed to retrieve memory {memory_id} from database: {e}")
            
        return None
        
    def _perform_cleanup(self):
        """Perform periodic cleanup and optimization"""
        logger.info("Performing memory system cleanup")
        
        try:
            # Remove old, unimportant memories
            cutoff_time = time.time() - (30 * 24 * 3600)  # 30 days
            
            with sqlite3.connect(self.db_path) as conn:
                # Delete memories that are old and unimportant
                conn.execute('''
                    DELETE FROM memories 
                    WHERE timestamp < ? AND importance < 0.3 AND frequency_accessed < 2
                ''', (cutoff_time,))
                
                # Update storage tiers based on access patterns
                conn.execute('''
                    UPDATE memories 
                    SET storage_tier = 'cold' 
                    WHERE last_accessed < ? AND importance < 0.4
                ''', (cutoff_time,))
                
                conn.commit()
                
            # Clean up performance metrics
            if len(self.performance_metrics['retrieval_times']) > 1000:
                self.performance_metrics['retrieval_times'] = self.performance_metrics['retrieval_times'][-500:]
            if len(self.performance_metrics['storage_times']) > 1000:
                self.performance_metrics['storage_times'] = self.performance_metrics['storage_times'][-500:]
                
            logger.info("Memory cleanup completed successfully")
            
        except Exception as e:
            logger.error(f"Memory cleanup failed: {e}")

# Backward compatibility adapters

class ConversationalMemoryAdapter:
    """Adapter to make UnifiedMemorySystem compatible with existing ConversationalMemorySystem interface"""
    
    def __init__(self, unified_system: UnifiedMemorySystem):
        self.unified_system = unified_system
        
    def add_conversation_turn(self, user_input: str, character_response: str, emotional_tone: str = "neutral"):
        """Add conversation turn using unified system"""
        self.unified_system.store_memory(
            content={
                "user_input": user_input,
                "character_response": character_response,
                "emotional_tone": emotional_tone
            },
            memory_type=MemoryType.CONVERSATION,
            category="dialogue",
            importance=0.6,
            context=f"User: {user_input}",
            tags=["conversation", emotional_tone]
        )
        
    def retrieve_relevant_memories(self, query: str, context: str = "", max_memories: int = 5):
        """Retrieve memories using unified system"""
        memories = self.unified_system.retrieve_memories(
            query=query,
            memory_types=[MemoryType.CONVERSATION, MemoryType.PERSONALITY, MemoryType.RELATIONSHIP],
            max_results=max_memories
        )
        return [self._convert_to_legacy_format(m) for m in memories]
        
    def _convert_to_legacy_format(self, memory: UnifiedMemoryEntry):
        """Convert unified memory to legacy format"""
        # Create a simple object that mimics the old MemoryEntry
        class LegacyMemory:
            def __init__(self, content, category, importance, timestamp, context, tags):
                self.content = content
                self.category = category
                self.importance = importance
                self.timestamp = timestamp
                self.context = context
                self.tags = tags
                
        return LegacyMemory(
            content=str(memory.content),
            category=memory.category,
            importance=memory.importance,
            timestamp=memory.timestamp,
            context=memory.context,
            tags=memory.tags
        )
        
    def export_memories(self, filename: str):
        """Export memories in legacy format"""
        memories = self.unified_system.retrieve_memories(
            memory_types=[MemoryType.CONVERSATION],
            max_results=1000
        )
        
        export_data = {
            'memories': {m.id: {
                'content': str(m.content),
                'category': m.category,
                'importance': m.importance,
                'timestamp': m.timestamp,
                'context': m.context,
                'tags': m.tags
            } for m in memories},
            'export_timestamp': time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
            
    def import_memories(self, filename: str) -> bool:
        """Import memories from legacy format"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            for memory_data in data.get('memories', {}).values():
                self.unified_system.store_memory(
                    content=memory_data['content'],
                    memory_type=MemoryType.CONVERSATION,
                    category=memory_data.get('category', 'general'),
                    importance=memory_data.get('importance', 0.5),
                    context=memory_data.get('context', ''),
                    tags=memory_data.get('tags', [])
                )
                
            return True
        except Exception as e:
            logger.error(f"Failed to import memories: {e}")
            return False

class EventManagerAdapter:
    """Adapter to make UnifiedMemorySystem compatible with existing EventManager interface"""
    
    def __init__(self, unified_system: UnifiedMemorySystem):
        self.unified_system = unified_system
        
    def export_events(self, filename: str):
        """Export events using unified system"""
        events = self.unified_system.retrieve_memories(
            memory_types=[MemoryType.EVENT],
            max_results=1000
        )
        
        export_data = {
            'events': [m.content for m in events if isinstance(m.content, dict)],
            'export_timestamp': time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
            
    def import_events(self, filename: str) -> bool:
        """Import events using unified system"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            for event_data in data.get('events', []):
                self.unified_system.store_memory(
                    content=event_data,
                    memory_type=MemoryType.EVENT,
                    category=event_data.get('event_type', 'general'),
                    importance=event_data.get('probability', 0.5),
                    tags=['event', event_data.get('event_type', 'general')]
                )
                
            return True
        except Exception as e:
            logger.error(f"Failed to import events: {e}")
            return False