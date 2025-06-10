"""
Real-time Collaborative Editing Service
Free and open-source collaborative CV editing with WebSocket support
"""

import json
import asyncio
import uuid
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ChangeType(Enum):
    TEXT_EDIT = "text_edit"
    SECTION_ADD = "section_add"
    SECTION_DELETE = "section_delete"
    SECTION_MOVE = "section_move"
    STRUCTURE_CHANGE = "structure_change"
    COMMENT_ADD = "comment_add"
    COMMENT_RESOLVE = "comment_resolve"

class UserRole(Enum):
    OWNER = "owner"
    EDITOR = "editor"
    COMMENTER = "commenter"
    VIEWER = "viewer"

@dataclass
class CollaborationUser:
    user_id: str
    name: str
    email: str
    role: UserRole
    avatar_url: Optional[str] = None
    is_online: bool = False
    last_seen: datetime = None

@dataclass
class CVChange:
    change_id: str
    user_id: str
    change_type: ChangeType
    timestamp: datetime
    path: List[str]  # Path to the changed field (e.g., ["work_experience", "0", "job_title"])
    old_value: Any
    new_value: Any
    metadata: Dict[str, Any] = None

@dataclass
class Comment:
    comment_id: str
    user_id: str
    user_name: str
    content: str
    timestamp: datetime
    path: List[str]  # Path to the field being commented on
    is_resolved: bool = False
    replies: List['Comment'] = None

@dataclass
class CollaborationSession:
    session_id: str
    cv_id: str
    owner_id: str
    participants: Dict[str, CollaborationUser]
    changes: List[CVChange]
    comments: List[Comment]
    current_version: int
    created_at: datetime
    last_modified: datetime
    settings: Dict[str, Any]

class OperationalTransform:
    """
    Operational Transform for conflict resolution in real-time editing
    """
    
    @staticmethod
    def transform_changes(change1: CVChange, change2: CVChange) -> tuple[CVChange, CVChange]:
        """Transform two concurrent changes to maintain consistency"""
        
        # If changes are on different paths, no transformation needed
        if not OperationalTransform._paths_conflict(change1.path, change2.path):
            return change1, change2
        
        # Handle text editing conflicts
        if change1.change_type == ChangeType.TEXT_EDIT and change2.change_type == ChangeType.TEXT_EDIT:
            return OperationalTransform._transform_text_edits(change1, change2)
        
        # Handle structural changes
        if change1.change_type in [ChangeType.SECTION_ADD, ChangeType.SECTION_DELETE]:
            return OperationalTransform._transform_structural_changes(change1, change2)
        
        # Default: prioritize by timestamp
        if change1.timestamp <= change2.timestamp:
            return change1, change2
        else:
            return change2, change1
    
    @staticmethod
    def _paths_conflict(path1: List[str], path2: List[str]) -> bool:
        """Check if two paths conflict (one is ancestor of the other)"""
        min_len = min(len(path1), len(path2))
        return path1[:min_len] == path2[:min_len]
    
    @staticmethod
    def _transform_text_edits(change1: CVChange, change2: CVChange) -> tuple[CVChange, CVChange]:
        """Transform concurrent text edits"""
        # Simplified text transformation - in production, use more sophisticated algorithms
        # like diff-match-patch for character-level transformation
        
        # For now, prioritize the earlier change
        if change1.timestamp <= change2.timestamp:
            return change1, change2
        else:
            return change2, change1
    
    @staticmethod
    def _transform_structural_changes(change1: CVChange, change2: CVChange) -> tuple[CVChange, CVChange]:
        """Transform structural changes like adding/deleting sections"""
        
        # If both are adding sections, adjust indices
        if (change1.change_type == ChangeType.SECTION_ADD and 
            change2.change_type == ChangeType.SECTION_ADD):
            
            # Adjust the index of the second change if it's after the first
            if len(change1.path) > 1 and len(change2.path) > 1:
                try:
                    index1 = int(change1.path[1])
                    index2 = int(change2.path[1])
                    
                    if index2 >= index1:
                        # Adjust the path of change2
                        new_path = change2.path.copy()
                        new_path[1] = str(index2 + 1)
                        change2.path = new_path
                except (ValueError, IndexError):
                    pass
        
        return change1, change2

