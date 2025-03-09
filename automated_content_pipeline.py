import os
from scrapers.youtube_shorts.shorts_scraper import YouTubeShortsAnalyzer, analyze_short, generate_short_script
import json
import asyncio
import requests
from datetime import datetime

class ContentPipeline:
    def __init__(self):
        """Initialize the pipeline with necessary API keys."""
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.vadoo_api_key = os.getenv('VADOO_API_KEY')
        self.analyzer = YouTubeShortsAnalyzer(self.youtube_api_key)

    async def generate_content(self):
        """Main pipeline to generate and post content."""
        try:
            # Step 1: Get and analyze trending shorts
            print("🔍 Analyzing trending YouTube Shorts...")
            trending_shorts = self.analyzer.get_trending_shorts(max_results=3)
            
            if not trending_shorts:
                raise Exception("No trending shorts found")
            
            # Analyze the top trending short
            top_short = trending_shorts[0]
            analysis = analyze_short(top_short)
            
            if not analysis:
                raise Exception("Failed to analyze trending short")
            
            # Generate a script based on the analysis
            script = generate_short_script(top_short, analysis)
            
            if not script:
                raise Exception("Failed to generate script")
            
            # Step 2: Send to Vadoo for video generation
            print("🎬 Sending to Vadoo for video generation...")
            vadoo_response = await self.create_vadoo_video(script)
            
            if not vadoo_response['success']:
                raise Exception(f"Vadoo generation failed: {vadoo_response['error']}")
            
            # Step 3: Wait for Vadoo webhook (simulated here)
            print("⏳ Waiting for video generation...")
            video_data = await self.wait_for_vadoo_completion(vadoo_response['job_id'])
            
            if not video_data['success']:
                raise Exception(f"Video generation failed: {video_data['error']}")
            
            # Step 4: Post to YouTube
            print("📤 Posting to YouTube...")
            youtube_response = await self.post_to_youtube(
                video_url=video_data['video_url'],
                title=f"Trending Style: {top_short['title']}",
                description=f"Inspired by trending content\n\nAnalysis:\n{analysis[:500]}..."
            )
            
            return {
                'success': True,
                'youtube_url': youtube_response['video_url'],
                'analysis': analysis,
                'script': script
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def create_vadoo_video(self, script):
        """Send script to Vadoo for video generation."""
        try:
            # Format the script for Vadoo's API
            vadoo_payload = {
                'script': script,
                'style': 'youtube_shorts',  # Assuming Vadoo has this style preset
                'aspect_ratio': '9:16',
                'duration': '60',  # Maximum duration for Shorts
                'webhook_url': 'your_webhook_url'  # Replace with your webhook URL
            }
            
            # This is a placeholder for your actual Vadoo API implementation
            headers = {
                'Authorization': f'Bearer {self.vadoo_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Replace with actual Vadoo API endpoint
            response = requests.post(
                'https://api.vadoo.ai/v1/videos',
                json=vadoo_payload,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'job_id': data['job_id']
                }
            else:
                return {
                    'success': False,
                    'error': f"Vadoo API error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def wait_for_vadoo_completion(self, job_id):
        """Wait for Vadoo webhook callback (simulated here)."""
        try:
            # This would normally be handled by your webhook endpoint
            # For now, we'll simulate polling the status
            max_attempts = 30
            attempt = 0
            
            while attempt < max_attempts:
                # Replace with actual Vadoo status check endpoint
                headers = {
                    'Authorization': f'Bearer {self.vadoo_api_key}',
                }
                
                response = requests.get(
                    f'https://api.vadoo.ai/v1/videos/{job_id}',
                    headers=headers
                )
                
                if response.status_code == 200:
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
                await asyncio.sleep(10)  # Wait 10 seconds between checks
            
            return {
                'success': False,
                'error': 'Timeout waiting for video generation'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def post_to_youtube(self, video_url, title, description):
        """Post the generated video to YouTube Shorts."""
        try:
            # This would be your implementation of YouTube upload
            # You might want to download the video from Vadoo first
            
            # Placeholder for successful upload
            return {
                'success': True,
                'video_url': f"https://youtube.com/shorts/example_id",
                'status': 'published'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

async def run_pipeline():
    """Run the content pipeline."""
    pipeline = ContentPipeline()
    result = await pipeline.generate_content()
    
    if result['success']:
        print("\n✅ Content Pipeline Complete!")
        print(f"YouTube URL: {result['youtube_url']}")
        print("\nAnalysis:")
        print(result['analysis'])
        print("\nGenerated Script:")
        print(result['script'])
    else:
        print(f"\n❌ Pipeline Error: {result['error']}")

# Run the pipeline
if __name__ == "__main__":
    asyncio.run(run_pipeline()) 