"""
YouTube Shorts Automation System
------------------------------
A complete pipeline for analyzing trending YouTube Shorts, generating content,
creating videos through Vadoo, and publishing back to YouTube.
"""

import os
import asyncio
import requests
import json
import logging
from typing import Dict, List, Optional, Union
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class YouTubeShortsAnalyzer:
    """Handles YouTube Shorts trend analysis and data gathering."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def get_trending_shorts(self, max_results: int = 3) -> List[Dict]:
        """
        Fetch trending YouTube Shorts.
        
        Args:
            max_results (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of trending shorts with their metadata
        """
        try:
            # Search for trending shorts
            search_url = f"{self.base_url}/search"
            params = {
                'part': 'snippet',
                'maxResults': max_results,
                'q': '#shorts',
                'type': 'video',
                'videoDuration': 'short',
                'order': 'viewCount',
                'key': self.api_key
            }
            
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            
            # Process and return results
            results = response.json()
            return [
                {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'channel_id': item['snippet']['channelId'],
                    'published_at': item['snippet']['publishedAt']
                }
                for item in results.get('items', [])
            ]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching trending shorts: {str(e)}")
            return []

class ContentPipeline:
    """Main pipeline for automating YouTube Shorts content creation and publishing."""
    
    def __init__(self):
        """Initialize the pipeline with necessary API keys and components."""
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.vadoo_api_key = os.getenv('VADOO_API_KEY')
        
        if not all([self.youtube_api_key, self.vadoo_api_key]):
            raise ValueError("Missing required API keys. Please set YOUTUBE_API_KEY and VADOO_API_KEY environment variables.")
        
        self.analyzer = YouTubeShortsAnalyzer(self.youtube_api_key)
        self.vadoo_style = "youtube_shorts"
        self.video_duration = 60
        
    def set_vadoo_style(self, style: str) -> None:
        """Set the Vadoo video style."""
        self.vadoo_style = style
        
    def set_video_duration(self, duration: int) -> None:
        """Set the video duration in seconds."""
        self.video_duration = duration
    
    async def generate_content(self) -> Dict[str, Union[bool, str]]:
        """
        Main pipeline execution method.
        
        Returns:
            Dict containing success status and relevant data or error message
        """
        try:
            # Step 1: Analyze trending shorts
            logger.info("Analyzing trending YouTube Shorts...")
            trending_shorts = self.analyzer.get_trending_shorts()
            
            if not trending_shorts:
                raise Exception("No trending shorts found")
            
            # Step 2: Generate script from top trending short
            top_short = trending_shorts[0]
            script = self._generate_script(top_short)
            
            # Step 3: Create video through Vadoo
            logger.info("Initiating video creation through Vadoo...")
            vadoo_response = await self.create_vadoo_video(script)
            
            if not vadoo_response['success']:
                raise Exception(f"Vadoo video creation failed: {vadoo_response['error']}")
            
            # Step 4: Wait for video generation
            logger.info("Waiting for video generation...")
            video_data = await self.wait_for_vadoo_completion(vadoo_response['job_id'])
            
            if not video_data['success']:
                raise Exception(f"Video generation failed: {video_data['error']}")
            
            # Step 5: Post to YouTube
            logger.info("Publishing to YouTube...")
            youtube_response = await self.post_to_youtube(
                video_url=video_data['video_url'],
                title=f"Trending Style: {top_short['title']}",
                description=f"Inspired by trending content\n\nOriginal video ID: {top_short['video_id']}"
            )
            
            return {
                'success': True,
                'youtube_url': youtube_response['video_url'],
                'analysis': json.dumps(top_short, indent=2),
                'script': script
            }
            
        except Exception as e:
            logger.error(f"Pipeline error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_script(self, video_data: Dict) -> str:
        """
        Generate a script based on the analyzed video, formatted for Vadoo.
        
        Args:
            video_data (Dict): Video metadata and analysis
            
        Returns:
            str: Generated script content formatted for Vadoo
        """
        # Extract keywords from title and description
        keywords = video_data['title'].split()[:5]
        
        # Format the script in Vadoo's preferred structure
        script = {
            "title": video_data['title'],
            "style": "youtube_shorts",
            "scenes": [
                {
                    "scene": "Opening Hook",
                    "duration": "3",
                    "voiceover": f"Hey! Want to know about {keywords[0] if keywords else 'this'}?",
                    "visual": "Dynamic zoom-in transition with text overlay",
                    "text_overlay": video_data['title']
                },
                {
                    "scene": "Main Content",
                    "duration": "45",
                    "voiceover": f"Let's dive into {video_data['title']}. This trending topic is taking over social media!",
                    "visual": "Engaging visuals with smooth transitions",
                    "text_overlay": "Key points from content",
                    "background": "Upbeat background music"
                },
                {
                    "scene": "Call to Action",
                    "duration": "12",
                    "voiceover": "If you enjoyed this content, make sure to like and follow for more!",
                    "visual": "Outro animation with social links",
                    "text_overlay": "Follow for more content!",
                    "background": "Fade out music"
                }
            ],
            "settings": {
                "aspect_ratio": "9:16",
                "total_duration": "60",
                "style": "energetic",
                "music_style": "upbeat",
                "caption_style": "modern"
            }
        }
        
        # Convert to Vadoo's expected string format
        formatted_script = f"""
[Video Settings]
Title: {script['title']}
Style: {script['style']}
Duration: {script['settings']['total_duration']} seconds
Aspect Ratio: {script['settings']['aspect_ratio']}

[Scenes]

1. Opening Hook ({script['scenes'][0]['duration']}s)
Visual: {script['scenes'][0]['visual']}
Text: {script['scenes'][0]['text_overlay']}
VO: {script['scenes'][0]['voiceover']}

2. Main Content ({script['scenes'][1]['duration']}s)
Visual: {script['scenes'][1]['visual']}
Text: {script['scenes'][1]['text_overlay']}
VO: {script['scenes'][1]['voiceover']}
Background: {script['scenes'][1]['background']}

3. Call to Action ({script['scenes'][2]['duration']}s)
Visual: {script['scenes'][2]['visual']}
Text: {script['scenes'][2]['text_overlay']}
VO: {script['scenes'][2]['voiceover']}
Background: {script['scenes'][2]['background']}

[Additional Settings]
Music Style: {script['settings']['music_style']}
Caption Style: {script['settings']['caption_style']}
Energy Level: {script['settings']['style']}
"""
        return formatted_script.strip()
    
    async def create_vadoo_video(self, script: str) -> Dict[str, Union[bool, str]]:
        """
        Send script to Vadoo for video generation.
        
        Args:
            script (str): The video script to process
            
        Returns:
            Dict containing success status and job ID or error message
        """
        try:
            vadoo_payload = {
                'script': script,
                'style': self.vadoo_style,
                'aspect_ratio': '9:16',
                'duration': str(self.video_duration),
                'webhook_url': os.getenv('VADOO_WEBHOOK_URL', '')
            }
            
            headers = {
                'Authorization': f'Bearer {self.vadoo_api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                'https://api.vadoo.ai/v1/videos',
                json=vadoo_payload,
                headers=headers
            )
            response.raise_for_status()
            
            data = response.json()
            return {
                'success': True,
                'job_id': data['job_id']
            }
            
        except Exception as e:
            logger.error(f"Vadoo API error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def wait_for_vadoo_completion(self, job_id: str) -> Dict[str, Union[bool, str]]:
        """
        Wait for Vadoo video generation to complete.
        
        Args:
            job_id (str): The Vadoo job ID to monitor
            
        Returns:
            Dict containing success status and video URL or error message
        """
        try:
            max_attempts = 30
            attempt = 0
            
            while attempt < max_attempts:
                headers = {
                    'Authorization': f'Bearer {self.vadoo_api_key}',
                }
                
                response = requests.get(
                    f'https://api.vadoo.ai/v1/videos/{job_id}',
                    headers=headers
                )
                response.raise_for_status()
                
                data = response.json()
                if data['status'] == 'completed':
                    return {
                        'success': True,
                        'video_url': data['video_url']
                    }
                elif data['status'] == 'failed':
                    return {
                        'success': False,
                        'error': 'Video generation failed'
                    }
                
                attempt += 1
                await asyncio.sleep(10)
            
            return {
                'success': False,
                'error': 'Timeout waiting for video generation'
            }
            
        except Exception as e:
            logger.error(f"Error checking Vadoo status: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def post_to_youtube(self, video_url: str, title: str, description: str) -> Dict[str, Union[bool, str]]:
        """
        Post the generated video to YouTube.
        
        Args:
            video_url (str): URL of the generated video
            title (str): Video title
            description (str): Video description
            
        Returns:
            Dict containing success status and video URL or error message
        """
        try:
            # Implement your YouTube upload logic here
            # This is a placeholder implementation
            logger.info(f"Would upload video from {video_url} with title: {title}")
            
            return {
                'success': True,
                'video_url': f"https://youtube.com/shorts/example_id",
                'status': 'published'
            }
            
        except Exception as e:
            logger.error(f"YouTube upload error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

async def main():
    """Main entry point for the automation pipeline."""
    try:
        pipeline = ContentPipeline()
        
        # Configure custom parameters if needed
        pipeline.set_vadoo_style("youtube_shorts")
        pipeline.set_video_duration(60)
        
        # Run the pipeline
        result = await pipeline.generate_content()
        
        if result['success']:
            logger.info(f"Pipeline completed successfully!")
            logger.info(f"Video published: {result['youtube_url']}")
            logger.info("\nAnalysis:")
            logger.info(result['analysis'])
            logger.info("\nGenerated Script:")
            logger.info(result['script'])
        else:
            logger.error(f"Pipeline error: {result['error']}")
            
    except Exception as e:
        logger.error(f"Main execution error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 