class CollaborationManager:
    """
    Manages collaborative editing sessions and real-time synchronization
    """
    
    def __init__(self):
        self.active_sessions: Dict[str, CollaborationSession] = {}
        self.user_sessions: Dict[str, Set[str]] = {}  # user_id -> set of session_ids
        self.websocket_connections: Dict[str, List] = {}  # session_id -> list of websocket connections
    
    async def create_session(self, cv_id: str, owner_id: str, owner_name: str, 
                           owner_email: str) -> CollaborationSession:
        """Create a new collaboration session"""
        session_id = str(uuid.uuid4())
        
        owner = CollaborationUser(
            user_id=owner_id,
            name=owner_name,
            email=owner_email,
            role=UserRole.OWNER,
            is_online=True,
            last_seen=datetime.now()
        )
        
        session = CollaborationSession(
            session_id=session_id,
            cv_id=cv_id,
            owner_id=owner_id,
            participants={owner_id: owner},
            changes=[],
            comments=[],
            current_version=1,
            created_at=datetime.now(),
            last_modified=datetime.now(),
            settings={
                "allow_comments": True,
                "allow_suggestions": True,
                "auto_save": True,
                "save_interval": 30  # seconds
            }
        )
        
        self.active_sessions[session_id] = session
        
        if owner_id not in self.user_sessions:
            self.user_sessions[owner_id] = set()
        self.user_sessions[owner_id].add(session_id)
        
        return session
    
    async def join_session(self, session_id: str, user_id: str, user_name: str, 
                          user_email: str, role: UserRole = UserRole.VIEWER) -> bool:
        """Add a user to an existing collaboration session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        
        # Check permissions
        if role in [UserRole.OWNER, UserRole.EDITOR] and user_id != session.owner_id:
            # Only owner can assign editor roles
            role = UserRole.COMMENTER
        
        user = CollaborationUser(
            user_id=user_id,
            name=user_name,
            email=user_email,
            role=role,
            is_online=True,
            last_seen=datetime.now()
        )
        
        session.participants[user_id] = user
        
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = set()
        self.user_sessions[user_id].add(session_id)
        
        # Notify other participants
        await self._broadcast_user_joined(session_id, user)
        
        return True
    
    async def leave_session(self, session_id: str, user_id: str):
        """Remove a user from a collaboration session"""
        if session_id not in self.active_sessions:
            return
        
        session = self.active_sessions[session_id]
        
        if user_id in session.participants:
            session.participants[user_id].is_online = False
            session.participants[user_id].last_seen = datetime.now()
            
            # Notify other participants
            await self._broadcast_user_left(session_id, user_id)
            
            # Remove from user sessions
            if user_id in self.user_sessions:
                self.user_sessions[user_id].discard(session_id)
    
    async def apply_change(self, session_id: str, user_id: str, change: CVChange) -> bool:
        """Apply a change to the CV and broadcast to all participants"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        
        # Check permissions
        user = session.participants.get(user_id)
        if not user or user.role not in [UserRole.OWNER, UserRole.EDITOR]:
            return False
        
        # Apply operational transformation for concurrent changes
        for existing_change in reversed(session.changes[-10:]):  # Check last 10 changes
            if abs((change.timestamp - existing_change.timestamp).total_seconds()) < 5:  # Within 5 seconds
                change, existing_change = OperationalTransform.transform_changes(change, existing_change)
        
        # Add change to session
        session.changes.append(change)
        session.current_version += 1
        session.last_modified = datetime.now()
        
        # Broadcast change to all participants
        await self._broadcast_change(session_id, change)
        
        return True
    
    async def add_comment(self, session_id: str, user_id: str, path: List[str], 
                         content: str) -> Optional[Comment]:
        """Add a comment to a specific field"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        user = session.participants.get(user_id)
        
        if not user or user.role == UserRole.VIEWER:
            return None
        
        comment = Comment(
            comment_id=str(uuid.uuid4()),
            user_id=user_id,
            user_name=user.name,
            content=content,
            timestamp=datetime.now(),
            path=path,
            is_resolved=False,
            replies=[]
        )
        
        session.comments.append(comment)
        
        # Broadcast comment to all participants
        await self._broadcast_comment(session_id, comment)
        
        return comment
    
    async def resolve_comment(self, session_id: str, user_id: str, comment_id: str) -> bool:
        """Resolve a comment"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        user = session.participants.get(user_id)
        
        if not user:
            return False
        
        # Find and resolve comment
        for comment in session.comments:
            if comment.comment_id == comment_id:
                # Only comment author or owner can resolve
                if user_id == comment.user_id or user.role == UserRole.OWNER:
                    comment.is_resolved = True
                    
                    # Broadcast resolution
                    await self._broadcast_comment_resolved(session_id, comment_id)
                    return True
        
        return False
    
    async def get_session_state(self, session_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get complete session state for a user"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        
        if user_id not in session.participants:
            return None
        
        return {
            "session_id": session_id,
            "cv_id": session.cv_id,
            "current_version": session.current_version,
            "participants": {uid: asdict(user) for uid, user in session.participants.items()},
            "recent_changes": [asdict(change) for change in session.changes[-20:]],  # Last 20 changes
            "active_comments": [asdict(comment) for comment in session.comments if not comment.is_resolved],
            "user_role": session.participants[user_id].role.value,
            "settings": session.settings
        }
    
    async def _broadcast_change(self, session_id: str, change: CVChange):
        """Broadcast a change to all session participants"""
        if session_id not in self.websocket_connections:
            return
        
        message = {
            "type": "change",
            "data": asdict(change)
        }
        
        await self._broadcast_message(session_id, message)
    
    async def _broadcast_comment(self, session_id: str, comment: Comment):
        """Broadcast a new comment to all session participants"""
        message = {
            "type": "comment",
            "data": asdict(comment)
        }
        
        await self._broadcast_message(session_id, message)
    
    async def _broadcast_comment_resolved(self, session_id: str, comment_id: str):
        """Broadcast comment resolution to all session participants"""
        message = {
            "type": "comment_resolved",
            "data": {"comment_id": comment_id}
        }
        
        await self._broadcast_message(session_id, message)
    
    async def _broadcast_user_joined(self, session_id: str, user: CollaborationUser):
        """Broadcast user join event"""
        message = {
            "type": "user_joined",
            "data": asdict(user)
        }
        
        await self._broadcast_message(session_id, message)
    
    async def _broadcast_user_left(self, session_id: str, user_id: str):
        """Broadcast user leave event"""
        message = {
            "type": "user_left",
            "data": {"user_id": user_id}
        }
        
        await self._broadcast_message(session_id, message)
    
    async def _broadcast_message(self, session_id: str, message: Dict[str, Any]):
        """Broadcast a message to all WebSocket connections in a session"""
        if session_id not in self.websocket_connections:
            return
        
        message_json = json.dumps(message, default=str)
        
        # Remove dead connections
        active_connections = []
        
        for connection in self.websocket_connections[session_id]:
            try:
                await connection.send_text(message_json)
                active_connections.append(connection)
            except:
                # Connection is dead, remove it
                pass
        
        self.websocket_connections[session_id] = active_connections
    
    def add_websocket_connection(self, session_id: str, websocket):
        """Add a WebSocket connection to a session"""
        if session_id not in self.websocket_connections:
            self.websocket_connections[session_id] = []
        
        self.websocket_connections[session_id].append(websocket)
    
    def remove_websocket_connection(self, session_id: str, websocket):
        """Remove a WebSocket connection from a session"""
        if session_id in self.websocket_connections:
            try:
                self.websocket_connections[session_id].remove(websocket)
            except ValueError:
                pass

class ShareService:
    """
    Service for sharing CVs and managing permissions
    """
    
    def __init__(self, collaboration_manager: CollaborationManager):
        self.collaboration_manager = collaboration_manager
        self.share_links: Dict[str, Dict[str, Any]] = {}  # share_token -> share_info
    
    def create_share_link(self, cv_id: str, owner_id: str, permissions: Dict[str, Any]) -> str:
        """Create a shareable link for a CV"""
        share_token = str(uuid.uuid4())
        
        share_info = {
            "cv_id": cv_id,
            "owner_id": owner_id,
            "permissions": permissions,
            "created_at": datetime.now(),
            "expires_at": permissions.get("expires_at"),
            "access_count": 0,
            "max_access": permissions.get("max_access"),
            "require_login": permissions.get("require_login", False)
        }
        
        self.share_links[share_token] = share_info
        
        return f"/shared/{share_token}"
    
    def validate_share_link(self, share_token: str, user_id: str = None) -> Optional[Dict[str, Any]]:
        """Validate a share link and return access info"""
        if share_token not in self.share_links:
            return None
        
        share_info = self.share_links[share_token]
        
        # Check expiration
        if share_info["expires_at"] and datetime.now() > share_info["expires_at"]:
            return None
        
        # Check access count
        if (share_info["max_access"] and 
            share_info["access_count"] >= share_info["max_access"]):
            return None
        
        # Check login requirement
        if share_info["require_login"] and not user_id:
            return None
        
        # Increment access count
        share_info["access_count"] += 1
        
        return share_info
    
    async def access_shared_cv(self, share_token: str, user_id: str = None, 
                              user_name: str = "Anonymous") -> Optional[str]:
        """Access a shared CV and potentially join collaboration session"""
        share_info = self.validate_share_link(share_token, user_id)
        
        if not share_info:
            return None
        
        cv_id = share_info["cv_id"]
        permissions = share_info["permissions"]
        
        # If collaboration is enabled, create/join session
        if permissions.get("allow_collaboration", False):
            # Find or create collaboration session
            session_id = None
            for sid, session in self.collaboration_manager.active_sessions.items():
                if session.cv_id == cv_id:
                    session_id = sid
                    break
            
            if not session_id:
                # Create new session
                session = await self.collaboration_manager.create_session(
                    cv_id, share_info["owner_id"], "Owner", "owner@example.com"
                )
                session_id = session.session_id
            
            # Join session with appropriate role
            role = UserRole.VIEWER
            if permissions.get("can_edit", False):
                role = UserRole.EDITOR
            elif permissions.get("can_comment", False):
                role = UserRole.COMMENTER
            
            if user_id:
                await self.collaboration_manager.join_session(
                    session_id, user_id, user_name, f"{user_id}@example.com", role
                )
            
            return session_id
        
        return cv_id

# Global service instances
collaboration_manager = CollaborationManager()
share_service = ShareService(collaboration_manager)