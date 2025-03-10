"""
TikTok API Client and Related Classes
-----------------------------------
Classes for interacting with TikTok's API and web interface.
"""

import os
import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from .tiktok_types import TikTokSound, TikTokHashtag, TikTokTrendingVideo

logger = logging.getLogger(__name__)

class RateLimitHandler:
    """Handles rate limiting for TikTok API requests."""
    
    def __init__(self):
        self.rate_limits = {
            'api': {'calls': 0, 'reset_time': datetime.now()},
            'transcription': {'calls': 0, 'reset_time': datetime.now()},
            'web': {'calls': 0, 'reset_time': datetime.now()}
        }
        self.max_calls = {
            'api': 100,  # per minute
            'transcription': 50,  # per minute
            'web': 30  # per minute
        }
    
    async def handle_rate_limit(self, limit_type: str):
        """
        Check and handle rate limiting for different types of requests.
        
        Args:
            limit_type (str): Type of rate limit to check ('api', 'transcription', 'web')
        """
        if limit_type not in self.rate_limits:
            raise ValueError(f"Unknown rate limit type: {limit_type}")
            
        limit = self.rate_limits[limit_type]
        now = datetime.now()
        
        # Reset counters if minute has passed
        if now - limit['reset_time'] > timedelta(minutes=1):
            limit['calls'] = 0
            limit['reset_time'] = now
            
        # Check if we've hit the limit
        if limit['calls'] >= self.max_calls[limit_type]:
            wait_time = 60 - (now - limit['reset_time']).seconds
            logger.warning(f"Rate limit reached for {limit_type}. Waiting {wait_time} seconds.")
            await asyncio.sleep(wait_time)
            limit['calls'] = 0
            limit['reset_time'] = datetime.now()
            
        limit['calls'] += 1

class TikTokAPIClient:
    """Client for interacting with TikTok's API."""
    
    def __init__(self):
        """Initialize the TikTok API client."""
        self.api_key = os.getenv('TIKTOK_API_KEY', 'test_key')
        self.base_url = "https://api.tiktok.com/v1"
        self._session = None
        self.rate_limiter = RateLimitHandler()
        
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp ClientSession."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
        return self._session

    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def get_trending_videos(self, max_results: int = 20) -> List[TikTokTrendingVideo]:
        """Fetch trending videos from TikTok API."""
        await self.rate_limiter.handle_rate_limit('api')
        
        # For testing purposes, return mock data
        return [
            TikTokTrendingVideo(
                video_id="123",
                description="Test video",
                author="test_user",
                sound=TikTokSound(
                    sound_id="123",
                    name="Test Sound",
                    author="test_user",
                    video_count=1000,
                    duration=30
                ),
                hashtags=["test"],
                likes=1000,
                shares=500,
                comments=100,
                created_at=datetime.now()
            )
        ]
    
    def _parse_video_data(self, data: Dict) -> TikTokTrendingVideo:
        """Parse raw video data into TikTokTrendingVideo object."""
        return TikTokTrendingVideo(
            video_id=data['id'],
            description=data['desc'],
            author=data['author']['uniqueId'],
            sound=TikTokSound(
                sound_id=data['music']['id'],
                name=data['music']['title'],
                author=data['music']['authorName'],
                video_count=data['music'].get('videoCount', 0),
                duration=data['music'].get('duration', 0)
            ),
            hashtags=[tag['name'] for tag in data.get('challenges', [])],
            likes=data['stats']['diggCount'],
            shares=data['stats']['shareCount'],
            comments=data['stats']['commentCount'],
            created_at=datetime.fromtimestamp(data['createTime'])
        )

class TikTokWebScraper:
    """Scrapes TikTok web interface for trend data."""
    
    def __init__(self):
        self.rate_limiter = RateLimitHandler()
    
    async def scrape_discover_page(self) -> List[TikTokHashtag]:
        """Scrape trending hashtags from TikTok's discover page."""
        await self.rate_limiter.handle_rate_limit('web')
        
        # For testing purposes, return mock data
        return [
            TikTokHashtag(
                name="lifehack",
                video_count=500000,
                view_count=5000000,
                description="Life hacks to make your day easier"
            ),
            TikTokHashtag(
                name="tutorial",
                video_count=300000,
                view_count=3000000,
                description="Step-by-step guides and tutorials"
            ),
            TikTokHashtag(
                name="productivity",
                video_count=200000,
                view_count=2000000,
                description="Tips and tricks for better productivity"
            )
        ]

class TikTokSoundAnalyzer:
    """Analyzes TikTok sounds and their trends."""
    
    def __init__(self):
        self.api_client = TikTokAPIClient()
        self.rate_limiter = RateLimitHandler()
    
    async def get_trending_sounds(self, max_results: int = 20) -> List[TikTokSound]:
        """Fetch and analyze trending sounds."""
        await self.rate_limiter.handle_rate_limit('api')
        
        try:
            videos = await self.api_client.get_trending_videos(max_results * 2)
            sounds = {}
            
            for video in videos:
                sound = video.sound
                if sound.sound_id not in sounds:
                    sounds[sound.sound_id] = sound
                    
            return list(sounds.values())[:max_results]
            
        except Exception as e:
            logger.error(f"Error fetching trending sounds: {str(e)}")
            return []

class TikTokHashtagAnalyzer:
    """Analyzes TikTok hashtags and their performance."""
    
    def __init__(self):
        self.api_client = TikTokAPIClient()
        self.web_scraper = TikTokWebScraper()
        self.rate_limiter = RateLimitHandler()
    
    async def get_trending_hashtags(self, max_results: int = 20) -> List[TikTokHashtag]:
        """Fetch and analyze trending hashtags."""
        await self.rate_limiter.handle_rate_limit('api')
        
        try:
            # Combine data from API and web scraping
            api_videos = await self.api_client.get_trending_videos(max_results * 2)
            web_hashtags = await self.web_scraper.scrape_discover_page()
            
            # Extract hashtags from videos
            video_hashtags = {}
            for video in api_videos:
                for tag in video.hashtags:
                    if tag not in video_hashtags:
                        video_hashtags[tag] = {
                            'count': 1,
                            'views': video.likes + video.shares + video.comments
                        }
                    else:
                        video_hashtags[tag]['count'] += 1
                        video_hashtags[tag]['views'] += video.likes + video.shares + video.comments
            
            # Combine with web scraped hashtags
            hashtags = []
            seen = set()
            
            # First add web scraped hashtags
            for tag in web_hashtags:
                if tag.name not in seen:
                    hashtags.append(tag)
                    seen.add(tag.name)
            
            # Then add hashtags from videos that weren't in web results
            for tag, stats in video_hashtags.items():
                if tag not in seen:
                    hashtags.append(TikTokHashtag(
                        name=tag,
                        video_count=stats['count'],
                        view_count=stats['views'],
                        description=None
                    ))
            
            return sorted(hashtags, key=lambda x: x.view_count, reverse=True)[:max_results]
            
        except Exception as e:
            logger.error(f"Error analyzing hashtags: {str(e)}")
            return [] 