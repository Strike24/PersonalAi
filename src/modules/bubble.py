"""
Bubble module for managing ephemeral working memory through function calls.

This module provides function-based access to the bubble system, allowing
AI assistants to create, update, retrieve, delete, and list temporary bubbles.
"""

from utils.bubble_manager import (
    create_bubble as _create_bubble,
    update_bubble as _update_bubble,
    get_bubble as _get_bubble,
    delete_bubble as _delete_bubble,
    list_bubbles as _list_bubbles,
    get_bubble_context as _get_bubble_context
)


def execute(args):
    """
    Execute bubble operations.
    
    Supported actions:
    - create: Create a new bubble
    - update: Update an existing bubble
    - get: Retrieve a bubble by key
    - delete: Delete a bubble by key
    - list: List all bubbles
    - context: Get formatted context of auto-include bubbles
    """
    if args is None or len(args) == 0:
        return "No arguments provided for bubble operation."
    
    action = args.get("action", "").lower()
    
    if action == "create":
        key = args.get("key")
        value = args.get("value")
        lifespan = args.get("lifespan")
        on_demand = args.get("on_demand", False)
        
        if not key:
            return "Error: 'key' is required for creating a bubble."
        if not value:
            return "Error: 'value' is required for creating a bubble."
        
        # Parse lifespan if provided as string
        if isinstance(lifespan, str):
            lifespan = _parse_lifespan_string(lifespan)
        
        success = _create_bubble(key, value, lifespan, on_demand)
        if success:
            lifespan_str = _format_lifespan(lifespan) if lifespan else "no expiration"
            demand_str = "on-demand" if on_demand else "auto-include"
            return f"Bubble '{key}' created successfully. Lifespan: {lifespan_str}, Mode: {demand_str}."
        else:
            return f"Error: Bubble with key '{key}' already exists."
    
    elif action == "update":
        key = args.get("key")
        value = args.get("value")
        lifespan = args.get("lifespan")
        on_demand = args.get("on_demand")
        
        if not key:
            return "Error: 'key' is required for updating a bubble."
        
        # Parse lifespan if provided as string
        if isinstance(lifespan, str):
            lifespan = _parse_lifespan_string(lifespan)
        
        success = _update_bubble(key, value, lifespan, on_demand)
        if success:
            return f"Bubble '{key}' updated successfully."
        else:
            return f"Error: Bubble with key '{key}' not found."
    
    elif action == "get":
        key = args.get("key")
        if not key:
            return "Error: 'key' is required for retrieving a bubble."
        
        bubble = _get_bubble(key)
        if bubble:
            lifespan_str = _format_lifespan(bubble.lifespan) if bubble.lifespan else "no expiration"
            demand_str = "on-demand" if bubble.on_demand else "auto-include"
            return f"Bubble '{key}': {bubble.value}\nLifespan: {lifespan_str}, Mode: {demand_str}"
        else:
            return f"Bubble with key '{key}' not found or has expired."
    
    elif action == "delete":
        key = args.get("key")
        if not key:
            return "Error: 'key' is required for deleting a bubble."
        
        success = _delete_bubble(key)
        if success:
            return f"Bubble '{key}' deleted successfully."
        else:
            return f"Bubble with key '{key}' not found."
    
    elif action == "list":
        include_expired = args.get("include_expired", False)
        bubbles = _list_bubbles(include_expired)
        
        if not bubbles:
            return "No bubbles found."
        
        result = "Current bubbles:\n"
        for bubble_info in bubbles:
            status = " (EXPIRED)" if bubble_info['is_expired'] else ""
            lifespan_str = _format_lifespan(bubble_info['lifespan']) if bubble_info['lifespan'] else "no expiration"
            demand_str = "on-demand" if bubble_info['on_demand'] else "auto-include"
            
            result += f"• {bubble_info['key']}: {bubble_info['value'][:100]}{'...' if len(bubble_info['value']) > 100 else ''}\n"
            result += f"  Created: {bubble_info['created_datetime']}, Lifespan: {lifespan_str}, Mode: {demand_str}{status}\n"
        
        return result.strip()
    
    elif action == "context":
        context = _get_bubble_context()
        if context:
            return context
        else:
            return "No auto-include bubbles found."
    
    else:
        return f"Unknown action '{action}'. Supported actions: create, update, get, delete, list, context."


def _parse_lifespan_string(lifespan_str):
    """Parse a lifespan string like '30 minutes' or '2 hours' into a lifespan dict."""
    if not lifespan_str:
        return None
    
    parts = lifespan_str.lower().strip().split()
    if len(parts) != 2:
        return None
    
    try:
        value = int(parts[0])
        unit = parts[1]
        
        if unit in ['minute', 'minutes']:
            return {'minutes': value}
        elif unit in ['hour', 'hours']:
            return {'hours': value}
        elif unit in ['second', 'seconds']:
            return {'seconds': value}
        elif unit in ['message', 'messages']:
            return {'messages': value}
    except ValueError:
        pass
    
    return None


def _format_lifespan(lifespan):
    """Format a lifespan dict into a readable string."""
    if not lifespan:
        return "no expiration"
    
    parts = []
    if 'minutes' in lifespan:
        parts.append(f"{lifespan['minutes']} minute(s)")
    if 'hours' in lifespan:
        parts.append(f"{lifespan['hours']} hour(s)")
    if 'seconds' in lifespan:
        parts.append(f"{lifespan['seconds']} second(s)")
    if 'messages' in lifespan:
        parts.append(f"{lifespan['messages']} message(s)")
    
    return " or ".join(parts) if parts else "no expiration"
