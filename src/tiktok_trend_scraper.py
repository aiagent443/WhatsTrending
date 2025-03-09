"""
TikTok Trend Scraper
------------------
Comprehensive trend analysis for TikTok content using official API and web scraping.
"""

import os
import json
import logging
import asyncio
import aiohttp
import requests
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TikTokSound:
    """Structure for TikTok sound data"""
    sound_id: str
    name: str
    author: str
    video_count: int
    duration: int

@dataclass
class TikTokHashtag:
    """Structure for TikTok hashtag data"""
    name: str
    video_count: int
    view_count: int
    description: Optional[str] = None

@dataclass
class TikTokTrendingVideo:
    """Structure for trending video data"""
    video_id: str
    description: str
    author: str
    likes: int
    shares: int
    comments: int
    sound: Optional[TikTokSound] = None
    hashtags: List[str] = None

class TikTokTrendScraper:
    """Scrapes and analyzes TikTok trends using multiple methods."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the scraper with optional API key.
        
        Args:
            api_key (str, optional): TikTok API key for official endpoints
        """
        self.api_key = api_key
        self.base_url = "https://www.tiktok.com"
        self.api_base_url = "https://api.tiktok.com/v2"
        self._setup_selenium()
        
    def _setup_selenium(self):
        """Configure Selenium for dynamic content scraping."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        
    async def get_trending_hashtags(self, limit: int = 10) -> List[TikTokHashtag]:
        """
        Get currently trending hashtags.
        
        Args:
            limit (int): Maximum number of hashtags to return
            
        Returns:
            List[TikTokHashtag]: List of trending hashtags with metadata
        """
        try:
            trending_tags = []
            
            # Method 1: Official API (if available)
            if self.api_key:
                api_tags = await self._get_trending_hashtags_api()
                if api_tags:
                    trending_tags.extend(api_tags)
            
            # Method 2: Discover page scraping
            discover_tags = await self._scrape_discover_page()
            trending_tags.extend(discover_tags)
            
            # Method 3: Trending sounds analysis
            sound_related_tags = await self._get_trending_sound_hashtags()
            trending_tags.extend(sound_related_tags)
            
            # Deduplicate and sort by video count
            unique_tags = {tag.name: tag for tag in trending_tags}
            sorted_tags = sorted(
                unique_tags.values(),
                key=lambda x: x.video_count,
                reverse=True
            )
            
            return sorted_tags[:limit]
            
        except Exception as e:
            logger.error(f"Error fetching trending hashtags: {str(e)}")
            return []
    
    async def _get_trending_hashtags_api(self) -> List[TikTokHashtag]:
        """Fetch trending hashtags from official API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_base_url}/trending/hashtag/",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [
                            TikTokHashtag(
                                name=item["title"],
                                video_count=item["video_count"],
                                view_count=item["view_count"],
                                description=item.get("description")
                            )
                            for item in data.get("hashtags", [])
                        ]
            return []
            
        except Exception as e:
            logger.error(f"API hashtag error: {str(e)}")
            return []
    
    async def _scrape_discover_page(self) -> List[TikTokHashtag]:
        """Scrape trending hashtags from TikTok's discover page."""
        try:
            self.driver.get(f"{self.base_url}/discover")
            
            # Wait for hashtag elements to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "challenge-card"))
            )
            
            hashtag_elements = self.driver.find_elements(By.CLASS_NAME, "challenge-card")
            trending_tags = []
            
            for element in hashtag_elements:
                try:
                    name = element.find_element(By.CLASS_NAME, "challenge-title").text
                    views = element.find_element(By.CLASS_NAME, "challenge-views").text
                    view_count = self._parse_count(views)
                    
                    # Get video count from hashtag page
                    video_count = await self._get_hashtag_video_count(name)
                    
                    trending_tags.append(
                        TikTokHashtag(
                            name=name,
                            video_count=video_count,
                            view_count=view_count
                        )
                    )
                except Exception as e:
                    logger.warning(f"Error parsing hashtag element: {str(e)}")
                    continue
            
            return trending_tags
            
        except Exception as e:
            logger.error(f"Discover page scraping error: {str(e)}")
            return []
    
    async def _get_trending_sound_hashtags(self) -> List[TikTokHashtag]:
        """Get hashtags from trending sounds."""
        try:
            trending_sounds = await self.get_trending_sounds(limit=5)
            hashtags = []
            
            for sound in trending_sounds:
                # Get videos using this sound
                videos = await self._get_videos_by_sound(sound.sound_id, limit=10)
                
                # Extract hashtags from video descriptions
                sound_hashtags = {}
                for video in videos:
                    if video.hashtags:
                        for tag in video.hashtags:
                            if tag in sound_hashtags:
                                sound_hashtags[tag] += 1
                            else:
                                sound_hashtags[tag] = 1
                
                # Convert to TikTokHashtag objects
                for tag_name, count in sound_hashtags.items():
                    view_count = await self._get_hashtag_view_count(tag_name)
                    hashtags.append(
                        TikTokHashtag(
                            name=tag_name,
                            video_count=count,
                            view_count=view_count
                        )
                    )
            
            return hashtags
            
        except Exception as e:
            logger.error(f"Sound hashtag analysis error: {str(e)}")
            return []
    
    async def get_trending_sounds(self, limit: int = 10) -> List[TikTokSound]:
        """Get currently trending sounds."""
        try:
            trending_sounds = []
            
            # Method 1: Official API
            if self.api_key:
                api_sounds = await self._get_trending_sounds_api()
                trending_sounds.extend(api_sounds)
            
            # Method 2: Music page scraping
            scraped_sounds = await self._scrape_trending_sounds()
            trending_sounds.extend(scraped_sounds)
            
            # Deduplicate and sort by video count
            unique_sounds = {sound.sound_id: sound for sound in trending_sounds}
            sorted_sounds = sorted(
                unique_sounds.values(),
                key=lambda x: x.video_count,
                reverse=True
            )
            
            return sorted_sounds[:limit]
            
        except Exception as e:
            logger.error(f"Error fetching trending sounds: {str(e)}")
            return []
    
    async def _get_videos_by_sound(
        self,
        sound_id: str,
        limit: int = 10
    ) -> List[TikTokTrendingVideo]:
        """Get videos using a specific sound."""
        try:
            videos = []
            
            # Try API first
            if self.api_key:
                api_videos = await self._get_sound_videos_api(sound_id, limit)
                videos.extend(api_videos)
            
            # Fallback to scraping
            if not videos:
                scraped_videos = await self._scrape_sound_videos(sound_id, limit)
                videos.extend(scraped_videos)
            
            return videos[:limit]
            
        except Exception as e:
            logger.error(f"Error fetching videos by sound: {str(e)}")
            return []
    
    @staticmethod
    def _parse_count(count_str: str) -> int:
        """Convert string count (e.g., '1.5M') to integer."""
        try:
            count_str = count_str.lower().strip()
            multiplier = 1
            
            if 'k' in count_str:
                multiplier = 1000
                count_str = count_str.replace('k', '')
            elif 'm' in count_str:
                multiplier = 1000000
                count_str = count_str.replace('m', '')
            elif 'b' in count_str:
                multiplier = 1000000000
                count_str = count_str.replace('b', '')
            
            return int(float(count_str) * multiplier)
            
        except Exception:
            return 0
    
    async def _get_hashtag_video_count(self, hashtag: str) -> int:
        """Get video count for a specific hashtag."""
        try:
            url = f"{self.base_url}/tag/{hashtag}"
            self.driver.get(url)
            
            video_count_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "video-count"))
            )
            
            return self._parse_count(video_count_element.text)
            
        except Exception as e:
            logger.warning(f"Error getting video count for #{hashtag}: {str(e)}")
            return 0
    
    async def _get_hashtag_view_count(self, hashtag: str) -> int:
        """Get view count for a specific hashtag."""
        try:
            url = f"{self.base_url}/tag/{hashtag}"
            self.driver.get(url)
            
            view_count_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "view-count"))
            )
            
            return self._parse_count(view_count_element.text)
            
        except Exception as e:
            logger.warning(f"Error getting view count for #{hashtag}: {str(e)}")
            return 0
    
    def __del__(self):
        """Clean up Selenium driver."""
        try:
            self.driver.quit()
        except:
            pass

async def main():
    """Example usage of TikTok trend scraper."""
    try:
        api_key = os.getenv('TIKTOK_API_KEY')
        scraper = TikTokTrendScraper(api_key)
        
        # Get trending hashtags
        trending_tags = await scraper.get_trending_hashtags(limit=10)
        
        print("\nTrending Hashtags:")
        for tag in trending_tags:
            print(f"#{tag.name}: {tag.video_count:,} videos, {tag.view_count:,} views")
        
        # Get trending sounds
        trending_sounds = await scraper.get_trending_sounds(limit=5)
        
        print("\nTrending Sounds:")
        for sound in trending_sounds:
            print(f"{sound.name} by {sound.author}: {sound.video_count:,} videos")
            
    except Exception as e:
        logger.error(f"Main execution error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 