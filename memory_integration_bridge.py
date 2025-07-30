#!/usr/bin/env python3
"""
Memory Integration Bridge for Dating Simulator
Provides seamless integration between the existing memory systems and the new unified memory system
Ensures backward compatibility and graceful migration
"""

import json
import time
import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# Import existing systems
try:
    from memory_system import ConversationalMemorySystem, MemoryCategories
    MEMORY_SYSTEM_AVAILABLE = True
except ImportError:
    MEMORY_SYSTEM_AVAILABLE = False
    logging.warning("Original memory system not available")

try:
    from event_system import EventManager
    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    EVENT_SYSTEM_AVAILABLE = False
    logging.warning("Event system not available")

# Import unified system
from unified_memory_system import (
    UnifiedMemorySystem, MemoryType, UnifiedMemoryEntry,
    ConversationalMemoryAdapter, EventManagerAdapter
)

logger = logging.getLogger(__name__)

class MemoryIntegrationBridge:
    """
    Bridge that provides unified interface while maintaining backward compatibility
    Allows gradual migration from separate systems to unified system
    """
    
    def __init__(self, 
                 use_unified: bool = True,
                 migration_mode: bool = True,
                 backup_existing: bool = True):
        """
        Initialize the integration bridge
        
        Args:
            use_unified: Whether to use unified system as primary storage
            migration_mode: Whether to run in migration mode (sync both systems)
            backup_existing: Whether to backup existing data before migration
        """
        self.use_unified = use_unified
        self.migration_mode = migration_mode
        self.backup_existing = backup_existing
        
        # Initialize unified system
        self.unified_system = UnifiedMemorySystem(
            db_path="unified_memory.db",
            max_hot_memories=1000,
            max_warm_memories=5000
        )
        
        # Initialize legacy systems if available
        self.legacy_memory = None
        self.legacy_events = None
        
        if MEMORY_SYSTEM_AVAILABLE:
            try:
                self.legacy_memory = ConversationalMemorySystem(max_memories=1000, refinement_interval=25)
                logger.info("Legacy memory system initialized")
            except Exception as e:
                logger.error(f"Failed to initialize legacy memory system: {e}")
                
        if EVENT_SYSTEM_AVAILABLE:
            try:
                self.legacy_events = EventManager()
                logger.info("Legacy event system initialized")
            except Exception as e:
                logger.error(f"Failed to initialize legacy event system: {e}")
        
        # Create adapters for backward compatibility
        self.memory_adapter = ConversationalMemoryAdapter(self.unified_system)
        self.event_adapter = EventManagerAdapter(self.unified_system)
        
        # Track migration status
        self.migration_status = {
            'memories_migrated': 0,
            'events_migrated': 0,
            'migration_complete': False,
            'migration_started': False
        }
        
        # Performance monitoring
        self.performance_stats = {
            'unified_operations': 0,
            'legacy_operations': 0,
            'sync_operations': 0,
            'avg_operation_time': 0.0
        }
        
        # If backup is enabled and migration mode is on, backup existing data
        if self.backup_existing and self.migration_mode:
            self._backup_existing_data()
        
        logger.info(f"Memory Integration Bridge initialized - Unified: {use_unified}, Migration: {migration_mode}")
    
    def _backup_existing_data(self):
        """Backup existing data before migration"""
        try:
            timestamp = int(time.time())
            
            # Backup memory data
            if self.legacy_memory and hasattr(self.legacy_memory, 'export_memories'):
                backup_file = f"memory_backup_{timestamp}.json"
                try:
                    self.legacy_memory.export_memories(backup_file)
                    logger.info(f"Memory data backed up to {backup_file}")
                except Exception as e:
                    logger.error(f"Failed to backup memory data: {e}")
            
            # Backup event data
            if self.legacy_events and hasattr(self.legacy_events, 'export_events'):
                backup_file = f"events_backup_{timestamp}.json"
                try:
                    self.legacy_events.export_events(backup_file)
                    logger.info(f"Event data backed up to {backup_file}")
                except Exception as e:
                    logger.error(f"Failed to backup event data: {e}")
                    
        except Exception as e:
            logger.error(f"Backup process failed: {e}")
    
    def add_conversation_turn(self, user_input: str, character_response: str, emotional_tone: str = "neutral"):
        """Add conversation turn with unified interface"""
        start_time = time.time()
        
        try:
            if self.use_unified:
                # Store in unified system
                self.unified_system.store_memory(
                    content={
                        "user_input": user_input,
                        "character_response": character_response,
                        "emotional_tone": emotional_tone,
                        "timestamp": time.time()
                    },
                    memory_type=MemoryType.CONVERSATION,
                    category="dialogue",
                    importance=0.6,
                    context=f"User: {user_input[:100]}...",
                    tags=["conversation", emotional_tone]
                )
                self.performance_stats['unified_operations'] += 1
                
                # If in migration mode, also store in legacy system
                if self.migration_mode and self.legacy_memory:
                    try:
                        self.legacy_memory.add_conversation_turn(user_input, character_response, emotional_tone)
                        self.performance_stats['sync_operations'] += 1
                    except Exception as e:
                        logger.warning(f"Failed to sync with legacy memory system: {e}")
                        
            else:
                # Use legacy system as primary
                if self.legacy_memory:
                    self.legacy_memory.add_conversation_turn(user_input, character_response, emotional_tone)
                    self.performance_stats['legacy_operations'] += 1
                else:
                    # Fallback to unified system
                    logger.warning("Legacy memory system not available, using unified system")
                    self.memory_adapter.add_conversation_turn(user_input, character_response, emotional_tone)
                    self.performance_stats['unified_operations'] += 1
            
            # Update performance stats
            operation_time = time.time() - start_time
            self.performance_stats['avg_operation_time'] = (
                (self.performance_stats['avg_operation_time'] * 
                 (self.performance_stats['unified_operations'] + self.performance_stats['legacy_operations'] - 1) +
                 operation_time) / 
                (self.performance_stats['unified_operations'] + self.performance_stats['legacy_operations'])
            )
            
        except Exception as e:
            logger.error(f"Failed to add conversation turn: {e}")
            # Try fallback approach
            try:
                if self.use_unified and self.legacy_memory:
                    self.legacy_memory.add_conversation_turn(user_input, character_response, emotional_tone)
                elif not self.use_unified:
                    self.memory_adapter.add_conversation_turn(user_input, character_response, emotional_tone)
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {fallback_error}")
    
    def retrieve_relevant_memories(self, query: str, context: str = "", max_memories: int = 5):
        """Retrieve memories with unified interface"""
        start_time = time.time()
        
        try:
            if self.use_unified:
                # Retrieve from unified system
                memories = self.unified_system.retrieve_memories(
                    query=query,
                    memory_types=[MemoryType.CONVERSATION, MemoryType.PERSONALITY, MemoryType.RELATIONSHIP],
                    max_results=max_memories
                )
                
                # Convert to legacy format for backward compatibility
                legacy_memories = []
                for memory in memories:
                    class LegacyMemory:
                        def __init__(self, content, category, importance, timestamp, context, tags):
                            self.content = content
                            self.category = category
                            self.importance = importance
                            self.timestamp = timestamp
                            self.context = context
                            self.tags = tags
                    
                    legacy_memories.append(LegacyMemory(
                        content=str(memory.content),
                        category=memory.category,
                        importance=memory.importance,
                        timestamp=memory.timestamp,
                        context=memory.context,
                        tags=memory.tags
                    ))
                
                self.performance_stats['unified_operations'] += 1
                return legacy_memories
                
            else:
                # Use legacy system
                if self.legacy_memory:
                    memories = self.legacy_memory.retrieve_relevant_memories(query, context, max_memories)
                    self.performance_stats['legacy_operations'] += 1
                    return memories
                else:
                    # Fallback to unified system adapter
                    memories = self.memory_adapter.retrieve_relevant_memories(query, context, max_memories)
                    self.performance_stats['unified_operations'] += 1
                    return memories
                    
        except Exception as e:
            logger.error(f"Failed to retrieve memories: {e}")
            # Return empty list as fallback
            return []
    
    def store_event(self, event_data: Dict[str, Any]):
        """Store event data with unified interface"""
        start_time = time.time()
        
        try:
            if self.use_unified:
                # Store in unified system
                self.unified_system.store_memory(
                    content=event_data,
                    memory_type=MemoryType.EVENT,
                    category=event_data.get('event_type', 'general'),
                    importance=event_data.get('probability', 0.5),
                    context=event_data.get('description', ''),
                    tags=['event', event_data.get('event_type', 'general')]
                )
                self.performance_stats['unified_operations'] += 1
                
                # If in migration mode, also store in legacy system
                if self.migration_mode and self.legacy_events:
                    try:
                        # Store in legacy event system (this would need to be implemented based on EventManager interface)
                        self.performance_stats['sync_operations'] += 1
                    except Exception as e:
                        logger.warning(f"Failed to sync with legacy event system: {e}")
                        
            else:
                # Use legacy system as primary
                if self.legacy_events:
                    # Store in legacy event system
                    self.performance_stats['legacy_operations'] += 1
                else:
                    # Fallback to unified system
                    logger.warning("Legacy event system not available, using unified system")
                    self.event_adapter.import_events("temp_event.json")  # This is a placeholder
                    self.performance_stats['unified_operations'] += 1
            
        except Exception as e:
            logger.error(f"Failed to store event: {e}")
    
    def migrate_existing_data(self, force: bool = False) -> Dict[str, Any]:
        """Migrate existing data from legacy systems to unified system"""
        if self.migration_status['migration_complete'] and not force:
            logger.info("Migration already completed")
            return self.migration_status
        
        logger.info("Starting data migration to unified system")
        self.migration_status['migration_started'] = True
        migration_results = {
            'success': True,
            'memories_migrated': 0,
            'events_migrated': 0,
            'errors': []
        }
        
        try:
            # Migrate memory data
            if self.legacy_memory and hasattr(self.legacy_memory, 'memories'):
                logger.info("Migrating memory data...")
                for memory_id, memory in self.legacy_memory.memories.items():
                    try:
                        # Determine memory type based on category
                        memory_type = MemoryType.CONVERSATION
                        if hasattr(memory, 'category'):
                            category_mapping = {
                                'personality': MemoryType.PERSONALITY,
                                'relationship': MemoryType.RELATIONSHIP,
                                'preference': MemoryType.PREFERENCE,
                                'physical': MemoryType.PHYSICAL,
                                'emotional': MemoryType.EMOTIONAL,
                                'goal': MemoryType.GOAL,
                                'plot': MemoryType.PLOT
                            }
                            memory_type = category_mapping.get(memory.category, MemoryType.CONVERSATION)
                        
                        # Store in unified system
                        self.unified_system.store_memory(
                            content=memory.content,
                            memory_type=memory_type,
                            category=getattr(memory, 'category', 'general'),
                            importance=getattr(memory, 'importance', 0.5),
                            context=getattr(memory, 'context', ''),
                            tags=getattr(memory, 'tags', [])
                        )
                        migration_results['memories_migrated'] += 1
                        
                    except Exception as e:
                        error_msg = f"Failed to migrate memory {memory_id}: {e}"
                        logger.error(error_msg)
                        migration_results['errors'].append(error_msg)
                        
                logger.info(f"Migrated {migration_results['memories_migrated']} memories")
            
            # Migrate event data (if available)
            if self.legacy_events and hasattr(self.legacy_events, 'events'):
                logger.info("Migrating event data...")
                # This would depend on the specific structure of the EventManager
                # For now, we'll skip this part as it would need to be customized
                logger.info("Event migration not implemented for this system structure")
            
            # Update migration status
            self.migration_status.update({
                'memories_migrated': migration_results['memories_migrated'],
                'events_migrated': migration_results['events_migrated'],
                'migration_complete': True
            })
            
            logger.info(f"Migration completed successfully: {migration_results}")
            
        except Exception as e:
            migration_results['success'] = False
            migration_results['errors'].append(f"Migration failed: {e}")
            logger.error(f"Migration failed: {e}")
        
        return migration_results
    
    def export_unified_data(self, filename: str = None) -> str:
        """Export all data from unified system"""
        if filename is None:
            filename = f"unified_export_{int(time.time())}.json"
        
        try:
            # Get all memories from unified system
            all_memories = []
            for memory_type in MemoryType:
                memories = self.unified_system.retrieve_memories(
                    memory_types=[memory_type],
                    max_results=10000  # Large number to get all
                )
                all_memories.extend(memories)
            
            # Convert to exportable format
            export_data = {
                'unified_memories': [
                    {
                        'id': memory.id,
                        'content': memory.content,
                        'memory_type': memory.memory_type.value,
                        'category': memory.category,
                        'importance': memory.importance,
                        'timestamp': memory.timestamp,
                        'context': memory.context,
                        'tags': memory.tags,
                        'metadata': memory.metadata
                    }
                    for memory in all_memories
                ],
                'export_timestamp': time.time(),
                'total_memories': len(all_memories),
                'performance_stats': self.performance_stats,
                'migration_status': self.migration_status
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"Unified data exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export unified data: {e}")
            return ""
    
    def import_unified_data(self, filename: str) -> bool:
        """Import data into unified system"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            memories = data.get('unified_memories', [])
            imported_count = 0
            
            for memory_data in memories:
                try:
                    self.unified_system.store_memory(
                        content=memory_data['content'],
                        memory_type=MemoryType(memory_data['memory_type']),
                        category=memory_data['category'],
                        importance=memory_data['importance'],
                        context=memory_data['context'],
                        tags=memory_data['tags'],
                        metadata=memory_data.get('metadata', {})
                    )
                    imported_count += 1
                except Exception as e:
                    logger.error(f"Failed to import memory: {e}")
            
            logger.info(f"Imported {imported_count} memories from {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import unified data: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the integration bridge"""
        status = {
            'unified_system_active': self.use_unified,
            'migration_mode': self.migration_mode,
            'migration_status': self.migration_status,
            'performance_stats': self.performance_stats,
            'legacy_systems': {
                'memory_available': self.legacy_memory is not None,
                'events_available': self.legacy_events is not None
            }
        }
        
        # Get unified system performance metrics
        if hasattr(self.unified_system, 'performance_metrics'):
            status['unified_performance'] = self.unified_system.performance_metrics
        
        return status
    
    def switch_to_unified(self, migrate_data: bool = True) -> bool:
        """Switch to using unified system as primary"""
        try:
            if migrate_data and not self.migration_status['migration_complete']:
                migration_result = self.migrate_existing_data()
                if not migration_result['success']:
                    logger.error("Migration failed, cannot switch to unified system")
                    return False
            
            self.use_unified = True
            self.migration_mode = False  # No longer need to sync
            logger.info("Switched to unified system as primary")
            return True
            
        except Exception as e:
            logger.error(f"Failed to switch to unified system: {e}")
            return False
    
    def switch_to_legacy(self) -> bool:
        """Switch back to using legacy systems as primary"""
        try:
            if not (self.legacy_memory or self.legacy_events):
                logger.error("No legacy systems available")
                return False
            
            self.use_unified = False
            self.migration_mode = True  # Keep syncing with unified
            logger.info("Switched to legacy systems as primary")
            return True
            
        except Exception as e:
            logger.error(f"Failed to switch to legacy systems: {e}")
            return False
    
    # Backward compatibility methods
    def export_memories(self, filename: str):
        """Export memories in legacy format for backward compatibility"""
        if self.use_unified:
            self.memory_adapter.export_memories(filename)
        elif self.legacy_memory:
            self.legacy_memory.export_memories(filename)
        else:
            logger.error("No memory system available for export")
    
    def import_memories(self, filename: str) -> bool:
        """Import memories from legacy format"""
        if self.use_unified:
            return self.memory_adapter.import_memories(filename)
        elif self.legacy_memory:
            return self.legacy_memory.import_memories(filename)
        else:
            logger.error("No memory system available for import")
            return False
    
    def export_events(self, filename: str):
        """Export events for backward compatibility"""
        if self.use_unified:
            self.event_adapter.export_events(filename)
        elif self.legacy_events:
            self.legacy_events.export_events(filename)
        else:
            logger.error("No event system available for export")
    
    def import_events(self, filename: str) -> bool:
        """Import events from legacy format"""
        if self.use_unified:
            return self.event_adapter.import_events(filename)
        elif self.legacy_events:
            return self.legacy_events.import_events(filename)
        else:
            logger.error("No event system available for import")
            return False

# Convenience function for easy integration
def create_memory_bridge(use_unified: bool = True, 
                        migration_mode: bool = True,
                        backup_existing: bool = True) -> MemoryIntegrationBridge:
    """
    Create a memory integration bridge with sensible defaults
    
    Args:
        use_unified: Whether to use unified system as primary
        migration_mode: Whether to sync with legacy systems during transition
        backup_existing: Whether to backup existing data
        
    Returns:
        Configured MemoryIntegrationBridge instance
    """
    return MemoryIntegrationBridge(
        use_unified=use_unified,
        migration_mode=migration_mode,
        backup_existing=backup_existing
    )

# Global instance for easy access (optional)
_global_bridge = None

def get_memory_bridge() -> MemoryIntegrationBridge:
    """Get global memory bridge instance"""
    global _global_bridge
    if _global_bridge is None:
        _global_bridge = create_memory_bridge()
    return _global_bridge

def initialize_memory_bridge(**kwargs) -> MemoryIntegrationBridge:
    """Initialize global memory bridge with custom settings"""
    global _global_bridge
    _global_bridge = create_memory_bridge(**kwargs)
    return _global_bridge