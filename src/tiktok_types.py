"""
TikTok Data Types
----------------
Data structures for TikTok content and analysis.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum

class TikTokContentType(Enum):
    """Types of TikTok content formats"""
    TUTORIAL = "tutorial"
    STORYTELLING = "storytelling"
    TRENDING_SOUND = "trending_sound"
    TRANSITION = "transition"
    POV = "pov"
    DUET = "duet"

@dataclass
class TikTokTrend:
    """Structure for TikTok trend data"""
    hashtag: str
    description: str
    video_count: int
    sound_id: Optional[str] = None
    sound_name: Optional[str] = None
    trend_type: TikTokContentType = TikTokContentType.STORYTELLING

@dataclass
class TikTokSound:
    sound_id: str
    name: str
    author: str
    video_count: int
    duration: int

@dataclass
class TikTokHashtag:
    name: str
    video_count: int
    view_count: int
    description: Optional[str]

@dataclass
class TikTokTrendingVideo:
    video_id: str
    description: str
    author: str
    sound: TikTokSound
    hashtags: List[str]
    likes: int
    shares: int
    comments: int
    created_at: datetime 