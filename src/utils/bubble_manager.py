"""
Bubble Manager for ephemeral working memory.

This module provides a "temp bubble" system for storing temporary information
that can automatically expire based on time or message count.

Each bubble has:
- key: name/identifier of the bubble
- value: the information stored
- lifespan: optional expiration (time-based or message count-based)
- on_demand: whether it's automatically included in prompts or fetched manually
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any


class Bubble:
    """Represents a single bubble with its properties."""
    
    def __init__(self, key: str, value: str, lifespan: Optional[Dict[str, Any]] = None, on_demand: bool = False):
        self.key = key
        self.value = value
        self.lifespan = lifespan or {}
        self.on_demand = on_demand
        self.created_at = time.time()
        self.message_count_at_creation = 0  # Will be set by BubbleManager
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert bubble to dictionary for JSON serialization."""
        return {
            'key': self.key,
            'value': self.value,
            'lifespan': self.lifespan,
            'on_demand': self.on_demand,
            'created_at': self.created_at,
            'message_count_at_creation': self.message_count_at_creation
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Bubble':
        """Create bubble from dictionary."""
        bubble = cls(
            key=data['key'],
            value=data['value'],
            lifespan=data.get('lifespan', {}),
            on_demand=data.get('on_demand', False)
        )
        bubble.created_at = data.get('created_at', time.time())
        bubble.message_count_at_creation = data.get('message_count_at_creation', 0)
        return bubble
    
    def is_expired(self, current_message_count: int = 0) -> bool:
        """Check if the bubble has expired based on its lifespan."""
        if not self.lifespan:
            return False
        
        # Check time-based expiration
        if 'minutes' in self.lifespan:
            expiry_time = self.created_at + (self.lifespan['minutes'] * 60)
            if time.time() > expiry_time:
                return True
        
        if 'hours' in self.lifespan:
            expiry_time = self.created_at + (self.lifespan['hours'] * 3600)
            if time.time() > expiry_time:
                return True
        
        if 'seconds' in self.lifespan:
            expiry_time = self.created_at + self.lifespan['seconds']
            if time.time() > expiry_time:
                return True
        
        # Check message count-based expiration
        if 'messages' in self.lifespan:
            messages_passed = current_message_count - self.message_count_at_creation
            if messages_passed >= self.lifespan['messages']:
                return True
        
        return False


class BubbleManager:
    """Manages the collection of bubbles."""
    
    def __init__(self, bubbles_file: str = None):
        if bubbles_file is None:
            # Default to bubbles.json in the utils directory
            utils_dir = os.path.dirname(os.path.abspath(__file__))
            bubbles_file = os.path.join(utils_dir, 'bubbles.json')
        
        self.bubbles_file = bubbles_file
        self.bubbles: Dict[str, Bubble] = {}
        self.message_count = 0
        self.load_bubbles()
        self.cleanup_expired_bubbles()
    
    def load_bubbles(self):
        """Load bubbles from the JSON file."""
        if os.path.exists(self.bubbles_file):
            try:
                with open(self.bubbles_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.bubbles = {key: Bubble.from_dict(bubble_data) 
                                  for key, bubble_data in data.get('bubbles', {}).items()}
                    self.message_count = data.get('message_count', 0)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Could not load bubbles from {self.bubbles_file}: {e}")
                self.bubbles = {}
                self.message_count = 0
    
    def save_bubbles(self):
        """Save bubbles to the JSON file."""
        try:
            os.makedirs(os.path.dirname(self.bubbles_file), exist_ok=True)
            data = {
                'bubbles': {key: bubble.to_dict() for key, bubble in self.bubbles.items()},
                'message_count': self.message_count
            }
            with open(self.bubbles_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save bubbles to {self.bubbles_file}: {e}")
    
    def increment_message_count(self):
        """Increment the global message count. Call this for each user message."""
        self.message_count += 1
        self.save_bubbles()
    
    def cleanup_expired_bubbles(self):
        """Remove all expired bubbles."""
        expired_keys = []
        for key, bubble in self.bubbles.items():
            if bubble.is_expired(self.message_count):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.bubbles[key]
            print(f"Bubble '{key}' has expired and was removed.")
        
        if expired_keys:
            self.save_bubbles()
    
    def create_bubble(self, key: str, value: str, lifespan: Optional[Dict[str, Any]] = None, on_demand: bool = False) -> bool:
        """
        Create a new bubble.
        
        Args:
            key: Unique identifier for the bubble
            value: The information to store
            lifespan: Dictionary with expiration settings. Examples:
                     {'minutes': 30} - expires in 30 minutes
                     {'hours': 2} - expires in 2 hours
                     {'messages': 10} - expires after 10 messages
                     {'minutes': 15, 'messages': 5} - expires when either condition is met
            on_demand: If False, bubble is included in prompts automatically. If True, fetched manually.
        
        Returns:
            True if created successfully, False if key already exists
        """
        if key in self.bubbles:
            return False
        
        bubble = Bubble(key, value, lifespan, on_demand)
        bubble.message_count_at_creation = self.message_count
        self.bubbles[key] = bubble
        self.save_bubbles()
        return True
    
    def update_bubble(self, key: str, value: str = None, lifespan: Optional[Dict[str, Any]] = None, on_demand: bool = None) -> bool:
        """
        Update an existing bubble.
        
        Args:
            key: Bubble identifier
            value: New value (if None, keeps current value)
            lifespan: New lifespan (if None, keeps current lifespan)
            on_demand: New on_demand setting (if None, keeps current setting)
        
        Returns:
            True if updated successfully, False if bubble doesn't exist
        """
        if key not in self.bubbles:
            return False
        
        bubble = self.bubbles[key]
        if value is not None:
            bubble.value = value
        if lifespan is not None:
            bubble.lifespan = lifespan
        if on_demand is not None:
            bubble.on_demand = on_demand
        
        self.save_bubbles()
        return True
    
    def get_bubble(self, key: str) -> Optional[Bubble]:
        """Get a bubble by key. Returns None if not found or expired."""
        if key not in self.bubbles:
            return None
        
        bubble = self.bubbles[key]
        if bubble.is_expired(self.message_count):
            del self.bubbles[key]
            self.save_bubbles()
            return None
        
        return bubble
    
    def delete_bubble(self, key: str) -> bool:
        """Delete a bubble by key. Returns True if deleted, False if not found."""
        if key in self.bubbles:
            del self.bubbles[key]
            self.save_bubbles()
            return True
        return False
    
    def list_bubbles(self, include_expired: bool = False) -> List[Dict[str, Any]]:
        """
        List all bubbles with their information.
        
        Args:
            include_expired: If True, includes expired bubbles in the list
        
        Returns:
            List of dictionaries with bubble information
        """
        result = []
        for key, bubble in self.bubbles.items():
            is_expired = bubble.is_expired(self.message_count)
            if not include_expired and is_expired:
                continue
            
            result.append({
                'key': key,
                'value': bubble.value,
                'lifespan': bubble.lifespan,
                'on_demand': bubble.on_demand,
                'created_at': bubble.created_at,
                'created_datetime': datetime.fromtimestamp(bubble.created_at).strftime('%Y-%m-%d %H:%M:%S'),
                'is_expired': is_expired,
                'messages_since_creation': self.message_count - bubble.message_count_at_creation
            })
        
        return result
    
    def get_auto_include_bubbles(self) -> Dict[str, str]:
        """Get all non-expired bubbles that should be automatically included in prompts."""
        self.cleanup_expired_bubbles()
        result = {}
        for key, bubble in self.bubbles.items():
            if not bubble.on_demand and not bubble.is_expired(self.message_count):
                result[key] = bubble.value
        return result
    
    def get_bubble_context(self) -> str:
        """Get formatted context string for auto-include bubbles."""
        auto_bubbles = self.get_auto_include_bubbles()
        if not auto_bubbles:
            return ""
        
        context_parts = []
        for key, value in auto_bubbles.items():
            context_parts.append(f"[{key}]: {value}")
        
        return "Current working memory:\n" + "\n".join(context_parts)


# Global instance for easy access
_bubble_manager = None

def get_bubble_manager() -> BubbleManager:
    """Get the global bubble manager instance."""
    global _bubble_manager
    if _bubble_manager is None:
        _bubble_manager = BubbleManager()
    return _bubble_manager


# Convenience functions for easy access
def create_bubble(key: str, value: str, lifespan: Optional[Dict[str, Any]] = None, on_demand: bool = False) -> bool:
    """Create a new bubble."""
    return get_bubble_manager().create_bubble(key, value, lifespan, on_demand)

def update_bubble(key: str, value: str = None, lifespan: Optional[Dict[str, Any]] = None, on_demand: bool = None) -> bool:
    """Update an existing bubble."""
    return get_bubble_manager().update_bubble(key, value, lifespan, on_demand)

def get_bubble(key: str) -> Optional[Bubble]:
    """Get a bubble by key."""
    return get_bubble_manager().get_bubble(key)

def delete_bubble(key: str) -> bool:
    """Delete a bubble by key."""
    return get_bubble_manager().delete_bubble(key)

def list_bubbles(include_expired: bool = False) -> List[Dict[str, Any]]:
    """List all bubbles."""
    return get_bubble_manager().list_bubbles(include_expired)

def get_bubble_context() -> str:
    """Get formatted context string for auto-include bubbles."""
    return get_bubble_manager().get_bubble_context()

def increment_message_count():
    """Increment the global message count."""
    get_bubble_manager().increment_message_count()
